import sqlite3 as sq


def sql_start():
    """при запуске бота, должна создаваться или открываться база данных"""
    global base, cur
    base = sq.connect('data_base/student_base.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')

    # создаём основную таблицу main_data_base
    base.execute('CREATE TABLE IF NOT EXISTS main_data_base(id INTEGER PRIMARY KEY, id_telegram INTEGER)')
    base.commit()

    # создаём таблицу names_groups (там id групп и их названия)
    base.execute('CREATE TABLE IF NOT EXISTS names_groups(num_group INTEGER PRIMARY KEY, name_group TEXT)')
    base.commit()


async def sql_add_new_table_group_command(state) -> int:
    """создать новую таблицу для новой группы"""

    # узнаём какие уже есть группы (именно их id и создаём следующее id)
    id_from_main_data_base = cur.execute('SELECT num_group FROM names_groups').fetchall()
    if len(id_from_main_data_base) != 0:
        new_id_for_new_group = max(list(map(lambda id_group: id_group[0], id_from_main_data_base))) + 1
        print('new id for group is OK')
    else:
        new_id_for_new_group = 0

    # создаём таблицу для новой группы
    base.execute('CREATE TABLE IF NOT EXISTS group_{0}(id PRIMARY KEY, num_student_card TEXT, name_student TEXT, '
                 'id_telegram INTEGER, Status INTEGER)'.format(new_id_for_new_group))
    base.commit()
    # добавляем в таблицу names_groups новую строку (новую группу)
    async with state.proxy() as data:
        cur.execute('INSERT INTO names_groups VALUES(?, ?)', (new_id_for_new_group, data.get("name_group")))
        base.commit()
    return new_id_for_new_group


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO info_students VALUES(?, ?)', tuple(data.values()))
        base.commit()
