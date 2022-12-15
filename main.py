from aiogram.utils import executor
from create_bot import dp
from client.registration_of_students import registration_student_handlers
from admin.work_with_groups import add_new_group_handlers
from admin.add_new_students import add_new_students_handlers
from admin.moderarot import moderator_handlers
from admin.work_with_groups import get_info_about_students_handlers
from admin.send_message import send_mesage_in_group_handlers
from data_base import sqllite_db


async def on_start(_):
    print('Bot is online')
    sqllite_db.sql_start()  # подключаем базу данных, и создаём нужные таблицы, если их нет


# регистрируем хендлеры
registration_student_handlers.register_handlers_client_add_new_students(dp)
add_new_group_handlers.register_handlers_admin_add_new_group(dp)
add_new_students_handlers.register_handlers_admin_add_new_group(dp)
moderator_handlers.register_handlers_update_moderator(dp)
get_info_about_students_handlers.register_handlers_admin_get_info_about_students(dp)
send_mesage_in_group_handlers.register_handlers_admin_send_message_in_group(dp)

executor.start_polling(dp, skip_updates=False, on_startup=on_start)

# доработать при изменении данных о студенте, что бы его id_telegram не терялся
# доработать команду send_message_in_group (саму отправку в группы, а точнее... нужно добавить машину состояний и рабочие кнопки)
# добавить комманду, по которой можно добавить сразу много студентов, отправляя csv файлик в бот, конструкция id, num_student_card, name_student
# доработать команду get_small_info, что бы в группах показывались не только номера групп, а так же названия
