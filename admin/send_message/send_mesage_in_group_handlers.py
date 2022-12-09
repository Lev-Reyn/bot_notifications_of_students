"""хэндлеры для отправки сообщения определённой группе"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from keyboard.keyboard_admin.keyboard_add_new_student import inline_kb_groups_func
from aiogram.dispatcher.filters import Text
from admin.moderarot.moderator import Moderator
from keyboard.keyboard_admin.keyboard_send_message_in_group import inline_kb_send_message_in_group
from admin.send_message.send_message_in_group import SendMesageInGroupCallback


class FSMAdminSendMessageInGroup(StatesGroup):
    message = State()
    callback_group = State()
    group = State()
    confirmation = State()


messege_send_message_in_group_callback = SendMesageInGroupCallback()


# @dp.message_handler(commands=['send_message_in_group'], state=None)
async def send_message_in_group_process_command(message: types.Message):
    """команда по которой запускаем мушину состояний, для отправки сообщения в группу"""
    if not Moderator().check_moderator(id_telegram=message.from_user.id):
        await message.reply(f'Ты не модератор!')
        return
    await FSMAdminSendMessageInGroup.message.set()
    await message.reply('Вы решили отправить сообщение в группу\nвведите <b>текст сообщения</b>')


# @dp.message_handler(state=FSMAdminSendMessageInGroup.message)
async def send_message_in_group_message_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после send_message_in_group_process_command) в машине состояний,
    которая принимает текст сообщения для отправки студентам (в группу)"""
    async with state.proxy() as data:
        data['message'] = message.text
    await message.reply('Теперь выберите <b>группу</b> в которую хотите отправить сообщение',
                        reply_markup=inline_kb_send_message_in_group())
    await FSMAdminSendMessageInGroup.next()


# дорабатыаваем (функция для обновления/редактирования сообщения)
async def update_num_text(message: types.Message, new_value):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"{new_value}", reply_markup=inline_kb_groups_func())


@dp.callback_query_handler(Text(startswith="send_message_in_group_"), state=FSMAdminSendMessageInGroup.callback_group)
async def process_callback_kb_keyboard_groups(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    message_groups = messege_send_message_in_group_callback.send_message_in_group_message(callback_query)
    await update_num_text(callback_query.message, message_groups)


@dp.callback_query_handler(Text(startswith="send_send_message_in_group"),
                           state=FSMAdminSendMessageInGroup.callback_group)
async def process_callback_kb_keyboard_groups_send(callback_query: types.CallbackQuery, state: FSMContext):
    print(messege_send_message_in_group_callback.num_groups,
          messege_send_message_in_group_callback.messege_send_message_in_group_callback, 'TEST')
    # await add_new_student_group_process_command(callback_query.message, state)


def register_handlers_admin_send_message_in_group(dp: Dispatcher):
    dp.register_message_handler(send_message_in_group_process_command, commands=['send_message_in_group'], state=None)
    dp.register_message_handler(send_message_in_group_message_process_command, state=FSMAdminSendMessageInGroup.message)
