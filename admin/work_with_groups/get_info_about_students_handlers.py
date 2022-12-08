"""хендлеры для получение данныех о студентах"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from admin.work_with_groups.get_info_about_students import GetInfoAboutStudents

from admin.moderarot.moderator import Moderator


# @dp.message_handler(commands=['get_small_info'], state=None)
async def get_small_info_about_students_process_command(message: types.Message):
    """получить инфу о студентах в csv файле: id, id_telegram, num_student_card, name_student, Status, all_groups"""
    if not Moderator().check_moderator(id_telegram=message.from_user.id):
        await message.reply(f'Ты не модератор!')
        return

    await message.reply(f'Отправляю <b>csv файл</b> с данными о студентах'
                        f'\n{GetInfoAboutStudents().get_small_info_with_answer()}')
    doc = open('data_base/data/small_info.csv', 'rb')
    await message.reply_document(doc)


def register_handlers_admin_get_info_about_students(dp: Dispatcher):
    dp.register_message_handler(get_small_info_about_students_process_command, commands=['get_small_info'], state=None)

