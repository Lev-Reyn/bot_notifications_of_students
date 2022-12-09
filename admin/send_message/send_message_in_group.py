from aiogram import types
from data_base.sqllite_db import sql_get_all_groups


class SendMesageInGroupCallback:
    """клас для добавления студентов в группы"""

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
                return self.messege_send_message_in_group_callback

    def delete_last_info(self):
        self.messege_send_message_in_group_callback = 'Добавить в '
        self.num_groups = list()
