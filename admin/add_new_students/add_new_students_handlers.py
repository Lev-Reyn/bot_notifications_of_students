"""хэндлеры для добавления нового студента"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from admin.add_new_students.add_new_students import AddNewStudent, MessageForCallback
from keyboard.keyboard_admin.keyboard_add_new_student import inline_kb_groups_func
from aiogram.dispatcher.filters import Text
from admin.moderarot.moderator import Moderator
from data_base.sqllite_db import sql_get_all_groups, sql_admin_add_student_in_table_group, \
    sql_admin_add_student_in_table_group_delete_row, sql_get_groups_of_student


class FSMAdminAddNewStudent(StatesGroup):
    num_card_student = State()
    name_student = State()
    group_callback = State()
    group = State()  # в какую группу пойдёт студент


message_for_add_in_group_callback = MessageForCallback()  # для составления сообщения добавления студента в группу


# @dp.message_handler(commands=['new_student'], state=None)
async def add_new_student_process_command(message: types.Message):
    """команда по которой запускаем мушину состояний, для добавления нового студента"""
    if not Moderator().check_moderator(id_telegram=message.from_user.id):
        await message.reply(f'Ты не модератор!')
        return
    await FSMAdminAddNewStudent.num_card_student.set()
    await message.reply('Вы решили добавить нового студента, введите его <b>номер зачётки</b>')


# @dp.message_handler(state=FSMAdminAddNewStudent.num_card_student)
async def add_new_student_num_card_student_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после add_new_student_process_command) в машине состояний,
    которая принимает номер зачёчки студента"""
    async with state.proxy() as data:
        data['num_student_card'] = message.text
    if not AddNewStudent(data).check_num_card_student():
        await message.reply(f'Студент с номером зачётки {data.get("num_student_card")} уже присутствует, но вы можете'
                            f' изменить по нему данные, либо воспользуйтесь командой /отмена что бы не изменять по нему'
                            f' информацию')
    await message.reply('Теперь введите <b>имя студента</b>')
    await FSMAdminAddNewStudent.next()


# @dp.message_handler(state=FSMAdminAddNewStudent.name_student)
async def add_new_student_name_student_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после add_new_student_num_card_student_process_command) в машине состояний,
    которая принимает имя студента"""
    async with state.proxy() as data:
        data['name_student'] = message.text
    await message.reply('и последнее, введите <b>id группы или название группы (пока не придумал, что именно)</b>',
                        reply_markup=inline_kb_groups_func())
    await FSMAdminAddNewStudent.next()


# дорабатыаваем (функция для обновления/редактирования сообщения) https://mastergroosha.github.io/aiogram-2-guide/buttons/
async def update_num_text(message: types.Message, new_value):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"{new_value}", reply_markup=inline_kb_groups_func())


# @dp.callback_query_handler(Text(startswith="add_in_group_"), state=FSMAdminAddNewStudent.group_callback)
async def process_callback_kb_keyboard_groups(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    message_groups = message_for_add_in_group_callback.add_in_group_message(callback_query)
    await update_num_text(callback_query.message, message_groups)


# @dp.callback_query_handler(Text(startswith="send_groups"), state=FSMAdminAddNewStudent.group_callback)
async def process_callback_kb_keyboard_groups_send(callback_query: types.CallbackQuery, state: FSMContext):
    await add_new_student_group_process_command(callback_query.message, state)


# @dp.message_handler(state=FSMAdminAddNewStudent.group)
async def add_new_student_group_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после add_new_student_name_student_process_command) в машине состояний,
    которая принимает группу в которой будет студент"""
    await message.reply('пока что работает' + message.text)
    await message.reply(str(message_for_add_in_group_callback.num_groups))

    async with state.proxy() as data:
        data['group'] = message_for_add_in_group_callback.num_groups  # номера всех групп, куда добавить
        await message.reply(AddNewStudent(data).add_new_student_with_answer())

    message_for_add_in_group_callback.delete_last_info()  # удаляем данные сообщения
    await state.finish()


def register_handlers_admin_add_new_group(dp: Dispatcher):
    dp.register_message_handler(add_new_student_process_command, commands=['new_student'], state=None)
    dp.register_message_handler(add_new_student_num_card_student_process_command,
                                state=FSMAdminAddNewStudent.num_card_student)
    dp.register_message_handler(add_new_student_name_student_process_command, state=FSMAdminAddNewStudent.name_student)
    dp.register_message_handler(add_new_student_group_process_command, state=FSMAdminAddNewStudent.group),
    dp.register_callback_query_handler(process_callback_kb_keyboard_groups, Text(startswith="add_in_group_"),
                                       state=FSMAdminAddNewStudent.group_callback),
    dp.register_callback_query_handler(process_callback_kb_keyboard_groups_send, Text(startswith="send_groups"),
                                       state=FSMAdminAddNewStudent.group_callback)
    # dp.register_message_handler(cancel_process_command, state='*', commands=['отмена'])
    # dp.register_message_handler(cancel_process_command, Text(equals='отмена', ignore_case=True), state="*")
