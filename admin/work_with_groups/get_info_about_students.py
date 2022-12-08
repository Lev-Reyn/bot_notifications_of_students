from data_base.sqllite_db import sql_get_one_column, sql_get_row, sql_get_groups_of_student
from data_base.in_csv import InCsv


class GetInfoAboutStudents:
    # def __init__(self):

    def get_small_info(self):
        """получить инфу о студентах в csv файле: id, id_telegram, num_student_card, name_student, Status, all_groups
        именно создаёт csv файл data_base/data/small_info.csv"""
        self.status = {
            1: 'activ',
            0: 'blocked',
            -1: 'no activated'
        }

        all_id_students = sql_get_one_column(name_table='main_data_base', name_column='id')  # id всех студентов
        print(all_id_students)
        # дальше пробежимся по всем студентам, и соберём инфу по ним из базы данных
        data = []
        self.count_students_dict = {
            'count_student': len(all_id_students),
            'activ': 0,
            'blocked': 0,
            'no activated': 0
        }
        for id_student in all_id_students:
            groups = sql_get_groups_of_student(id=id_student)  # узнаём в каких группах находится студент
            info_about_alone_student = sql_get_row(table=f'group_{groups[0]}', id=id_student)[0][0:5]
            # считаем сколько студентов зарегистрировались в боте (active), сколько заблокировали бота (blocked),
            # и сколько не активировали бота (no activated)
            self.count_students_dict[self.status.get(info_about_alone_student[4])] += 1
            data_dict_alone_student = {
                'id': id_student,
                'num_student_card': info_about_alone_student[1],
                'name_student': info_about_alone_student[2],
                'id_telegram': info_about_alone_student[3],
                'Status': self.status.get(info_about_alone_student[4]),
                'groups': groups
            }
            data.append(data_dict_alone_student)
            # print(id_student, groups, info_about_alone_student)
            print(data_dict_alone_student)
        InCsv(name_file='data_base/data/small_info.csv',
              fieldnames=['id', 'num_student_card', 'name_student', 'id_telegram', 'Status', 'groups']).write(data)

    def get_small_info_with_answer(self):
        """получить инфу о студентах в csv файле: id, id_telegram, num_student_card, name_student, Status, all_groups
        создаёт csv файл data_base/data/small_info.csv
        и возвращает сообщение, что данные собраны и о скольких пользователях
        """
        self.get_small_info()
        return f'\n' \
               f'В базе находится <b>{self.count_students_dict["count_student"]} студентов</b>\n' \
               f'\n' \
               f'✅ из них <b>зарегистрировались {self.count_students_dict["activ"]}\n' \
               f'\n' \
               f'🟨 не зарегистрировались {self.count_students_dict["no activated"]}</b>\n' \
               f'\n' \
               f'❌ заблокировали {self.count_students_dict["blocked"]}\n'
