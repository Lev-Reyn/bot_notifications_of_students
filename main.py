from aiogram.utils import executor
from create_bot import dp
from client.registration_of_students import registration_student


async def on_start(_):
    print('Bot is online')

registration_student.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_start)
