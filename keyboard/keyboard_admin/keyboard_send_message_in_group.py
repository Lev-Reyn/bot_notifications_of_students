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


def inline_kb_send_message_in_group_confirmation_func():
    """функция, создания inline кнопок для подтверждения отправки сообщения"""
    global lst_inline_buttons_send_message_in_group_confirmation
    global inline_kb_send_message_in_group_confirmation
    lst_inline_buttons_send_message_in_group_confirmation = []
    # кнопка подтверждения
    lst_inline_buttons_send_message_in_group_confirmation.append(
        InlineKeyboardButton(f'Подтвердить', callback_data='confirmation_send_msg_in_group_conf'))
    # кнопка отмены
    lst_inline_buttons_send_message_in_group_confirmation.append(
        InlineKeyboardButton(f'Отменить', callback_data='confirmation_send_msg_in_group_cancel'))
    inline_kb_send_message_in_group_confirmation = InlineKeyboardMarkup()
    for button_conf in lst_inline_buttons_send_message_in_group_confirmation:
        inline_kb_send_message_in_group_confirmation.add(button_conf)
    return inline_kb_send_message_in_group_confirmation


def inline_kb_send_message_in_group_yes_no_other(for_callback: str):
    """клавиатура, которая отправляется вместе с сообщением студентам
    for_callback - принимает строку вида group_0_1_4<>question_13_9 (то есть в какие группы и какие это вопрос по счёту)
    """
    global lst_inline_buttons_send_message_in_group_yes_no_other
    global inline_kb_send_message_in_group_yes_no_other
    lst_inline_buttons_send_message_in_group_yes_no_other = []
    lst_inline_buttons_send_message_in_group_yes_no_other.append(
        InlineKeyboardButton('Да', callback_data='yes_no_other_yes_' + for_callback)
    )
    print('yes_no_other_yes_' + for_callback)
    lst_inline_buttons_send_message_in_group_yes_no_other.append(
        InlineKeyboardButton('Нет', callback_data='yes_no_other_no_' + for_callback)
    )
    print('yes_no_other_no_' + for_callback)
    lst_inline_buttons_send_message_in_group_yes_no_other.append(
        InlineKeyboardButton('Другое', callback_data='yes_no_other_other_' + for_callback)
    )
    print('yes_no_other_other_' + for_callback)
    inline_kb_send_message_in_group_yes_no_other = InlineKeyboardMarkup(row_width=2)
    for button in lst_inline_buttons_send_message_in_group_yes_no_other:
        inline_kb_send_message_in_group_yes_no_other.add(button)
    return inline_kb_send_message_in_group_yes_no_other
