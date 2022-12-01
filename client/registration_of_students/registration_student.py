from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text


class FSMAdmin(StatesGroup):
    num_card_student = State()
    name = State()


# @dp.message_handler(commands=['загрузить'], state=None)
async def download_process_command(message: types.Message):
    """команда по которой запускаем мушину состояний"""
    await FSMAdmin.num_card_student.set()
    await message.reply('введи номер зачётки студента')


# @dp.message_handler(state=FSMAdmin.num_card_student)
async def download_num_card_student_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после download_process_command) в машине состояний,
    которая принимает номер зачётки"""
    async with state.proxy() as data:
        data['num_card_student'] = message.text
    await FSMAdmin.next()
    await message.reply('А теперь введи его имя ')


# @dp.message_handler(state=FSMAdmin.name)
async def download_name_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после download_num_card_student_process_command) в машине состояний,
    которая принимает имя и выходит из машины сотояний"""
    async with state.proxy() as data:
        data['name'] = message.text
        await message.reply(str(data))
    await state.finish()


@dp.message_handler(state='*', commands=['отмена'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_process_command(messgae: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await messgae.reply('Ok')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(download_process_command, commands=['загрузить'], state=None)
    dp.register_message_handler(download_num_card_student_process_command, state=FSMAdmin.num_card_student)
    dp.register_message_handler(download_name_process_command, state=FSMAdmin.name)
    dp.register_message_handler(cancel_process_command, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_process_command, Text(equals='отмена', ignore_case=True), state="*")

