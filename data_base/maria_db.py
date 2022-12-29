import pymysql.cursors
from data_base.sqllite_db import sql_get_row, sql_start
import aioschedule
import asyncio
from create_bot import bot
from typing import List, Dict
from aiogram.utils.exceptions import BotBlocked


# connection is not autocommit by default. So you must commit to save
# your changes.
# connection.commit()


def connection_with_mariadb():
    """Connect to the database"""
    global connection
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='',
                                 database='sm_app',
                                 cursorclass=pymysql.cursors.DictCursor)

    print('Maria db connected OK')


def get_info_mariadb():
    """получить данные из базы данных, где is_sent = 0"""

    cursor = connection.cursor()
    connection.begin()  # позволяет обновить данные из mariadb (что бы когда добавили данные в phpmyadmin, то он
    # их увидел)
    cursor.execute("SELECT * FROM `user` WHERE `is_sent` = 0")
    students_mariadb = cursor.fetchall()

    for student in students_mariadb:
        print("Database: {0}".format(student))

    cursor.close()
    return students_mariadb


def update_info_mariadb(data: dict):
    """
    Обновляет информацию в базе mariadb
    :param data: словарь формата {'id': 2, 'num_student_card': 22222, 'message': 'i need your life', 'is_sent': None,
    'sentdatetime': datetime.datetime(2022, 12, 28, 16, 22, 24), 'if_delivered': None}
    :return: None
    """

    with connection.cursor() as cursor:
        request = "UPDATE `user` SET `is_sent` = {0}, `if_delivered` = {1} WHERE `user`.`id` = {2}".format(
            data['is_sent'], f"'{data['if_delivered']}'", data['id'])
        print(request)
        cursor.execute(request)
        connection.commit()


async def check_maria_db():
    """проверяет нет ли сообщений для отправки, и если есть, то отправляет нужному пользователю,
    после чего обновляет данные в mariadb"""
    data_mariadb = get_info_mariadb()
    if len(data_mariadb) != 0:
        for student_maria_db in data_mariadb:
            student_maria_db: Dict
            try:
                id_telegram = sql_get_row(num_student_card=student_maria_db['num_student_card'])[0][1]
            except TypeError:
                print(f"Error don't have num_student_card {student_maria_db['num_student_card']}")
                continue

            try:
                await bot.send_message(id_telegram, student_maria_db['message'])
                student_maria_db['if_delivered'] = 'yes'
            except BotBlocked:
                student_maria_db['if_delivered'] = 'block'
            finally:
                student_maria_db['is_sent'] = 1
                update_info_mariadb(data=student_maria_db)

    # await bot.send_message(664295561, 'сука')


async def scheduler_mariadb():
    # aioschedule.every().day.at(time_reminder).do(send_reminder)
    """
    каждые 3 секунды запускает функцию check_maria_db
    :return: None
    """
    aioschedule.every(3).seconds.do(check_maria_db)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


if __name__ == '__main__':
    sql_start()
    connection_with_mariadb()
    check_maria_db()
    # asyncio.run(scheduler_mariadb())
    # print(get_info_mariadb())
    # for i in range(100):
    #     print(f'time is: {i}')
    #     time.sleep(1)

# get_info_mariadb()
