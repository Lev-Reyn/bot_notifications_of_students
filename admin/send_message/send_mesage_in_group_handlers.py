"""хэндлеры для отправки сообщения определённой группе"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from keyboard.keyboard_admin.keyboard_add_new_student import inline_kb_groups_func
from aiogram.dispatcher.filters import Text
from admin.moderarot.moderator import Moderator
from keyboard.keyboard_admin.keyboard_send_message_in_group import inline_kb_send_message_in_group, \
    inline_kb_send_message_in_group_confirmation_func
from admin.send_message.send_message_in_group import SendMesageInGroupCallback, GetIdTelegramGroup
from admin.send_message.yes_no_other_handlers import send_message
from client.registration_of_students.registration_student_handlers import cancel_process_command



class FSMAdminSendMessageInGroup(StatesGroup):
    message = State()
    callback_group = State()
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
async def update_num_text_send_message_in_group(message: types.Message, new_value):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"{new_value}", reply_markup=inline_kb_send_message_in_group())


#
# # дорабатыаваем (функция для обновления/редактирования сообщения)
async def update_num_text_send_message_in_group_confirmation(message: types.Message, new_value):
    """изменяет сообщение без добавления клавиатуры"""
    await message.edit_text(f"{new_value}")


# @dp.callback_query_handler(Text(startswith="send_message_in_group_"), state=FSMAdminSendMessageInGroup.callback_group)
async def process_callback_kb_keyboard_send_message_in_group(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    message_groups = messege_send_message_in_group_callback.send_message_in_group_message(callback_query)
    await update_num_text_send_message_in_group(callback_query.message, message_groups)


# @dp.callback_query_handler(Text(startswith="send_send_message_in_group"),
#                            state=FSMAdminSendMessageInGroup.callback_group)
async def process_callback_kb_keyboard_send_send_message_in_group(callback_query: types.CallbackQuery,
                                                                  state: FSMContext):
    # print(messege_send_message_in_group_callback.num_groups,
    #       messege_send_message_in_group_callback.messege_send_message_in_group_callback, 'TEST')
    # await add_new_student_group_process_command(callback_query.message, state)
    await send_message_in_group_group_process_command(callback_query.message, state)


# @dp.message_handler(state=FSMAdminSendMessageInGroup.group) этого и не надо
async def send_message_in_group_group_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается из process_callback_kb_keyboard_send_send_message_in_group) в машине состояний,
    которая принимает группу в которой будет студент"""
    # await message.reply('пока что работает' + message.text)
    # await message.reply(str(messege_send_message_in_group_callback.num_groups))

    async with state.proxy() as data:
        data['group'] = messege_send_message_in_group_callback.num_groups  # номера всех групп, куда добавить
        await message.edit_text(f'Подтверждаете, что хотите'
                                f' <b>{messege_send_message_in_group_callback.messege_send_message_in_group_callback}</b>'
                                f' сообщение <b>{data.get("message")}</b>?',
                                reply_markup=inline_kb_send_message_in_group_confirmation_func())

    await FSMAdminSendMessageInGroup.next()


#
# @dp.callback_query_handler(Text(startswith="confirmation_send_msg_in_group"),
#                            state=FSMAdminSendMessageInGroup.confirmation)
async def send_message_in_group_confirmation_process_command(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirmation_send_msg_in_group_cancel':
        await callback_query.message.edit_text('отменяю')
        await cancel_process_command(callback_query.message, state)
        await update_num_text_send_message_in_group_confirmation(callback_query.message, f'🟥 отмена')
    else:
        async with state.proxy() as data:
            for_callback = messege_send_message_in_group_callback.for_callback(question=data.get('message'))
            await send_message(message=callback_query.message,
                               message_for_send=data.get('message'),
                               data_id_telegram=GetIdTelegramGroup().get_students_for_send_message(
                                   messege_send_message_in_group_callback.num_groups), for_callback=for_callback)
            await update_num_text_send_message_in_group_confirmation(callback_query.message,
                                                                     f'✅ сообщение  <b>{data.get("message")}'
                                                                     f'</b> отправлено')
        # await callback_query.message.edit_text('нужно доработать, пока что ничего не отправляет')
    messege_send_message_in_group_callback.delete_last_info()  # удаляем данные сообщения

    await state.finish()  # пока что finish


def register_handlers_admin_send_message_in_group(dp: Dispatcher):
    dp.register_message_handler(send_message_in_group_process_command, commands=['send_message_in_group'], state=None)
    dp.register_message_handler(send_message_in_group_message_process_command,
                                state=FSMAdminSendMessageInGroup.message),
    dp.register_callback_query_handler(process_callback_kb_keyboard_send_message_in_group,
                                       Text(startswith="send_message_in_group_"),
                                       state=FSMAdminSendMessageInGroup.callback_group),
    dp.register_callback_query_handler(process_callback_kb_keyboard_send_send_message_in_group,
                                       Text(startswith="send_send_message_in_group"),
                                       state=FSMAdminSendMessageInGroup.callback_group),
    dp.register_callback_query_handler(send_message_in_group_confirmation_process_command,
                                       Text(startswith="confirmation_send_msg_in_group"),
                                       state=FSMAdminSendMessageInGroup.confirmation)
