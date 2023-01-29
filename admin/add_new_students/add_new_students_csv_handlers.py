"""хэндлеры для добавления новых студентов в базу данных"""
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
from admin.add_new_students.add_new_students_csv import AddNewStudentsCsv


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def add_new_students_csv_finish_process_command(message: types.Message):
    """команда принимает csv файл со студентами, которых добавить"""
    if not Moderator().check_moderator(id_telegram=message.from_user.id):
        await message.reply(f'Ты не модератор!')
        return
    if message.document.file_name[-4:] != '.csv':
        await message.reply('Пока что я принимаю только csv файлы для добавления студентов')
        return
    await message.document.download('data_base/data/add_new_students.csv')
    try:
        AddNewStudentsCsv().add_new_students_csv()  # add all the students that are in the csv file
        await message.reply('Супер, не забудьте проверить, все ли студенты были добавлены корректно командой '
                            '/get_small_info')
    except TypeError:
        await message.reply('произошла ошибка, в столбце group должны быть списки (массивы)')
    except KeyError:
        await message.reply('Возможно проблема с разделителями, в качестве разделителя нужно использовать <b>";"</b>\n '
                            'либо нет какого-либо столбца')
    except Exception:
        await message.reply('error')
