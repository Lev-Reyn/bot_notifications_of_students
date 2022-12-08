import csv
import os


class InCsv:
    def __init__(self, name_file: str, fieldnames: list):
        """
        создаётся csv файл если такого нет, или открывается тот, который есть уже
        name_file - название файла, проверяет, если такого файла нет, то создаёт,
        fieldnames - список с названиями столбцов
        """
        self.name_file = name_file
        self.fieldnames = fieldnames
        if not os.path.exists(self.name_file):
            with open(self.name_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def write(self, lst: list):
        """перезаписывает данные в csv файл self.name_file
            args:
                lst - список, который закинуть в json файл self.name_file
                lst: dict[name_column] = value_for_that_column
                """
        with open(self.name_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in lst:
                writer.writerow(row)

    def read(self) -> list:
        self.lst_past = []
        with open(self.name_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.lst_past.append(row)
        return self.lst_past

    def update_list(self, lst: list):
        """добавляет сожержимое lst в содержимое csv файла (а внутри него словарь со структурой:
        lst: dict[name_column] = value_for_that_column)"""
        self.read()
        self.lst_past += lst
        self.write(self.lst_past)



# test = InCsv(name_file='test.csv', fieldnames=['Имена пидоров', 'Любимая игра', 'Имя его парня', 'имя отца'])
# data = [
#     {
#         'Имена пидоров': "Илья",
#         "Любимая игра": 'NFS',
#         'Имя его парня': "Мухамед",
#         "имя отца": "Иван"
#     },
#     {
#         'Имена пидоров': "Игорь",
#         "Любимая игра": 'ГТА 5',
#         'Имя его парня': "Рамзен",
#         "имя отца": "Виктор"
#     },
#
# ]
# test.write(lst=data)
