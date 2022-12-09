from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from data_base.sqllite_db import sql_get_all_groups


def inline_kb_send_message_in_group():
    """инлайн клавиатура со всеми группами """
    global lst_inline_buttons_send_message_in_group
    global inline_kb_send_message_in_group
    lst_inline_buttons_send_message_in_group = []
    groups = sql_get_all_groups()

    for group in groups:
        lst_inline_buttons_send_message_in_group.append(
            InlineKeyboardButton(f'id {group["num_group"]} | {group["name_group"]}',
                                 callback_data=f'send_message_in_group_{group["num_group"]}'),
        )
    lst_inline_buttons_send_message_in_group.append(
        InlineKeyboardButton(f'Отправить', callback_data=f'send_send_message_in_group'), )

    inline_kb_send_message_in_group = InlineKeyboardMarkup()
    for buttons_groups in lst_inline_buttons_send_message_in_group:
        inline_kb_send_message_in_group.add(buttons_groups)
    return inline_kb_send_message_in_group
