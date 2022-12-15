from aiogram import types
from data_base.sqllite_db import sql_get_all_groups, sql_get_one_column, sql_create_new_column, add_new_row
from aiogram import types
import sqlite3
import datetime


class SendMesageInGroupCallback:
    """класс для добавления групп, а именно куда отправить, в какие группы"""

    def __init__(self):
        self.messege_send_message_in_group_callback = 'Отправить в '
        self.num_groups = list()

    def send_message_in_group_message(self, callback_query: types.CallbackQuery):
        """метод, который составляет из нажатых inline кнопок сообщение, в какие группы добавить """
        num_group = int(callback_query.data.replace('send_message_in_group_', ''))
        groups = sql_get_all_groups()
        for group in groups:
            if group['num_group'] == num_group:
                if num_group in self.num_groups:
                    self.messege_send_message_in_group_callback += f"<s>{group['name_group']}</s>, "
                else:
                    self.messege_send_message_in_group_callback += f"{group['name_group']}, "
                    self.num_groups.append(num_group)
                return self.messege_send_message_in_group_callback[:-2]

    def delete_last_info(self):
        self.messege_send_message_in_group_callback = 'Отправить в '
        self.num_groups = list()

    def get_columns_for_answer_in_group(self, num_group):
        """метод для получения номера вопроса, который сейчас задаётся (именно для этой группы)
        """
        num_answer = 1
        while True:
            try:
                result = sql_get_one_column(name_table=f'group_{num_group}', name_column=f'answer_{num_answer}')
                num_answer += 1
            except sqlite3.OperationalError:
                break
        return num_answer

    def new_column_for_answer(self, num_group, num_answer):
        """создаёт два новых столбца в базе данных, answer_ и datetime_
        принимает номер группы и номер вопроса
        """
        sql_create_new_column(name_table=f'group_{num_group}', name_column=f'answer_{num_answer}', type_column='TEXT')
        sql_create_new_column(name_table=f'group_{num_group}', name_column=f'datetime_{num_answer}', type_column='TEXT')


    def create_columns_for_answers(self) -> dict:
        """создаёт в нужных таблицах новые столбцы (в группах столбцы ответов на вопрос)
        и возвращает cловарь с форматом dict[num_group] = num_answer (ключ - номер группы, значение - номер ответа на
        вопрос
        """
        self.data_group_answer = {}  # словарь где будет записан номер группы и какой вопрос сейчас задаётся в этой гр.
        for group in self.num_groups:
            num_answer = self.get_columns_for_answer_in_group(num_group=group)  # получаем номер вопроса, который задаём
            self.data_group_answer[group] = num_answer
            self.new_column_for_answer(num_group=group, num_answer=num_answer)  # создаём столбец в таблице этой группы
        return self.data_group_answer

    def for_callback(self, question: str) -> str:
        """создаёт доп часть для callback, где указан номер группы и номер вопроса в каждой группе, ну а так же создаёт
        новые столбцы для ответов на вопросы в нужных таблицах (группах)"""
        self.create_columns_for_answers()  # создаём столбцы ответов на вопрос в нужных таблицах (группах)
        # а так же собрали инфу какой вопрос для какой группы сейчас задаётся

        # добавляем вопросы в group_num_group_questions
        for num_group, num_answer in self.data_group_answer.items():
            data = {
                'name_table': f'group_{num_group}_questions',
                'names_columns': ['num_question', 'question', 'datetime_send'],
                'values': [num_answer, f"'{question}'", f"'{datetime.datetime.now()}'"]
            }
            add_new_row(data=data)


        """group_0_1_4<>question_13_17_9"""
        for_callback = 'group'
        for num_group in self.num_groups:
            for_callback += f'_{num_group}'
        for_callback += '<>question'
        for num_answer in self.data_group_answer.values():
            for_callback += f'_{num_answer}'
        return for_callback


class GetIdTelegramGroup:

    def get_students_for_send_message(self, groups: list) -> list:
        """метод для получения id_telegram всех студентов, кому отправить сообщения
        (только тех, кто активировал бота) """
        data_id_telegram = []  # список, где будут храниться все id_telegram для отправки сообщения
        for group in groups:
            data_id_telegram += sql_get_one_column(name_table=f'group_{group}', name_column='id_telegram')
        data_id_telegram = list(filter(lambda id_telegram: id_telegram != None, data_id_telegram))
        data_id_telegram = list(set(data_id_telegram))
        self.data_id_telegram = data_id_telegram
        return self.data_id_telegram
