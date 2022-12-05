from data_base.sqllite_db import sql_get_one_column, sql_admin_add_new_student, sql_get_all_groups
from aiogram import types


class AddNewStudent:
    def __init__(self, data):
        """data - это типо словаря из машины состояний"""
        self.data = data

    def check_num_card_student(self):
        """проверяет нет ли уже этого студента в базе по номеру зачётки
        если такого студента нет, то возвращает True, если такой студент есть, то False"""
        lst_num_student_card = sql_get_one_column('main_data_base', 'num_student_card')
        # print(lst_num_student_card)
        # print(self.data.get("num_card_student"))
        if self.data.get("num_card_student") not in lst_num_student_card:
            return True
        return False
        # sql_get_one_column('') # проверить как работает функция

    def add_new_student(self):
        if self.check_num_card_student():  # если студента нет в базе (проверяем по зачётке)
            # добавляем его в базу данных
            sql_admin_add_new_student(self.data)
            return True
        sql_admin_add_new_student(self.data, command=False)
        return False

    def add_new_student_with_answer(self):
        if self.add_new_student():
            return f'Студент <b>{self.data.get("name_student")}</b>\nномер зачётки: <b>' \
                   f'{self.data.get("num_card_student")}</b>\nуспешно добавлен в группу <b>{self.data.get("group")}</b>'
        else:
            return f'Данные пидора изменены'


class MessageForCallback:
    """клас для добавления студентов в группы"""

    def __init__(self):
        self.messege_for_add_in_group_callback = 'Добавить в '
        self.num_groups = list()

    def add_in_group_message(self, callback_query: types.CallbackQuery):
        """метод, который составляет из нажатых inline кнопок сообщение, в какие группы добавить """
        num_group = int(callback_query.data.replace('group_', ''))
        groups = sql_get_all_groups()
        for group in groups:
            if group['num_group'] == num_group:
                if num_group in self.num_groups:
                    self.messege_for_add_in_group_callback += f"<s>{group['name_group']}</s>, "
                else:
                    self.messege_for_add_in_group_callback += f"{group['name_group']}, "
                    self.num_groups.append(num_group)
                return self.messege_for_add_in_group_callback

    def delete_last_info(self):
        self.messege_for_add_in_group_callback = 'Добавить в '
        self.num_groups = list()
