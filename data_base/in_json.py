import json
import os.path
import csv
import zipfile


# class InJsonReadCreate:
#     """класс чтения или создавать с пустым словарём или списком и создания, если такого файла нет, а то что нам читать,
#      который будут наследовать классы InJson"""
#
#     def __init__(self, name_file: str, is_lst=True):
#         """name_file - название файла, проверяет, если такого файла нет, то создаёт
#         is_lst необходим только для того, что бы понимать, закидывать список в json или словарь"""
#         self.name_file = name_file
#         if not os.path.exists(self.name_file):
#             lst = []
#             print(is_lst)
#             if is_lst == False:
#                 lst = {}
#             with open(self.name_file, 'w') as file:
#                 json.dump(lst, file, indent=4, ensure_ascii=False)
#
#     def reed_json(self):
#         """считывает данные из файлика
#         можно в принципе посмотреть что в файлике через атрибут lst_paste,
#         но если хотим обновить данные, то используем метод"""
#         with open(self.name_file, 'r') as file:
#             self.lst_paste = json.load(file)
#         return self.lst_paste
#
#     def update_number_page(self, number_page: int):
#         with open('number_page.txt', 'w') as file:
#             file.write(str(number_page))


class InJson:
    # def __init__(self, name_file):
    #     print('InJon')
    #     super().__init__(name_file)

    def __init__(self, name_file: str, is_lst=True):
        """name_file - название файла, проверяет, если такого файла нет, то создаёт"""
        self.name_file = name_file
        if not os.path.exists(self.name_file):
            lst = []
            print(is_lst)
            if is_lst == False:
                lst = {}
            with open(self.name_file, 'w') as file:
                json.dump(lst, file, indent=4, ensure_ascii=False)

    def write_list(self, lst: list):
        """перезаписывает данные в json файл self.name_file
            args:
                lst - список, который закинуть в json файл self.name_file"""
        with open(self.name_file, 'w') as file:
            json.dump(lst, file, indent=4, ensure_ascii=False)

    def update_list(self, lst: list):
        """добавляет сожержимое lst в содержимое json файлика (а внутри него список должен быть)"""
        with open(self.name_file, 'r') as file:
            self.lst_past = json.load(file)
        self.lst_past += lst
        with open(self.name_file, 'w') as file:
            json.dump(self.lst_past, file, indent=4, ensure_ascii=False)

    def reed_json(self):
        """считывает данные из файлика
        можно в принципе посмотреть что в файлике через атрибут lst_paste,
        но если хотим обновить данные, то используем метод"""
        with open(self.name_file, 'r') as file:
            self.lst_paste = json.load(file)
        return self.lst_paste

    def json_lst_in_csv(self, name_csv_file: str, name_column: str):
        """json файл со структурой список строк/чисел и закидывает в json, где столбцы: номел элемента и сам элемент
            args:
                name_csv_file - название файла для csv файла
                name_column - названия для столбца с элментами списка
        """
        data_lst = self.reed_json()
        with open(name_csv_file, 'w') as file:
            fieldnames = ['№', name_column]
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for i, elem in enumerate(data_lst):
                writer.writerow({
                    '№': i,
                    name_column: elem
                })

    def update_number_page(self, number_page: int):
        with open('number_page.txt', 'w') as file:
            file.write(str(number_page))


class InJsonDict:
    """класс для того, что бы создавать json файлы со структурой словарей """

    def __init__(self, name_file: str):
        """name_file - название файла, проверяет, если такого файла нет, то создаёт"""
        self.name_file = name_file
        if not os.path.exists(self.name_file):
            dict_data = {}
            with open(self.name_file, 'w') as file:
                json.dump(dict_data, file, indent=4, ensure_ascii=False)

    def update_dict(self, dict_for_add):
        """добавляет (обновляет) json.  в словарь добавляются новые ключи и значения другого словаря
         параметры:
            dict_for_add - словарь, который добавить

        если в словарях есть одинаковые ключи, то данные заменяются на те, которые в dict_for_add
        """
        with open(self.name_file, 'r') as file:
            self.dict_past = json.load(file)
        self.dict_past: dict
        self.dict_past = self.dict_past | dict_for_add
        with open(self.name_file, 'w') as file:
            json.dump(self.dict_past, file, indent=4, ensure_ascii=False)

    def write_dict(self, dictionary: dict):
        """перезаписать данные словаря
            args:
                dictionary - словарь, который нужно закинуть в self.name_file
        """
        if not isinstance(dictionary, dict):
            raise ValueError('The dictionary must be of the dict type')
        with open(self.name_file, 'w') as file:
            json.dump(dictionary, file, indent=4, ensure_ascii=False)

    def reed_json(self):
        """считывает данные из файлика
        можно в принципе посмотреть что в файлике через атрибут self.dict_paste,
        но если хотим обновить данные, то используем метод"""
        with open(self.name_file, 'r') as file:
            self.dict_paste = json.load(file)
        return self.dict_paste

    def json_in_csv(self, name_csv_file: str, key_one: str):
        """переделывает json в csv
            параметры:
                name_csv_file - имя файла, в который созранить данные
                key_one - ключ одного словаря, так как нужно понимать какие столбцы делать
                """
        data_dict = self.reed_json()
        data_dict: dict
        with open(name_csv_file, 'w') as csvfile:
            fieldnames = [str(key) for key in data_dict[key_one]]
            writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
            writer.writeheader()
            for user in data_dict.values():
                writer.writerow(user)

    def update_number_page(self, number_page: int):
        with open('number_page.txt', 'w') as file:
            file.write(str(number_page))

    # доработать


class InZIP:
    """класс для работы с zip архивами (дорабатывать ещё можно, а то пока что только закидывать в архив может"""

    def __init__(self, name_zip):
        self.name_zip = name_zip

    def create_zip(self, directory: str):
        """метода закидывает файлы в архив"""
        self.directory = directory
        self.files_in_directory = os.listdir(directory)
        archive = zipfile.ZipFile(self.name_zip, mode='w')
        try:
            for i, file in enumerate(self.files_in_directory):
                archive.write(f'{self.directory}/{file}')
                print(f'Files added. {i + 1}')
        finally:
            print('Reading files now.')
            archive.close()


if __name__ == '__main__':
    os.chdir('../')  # поставить основную директорию другую (в данном случа я поставил bot_predictions

    InZIP('data_users.zip').create_zip(directory='data_users')
