from aiogram.utils import executor
from create_bot import dp
from client.registration_of_students import registration_student_handlers
from admin.work_with_groups import add_new_group_handlers
from admin.add_new_students import add_new_students_handlers
from admin.moderarot import moderator_handlers
from data_base import sqllite_db


async def on_start(_):
    print('Bot is online')
    sqllite_db.sql_start()  # подключаем базу данных, и создаём нужные таблицы, если их нет


registration_student_handlers.register_handlers_client_add_new_students(dp)
add_new_group_handlers.register_handlers_admin_add_new_group(dp)
add_new_students_handlers.register_handlers_admin_add_new_group(dp)
moderator_handlers.register_handlers_update_moderator(dp)

executor.start_polling(dp, skip_updates=False, on_startup=on_start)

# админская команда, позволяющая посмотреть всех зареганых студентов и информацию о них (вывод в csv: id, id_telegram, num_student_card, name_student, Status, all_groups)
# рассылка сообщений в группы (через сообщения в боте пока что)
