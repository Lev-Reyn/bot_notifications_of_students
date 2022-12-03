from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from client.registration_of_students.for_registration import Registration


class FSMClientRegistration(StatesGroup):
    num_card_student = State()


# @dp.message_handler(commands=['загрузить'], state=None)
async def download_process_command(message: types.Message):
    """команда по которой запускаем мушину состояний"""
    await FSMClientRegistration.num_card_student.set()
    await message.reply('введи номер зачётки студента')


# @dp.message_handler(state=FSMClientRegistration.num_card_student)
async def download_num_card_student_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после download_process_command) в машине состояний,
    которая принимает номер зачётки"""
    async with state.proxy() as data:
        data['num_card_student'] = message.text
        await message.reply(Registration(data).check_registr_with_answer())

    await state.finish()


@dp.message_handler(state='*', commands=['отмена'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_process_command(messgae: types.Message, state: FSMContext):
    """выключает машину состояний, при том любую, которая была б включена"""
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await messgae.reply('Ok')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(download_process_command, commands=['загрузить'], state=None)
    dp.register_message_handler(download_num_card_student_process_command, state=FSMClientRegistration.num_card_student)
    dp.register_message_handler(cancel_process_command, state='*', commands=['отмена'])
    dp.register_message_handler(cancel_process_command, Text(equals='отмена', ignore_case=True), state="*")