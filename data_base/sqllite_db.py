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


def sql_get_one_column(name_table: str, name_column: str) -> list:
    """Принимает имя таблицы и имя столбца, возвращает список со всеми данными в этом столбцу"""
    result = cur.execute('SELECT {0} FROM {1}'.format(name_column, name_table)).fetchall()
    result = list(map(lambda id_group: id_group[0], result))
    # print('new id for group is OK')
    return result


def sql_admin_add_student_in_table_group(data, num_group: int):
    """функция, которая добавляет в таблицу group_ данные о студенте, когда он только регистрируется,
    num_group - номер группы, в которую добавить"""
    print(data.get('num_student_card'))
    id = cur.execute(
        'SELECT id FROM main_data_base WHERE num_student_card == {0}'.format(data.get('num_student_card'))).fetchone()[
        0]

    cur.execute(
        'INSERT INTO group_{0}(id, num_student_card, name_student, Status) VALUES(?, ?, ?, ?)'.format(num_group),
        (id, data.get('num_student_card'), data.get('name_student'), -1))
    base.commit()

    print('данные добавлены', id, data.get('num_student_card'), data.get('name_student'), -1)


def sql_admin_add_student_in_table_group_delete_row(data, num_group: int):
    """удаляет данные об этом студенте в группе (таблице group_)
    data - что-то типо словаря из state.proxy()
    num_group - в какой группе находится этот студент, что бы его от туда удалить
    """
    cur.execute('DELETE FROM group_{0} WHERE num_student_card = ?'.format(num_group), (data.get('num_student_card'),))
    base.commit()


def sql_get_row(table='main_data_base', num_student_card=False, id=False, id_telegram=False):
    """получить строку по одному из параметров из main_data_base"""
    if num_student_card:
        groups = cur.execute(
            'SELECT * FROM {0} WHERE num_student_card == {1}'.format(table, num_student_card)).fetchmany()
    elif id:
        groups = cur.execute(
            'SELECT * FROM {0} WHERE id == {1}'.format(table, id)).fetchmany()
    elif id_telegram:
        groups = cur.execute(
            'SELECT * FROM {0} WHERE id_telegram == {1}'.format(table, id_telegram)).fetchmany()
    else:
        return False
    if len(groups) == 0:
        return False
    return groups


def sql_get_groups_of_student(num_student_card=False, id=False, id_telegram=False) -> list:
    """получить номера групп, в которых находится студент,
    а сделать это можно по любому из параметров"""
    groups = sql_get_row(num_student_card=num_student_card, id=id, id_telegram=id_telegram)

    groups = groups[0][3:]  # берём только столбцы групп
    groups = [i for i in range(len(groups)) if groups[i] == 1]  # получаем список групп, в которых он онаходится
    # print(groups)
    return groups


def sql_admin_add_student_in_table_groups(data, add_or_update=True):
    """
    пока что это функция, которая добавляет новых студентов, в таблицы group_
    add_or_update = True - если нового студента добавляем
    add_or_update = False - если обновить данные по студенту нужно (то есть старую информацию удалить и новую закинуть)
    """
    if not add_or_update:  # если нет, значит это на обновление данных (удаляем старые и добавляем новые)
        groups = sql_get_groups_of_student(num_student_card=data.get('num_student_card'))
        for num_group in groups:
            sql_admin_add_student_in_table_group_delete_row(data=data, num_group=num_group)

    for num_group in data.get('group'):
        sql_admin_add_student_in_table_group(data, num_group=num_group)


def sql_admin_add_new_student(data, command=True):
    """изменить данные или добавить data - типо словаря из state.proxi(),
    а command=True если нужно добавить нового студента
    command=False если нужно изменить данные студента"""

    # добавить нового студента
    if command:
        cur.execute('INSERT INTO main_data_base(num_student_card, group_{0}) VALUES(?, ?)'.format(data.get('group')[0]),
                    (data.get('num_student_card'), 1))
        base.commit()
        if len(data.get('group')) == 1: return
        for group in data.get('group')[1:]:
            cur.execute(
                'UPDATE main_data_base SET group_{0} == ? WHERE num_student_card == ?'.format(group),
                (1, data.get('num_student_card')))
            base.commit()

        sql_admin_add_student_in_table_groups(data=data)  # закидываем данные в таблицы group_
        # нужно обновить таблицу самой группы (групп)

    # изменить данные студента
    if not command:
        # изменить данные студентов, (нам нужно удалить старые данные, а потом закинуть новые туда)
        sql_admin_add_student_in_table_groups(data=data, add_or_update=False)  # в таблицах group_ изменяем данные
        for group in sql_get_all_groups():
            cur.execute(
                'UPDATE main_data_base SET group_{0} == ? WHERE num_student_card == ?'.format(group['num_group']),
                (0, data.get('num_student_card')))
            base.commit()

        """UPDATE main_data_base SET group_{0} == ? WHERE num_student_card = ?"""
        for group in data.get('group'):
            cur.execute(
                'UPDATE main_data_base SET group_{0} == ? WHERE num_student_card == ?'.format(group),
                (1, data.get('num_student_card')))
            base.commit()


def sql_get_all_groups():
    """получить все группы, которые есть (список словарей где написаны номера групп и их названия)"""
    groups = cur.execute("SELECT * FROM names_groups").fetchall()
    for i, group in enumerate(groups):
        groups[i] = {
            'num_group': group[0],
            'name_group': group[1]
        }
    # print(groups)
    return groups


def sql_update_row(data: dict):
    """
    data: dict - принимает словарь в качкстве аргумента, с такой структурой ↓
    data['name_table']: str - название таблицы, где нужно изменить данные
    data['column_primary']: str - название столбца, по которому искать строку, где изменить значения
    data['primary_value']: str - то значение, по которому искать строку
    data['columns']: dict['name_column'] = 'value' - ключи - это название столбцов, где изменить инфу, а их значения,
    это на что изменить
    """
    set_string = 'SET '
    count = 0
    for name_column, value in data['columns'].items():
        count += 1
        if len(data['columns']) == count:
            set_string += f'{name_column} == {value} '
        else:
            set_string += f'{name_column} == {value}, '
    # print(set_string)

    update = f'UPDATE {data["name_table"]} {set_string} WHERE {data["column_primary"]} = {data["primary_value"]}'
    print(update)
    cur.execute(update)
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO info_students VALUES(?, ?)', tuple(data.values()))
        base.commit()
