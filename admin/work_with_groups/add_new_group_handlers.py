"""хендлеры для создания новой группы"""
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
from aiogram import types, Dispatcher
from data_base.sqllite_db import sql_add_new_table_group_command, sql_get_all_groups, sql_create_new_table
from admin.moderarot.moderator import Moderator



class FSMAdminAddNewGroup(StatesGroup):
    name_group = State()


# @dp.message_handler(commands=['new_group'], state=None)
async def add_new_group_process_command(message: types.Message):
    if not Moderator().check_moderator(id_telegram=message.from_user.id):
        await message.reply(f'Ты не модератор!')
        return
    """команда по которой запускаем мушину состояний, для добавления новой группы"""
    await FSMAdminAddNewGroup.name_group.set()
    await message.reply('введите название для новой группы')


# @dp.message_handler(state=FSMAdminAddNewGroup.name_group)
async def add_new_group_finish_process_command(message: types.Message, state: FSMContext):
    """следующая команда (запускается после add_new_group_process_command) в машине состояний,
    которая принимает название новой группы"""
    async with state.proxy() as data:
        data['name_group'] = message.text
    new_id_for_new_group = await sql_add_new_table_group_command(state)
    sql_create_new_table(f'group_{new_id_for_new_group}_questions', 'num_question INTEGER PRIMARY KEY', 'question TEXT',
                         'datetime_send TEXT')
    async with state.proxy() as data:
        await message.reply(
            f'Группа <b>{data.get("name_group")}</b> добавлена и имеет <b>id {new_id_for_new_group}</b>')
    print(sql_get_all_groups())
    await state.finish()


def register_handlers_admin_add_new_group(dp: Dispatcher):
    dp.register_message_handler(add_new_group_process_command, commands=['new_group'], state=None)
    dp.register_message_handler(add_new_group_finish_process_command, state=FSMAdminAddNewGroup.name_group)
    # dp.register_message_handler(cancel_process_command, state='*', commands=['отмена'])
    # dp.register_message_handler(cancel_process_command, Text(equals='отмена', ignore_case=True), state="*")
