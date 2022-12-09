from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from data_base.sqllite_db import sql_get_all_groups


def inline_kb_groups_func():
    """инлайн клавиатура со всеми группами """
    global lst_inline_buttons_add_new_students
    global inline_kb_groups
    lst_inline_buttons_add_new_students = []
    groups = sql_get_all_groups()

    for group in groups:
        lst_inline_buttons_add_new_students.append(
            InlineKeyboardButton(f'id {group["num_group"]} | {group["name_group"]}',
                                 callback_data=f'add_in_group_{group["num_group"]}'),
        )
    lst_inline_buttons_add_new_students.append(
        InlineKeyboardButton(f'Отправить', callback_data=f'send_groups'),)

    inline_kb_groups = InlineKeyboardMarkup()
    for buttons_groups in lst_inline_buttons_add_new_students:
        inline_kb_groups.add(buttons_groups)
    return inline_kb_groups
