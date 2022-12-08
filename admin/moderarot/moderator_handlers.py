"""хэндлер для изменения модератора"""
from aiogram import types, Dispatcher
from admin.moderarot.moderator import Moderator


# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def update_moderator__process_command(message: types.Message):
    """изменяет модератора (админа)"""
    # if 'password' not in message.text:  # активировать позже, когда будет бот закончен
    #     return
    Moderator().update_moderator(id_telegram=message.from_user.id)
    ID_MODERATOR = message.from_user.id
    await message.reply(f'Модератор изменён, теперь id {ID_MODERATOR}')


def register_handlers_update_moderator(dp: Dispatcher):
    dp.register_message_handler(update_moderator__process_command, commands=['moderator'], is_chat_admin=True)
