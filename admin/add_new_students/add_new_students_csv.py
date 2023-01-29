from admin.add_new_students.add_new_students import AddNewStudent
from data_base.in_csv import InCsv
from ast import literal_eval


class AddNewStudentsCsv:
    def add_new_students_csv(self):
        """
        always takes data from the file data_base/data/add_new_students.csv
        :return:
        """
        csvfile_injson = InCsv(name_file='data_base/data/add_new_students.csv', fieldnames=['id', 'num_student_card',
                                                                                            'name_student', 'group'],
                               delimiter=';')
        for i, student_row in enumerate(csvfile_injson.read()):
            print(student_row)
            student_row['group'] = literal_eval(student_row['group'])
            print(student_row)
            if AddNewStudent(data=student_row).add_new_student():
                print('OK', i)

            else:
                print('hell________', i)
        return True
