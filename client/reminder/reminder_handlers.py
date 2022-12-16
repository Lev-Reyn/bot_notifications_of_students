from aiogram import types, Dispatcher
from data_base.sqllite_db import sql_get_columns_of_table, sql_get_all_groups, sql_get_id_telegram_where
from create_bot import bot
import asyncio
import aioschedule

time_reminder = '04:03'  # время отправки напоминания (каждый день отправляется)


async def send_reminder():
    """собирает id всех студентов, которые не ответили на последний вопрос и наплминет ответить"""
    groups_list = sql_get_all_groups()
    for group in groups_list:
        column_answer = sql_get_columns_of_table(name_table=f"group_{group['num_group']}")[-2]
        print(column_answer)
        students_not_respond = sql_get_id_telegram_where(column_need='id_telegram',
                                                         name_table=f"group_{group['num_group']}",
                                                         column_where=column_answer, where=None)
        for id_telegram in students_not_respond:
            await bot.send_message(id_telegram, 'Напоминаю ответить на последний вопрос')


async def scheduler():
    aioschedule.every().day.at(time_reminder).do(send_reminder)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)
