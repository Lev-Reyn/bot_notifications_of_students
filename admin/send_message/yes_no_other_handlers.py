from aiogram import types
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
from keyboard.keyboard_admin.keyboard_send_message_in_group import inline_kb_send_message_in_group_yes_no_other
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp
from admin.send_message.yes_no_other import YesNoOther
from aiogram.dispatcher import FSMContext


class FSMAdminOther(StatesGroup):
    """машина состояний для ответа 'другое'"""
    callback_answer = State()


async def send_message(message: types.Message, message_for_send: str, data_id_telegram: list, for_callback: str):
    """отправляет сообщения студентам
        message - types.Message из aiogram
        message_for_send - сообщение, которое отправляем
        data_id_telegram - список с id_telegram всех студентов, кому отправить сообщение
    """
    for id_telegram in data_id_telegram:
        try:
            await message.bot.send_message(id_telegram, message_for_send,
                                           reply_markup=inline_kb_send_message_in_group_yes_no_other(for_callback))

        except BotBlocked:
            print('бот заблокировали')
        except ChatNotFound:
            print('чат не найден')


# дорабатыаваем (функция для обновления/редактирования сообщения)
async def update_num_text_yes_no_other(message: types.Message, new_value,
                                       keyboard: types.InlineKeyboardMarkup = False):
    """функция для обновления текста с отправкой клавиатуры, если она передана"""
    if not keyboard:
        await message.edit_text(f"{new_value}")
    else:
        await message.edit_text(f"{new_value}", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="yes_no_other_"))
async def process_callback_kb_keyboard_yes_no_other(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    callback_data = callback_query.data.replace('yes_no_other_', '')
    if 'other' in callback_data:
        """запускаем машину состояний"""
        message_for_student = f'Отправь свой ответ, на вопрос {callback_query.message.text}'
        await FSMAdminOther.callback_answer.set()  # запускаем машину состояний
        await update_num_text_yes_no_other(callback_query.message, message_for_student)
        async with state.proxy() as data:
            data['callback_query_data'] = callback_query
    elif 'no' in callback_data or 'yes' in callback_data:
        message_for_student = YesNoOther().answer(callback_query)
        await update_num_text_yes_no_other(callback_query.message, message_for_student)


@dp.message_handler(state=FSMAdminOther.callback_answer)
async def send_message_in_group_message_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после process_callback_kb_keyboard_yes_no_other если студент ответил other) в
    машине состояний, которая принимает текст сообщения для ответа на вопрос"""
    async with state.proxy() as data:
        data['answer'] = message.text
        message_for_student = YesNoOther().answer(callback_query=data.get('callback_query_data'),
                                                  other_answer=message.text)
    print(message_for_student)
    await message.reply(message_for_student)

    await state.finish()

# @dp.callback_query_handler(Text(startswith="send_send_message_in_group"))
# async def process_callback_kb_keyboard_send_send_message_in_group(callback_query: types.CallbackQuery):
#     # print(messege_send_message_in_group_callback.num_groups,
#     #       messege_send_message_in_group_callback.messege_send_message_in_group_callback, 'TEST')
#     # await add_new_student_group_process_command(callback_query.message, state)
#     await send_message_in_group_group_process_command(callback_query.message, state)
