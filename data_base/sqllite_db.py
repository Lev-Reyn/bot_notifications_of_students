import sqlite3 as sq


def sql_start():
    """при запуске бота, должна создаваться или открываться база данных"""
    global base, cur
    base = sq.connect('data_base/student_base.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')

    # создаём основную таблицу main_data_base
    base.execute('CREATE TABLE IF NOT EXISTS main_data_base'
                 '(id INTEGER PRIMARY KEY, id_telegram INTEGER, num_student_card TEXT)')
    base.commit()

    # создаём таблицу names_groups (там id групп и их названия)
    base.execute('CREATE TABLE IF NOT EXISTS names_groups(num_group INTEGER PRIMARY KEY, name_group TEXT)')
    base.commit()


async def sql_add_new_table_group_command(state) -> int:
    """создать новую таблицу для новой группы и все зависимости подключить (сделать столбец группы в main_data_base)"""

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
        cur.execute('ALTER TABLE main_data_base ADD COLUMN {0} INTEGER'.format(f'group_{new_id_for_new_group}'))

    return new_id_for_new_group


def sql_get_one_column(name_table: str, name_column: str):
    """получает имя таблиы и номер столбца, возвращает список со всеми данными в этом столбцу"""
    result = cur.execute('SELECT {0} FROM {1}'.format(name_column, name_table)).fetchall()
    result = list(map(lambda id_group: id_group[0], result))
    # print('new id for group is OK')
    return result


def sql_admin_add_new_student(data, command=True):
    """изменить данные или добавить data - типо словаря из state.proxi(),
    а command=True если нужно добавить нового студента
    command=False если нужно изменить данные студента"""


    # добавить нового студента
    if command:
        cur.execute('INSERT INTO main_data_base(num_student_card, group_{0}) VALUES(?, ?)'.format(data.get('group')[0]),
                    (data.get('num_card_student'), 1))
        base.commit()
        if len(data.get('group')) == 1: return
        for group in data.get('group')[1:]:
            cur.execute(
                'UPDATE main_data_base SET group_{0} == ? WHERE num_student_card == ?'.format(group),
                (1, data.get('num_card_student')))
            base.commit()

    # изменить данные студента
    if not command:
        # изменить данные студентов, нам нужно удалить старые данные
        for group in sql_get_all_groups():
            cur.execute(
                'UPDATE main_data_base SET group_{0} == ? WHERE num_student_card == ?'.format(group['num_group']),
                (0, data.get('num_card_student')))
            base.commit()

        """UPDATE main_data_base SET group_{0} == ? WHERE num_student_card = ?"""
        for group in data.get('group'):
            cur.execute(
                'UPDATE main_data_base SET group_{0} == ? WHERE num_student_card == ?'.format(group),
                (1, data.get('num_card_student')))
            base.commit()



def sql_get_all_groups():
    """получить все группы, которые есть (список словарей где написаны номера групп и их названия)"""
    groups = cur.execute("SELECT * FROM names_groups").fetchall()
    for i, group in enumerate(groups):
        groups[i] = {
            'num_group': group[0],
            'name_group': group[1]
        }
    print(groups)
    return groups


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO info_students VALUES(?, ?)', tuple(data.values()))
        base.commit()
