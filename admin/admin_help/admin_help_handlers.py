"""хэндлер для изменения модератора"""
from aiogram import types, Dispatcher
from admin.moderarot.moderator import Moderator
from create_bot import bot


# @dp.message_handler(commands=['help_admin'], is_chat_admin=True)
async def help_admin_process_command(message: types.Message):
    """изменяет модератора (админа)"""

    Moderator().update_moderator(id_telegram=message.from_user.id)
    ID_MODERATOR = message.from_user.id
    await message.reply(f'/get_small_info - получить некоторую информацию о добавленных студентах\n'
                        f'/new_student - добавить нового студента\n'
                        f'/new_group - добавить новую группу\n'
                        f'/send_message_in_group - отправить сообщение в группу/ группы\n'
                        f'/отмена - выйти из машины состояний')


async def all_message_process_command(message: types.Message):
    """срабатывает на все сообщения, и отправляет их модератору"""
    # доработать - отправлять так же имя и номер зачётки
    print(message.text)
    moder = Moderator()
    await bot.send_message(moder.get_moderator_id(), message.text)

def register_handlers_help_admin(dp: Dispatcher):
    dp.register_message_handler(help_admin_process_command, commands=['help_admin'], is_chat_admin=True)
    dp.register_message_handler(all_message_process_command)
