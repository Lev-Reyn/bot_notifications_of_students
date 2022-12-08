"""для работы с регистрацией и проверкой при каждом сообщении зарегестрирован ли пользователь"""
import json
import os
from data_base.sqllite_db import sql_get_one_column, sql_get_groups_of_student, sql_update_row, sql_get_row
from aiogram import types


#  измененить надо, так как json будет в папке data_base


class Registration:
    """класс для регистрации студента"""

    def __init__(self, data, message: types.Message):
        """data - это из 'async with state.proxy() as data:'
        и в ней должно быть первым элементом обязательно номер зачётки, ну и больше ничего"""
        self.num_card_student = tuple(data.values())[0]
        self.message = message

    def update_info_about_student_id_telegram_and_activate(self):
        """обновляет данные о студенте, а точнее о его id_telegram и то, что студент активировал бота (зареган)"""
        # нужно сохранить его данные, телеграмм id и изменить статус на зарегестрированного
        groups = sql_get_groups_of_student(num_student_card=self.num_card_student)
        print('группы, в которых находится данный студент', groups)
        # обновляем сначала данные в main_data_base
        data = {
            'name_table': 'main_data_base',
            'column_primary': 'num_student_card',
            'primary_value': self.num_card_student,
            'columns': {'id_telegram': self.message.from_user.id}
        }
        sql_update_row(data)
        print(f'данные main_data_base обновлены для студента с id_telegram {self.message.from_user.id}')

        # обновляем данные в таблицах group_
        for group in groups:
            data = {
                'name_table': f'group_{group}',
                'column_primary': 'num_student_card',
                'primary_value': self.num_card_student,
                'columns': {'id_telegram': self.message.from_user.id, 'Status': 1}
            }
            sql_update_row(data)
        print('В таблицах данные обновлены')

    def check_registr(self) -> bool:
        """проверяет, есть ли этот студент в базе данных data_access_open.json (открыт ли ему доступ)"""
        self.students_with_open_access = sql_get_one_column(name_table='main_data_base', name_column='num_student_card')
        # print(self.students_with_open_access)
        if self.num_card_student in self.students_with_open_access:
            return True
        return False

    def check_id_telegram(self):
        """проверяет есть ли такой же id_telegram уже в базе
        True - если уже есть в базе данных такой id_telegram
        False - если нет
        """
        id_telegram_lst = sql_get_one_column(name_table='main_data_base', name_column='id_telegram')
        if self.message.from_user.id in id_telegram_lst:
            return True
        return False

    def check_registr_with_answer(self):
        """проверяет, может ли данный студент зарегистрироваться в боте, и даёт ответ в том виде,
         который получит клиент"""
        if self.check_id_telegram():
            return f"Ваш аккаунт уже зарегистрирован под зачёткой " \
                   f"{sql_get_row(id_telegram=self.message.from_user.id)[0][2]} \nP.s. войди с другого телеграмм " \
                   f"аккаунта под старую зачётку, и тогда ты сможешь освободить свой аккаунт под новую зачётку"
        if self.check_registr():
            self.update_info_about_student_id_telegram_and_activate()  # обновляем данные в таблицах о студенте
            return f"Успешно зарегистрирован! \nСтудент  " \
                   f"\nНомер зачётки {self.num_card_student}"
        return f"Вы не можете зарегистрироваться в боте, обратитесь к преподавателю"
