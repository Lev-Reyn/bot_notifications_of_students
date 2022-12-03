"""для работы с регистрацией и проверкой при каждом сообщении зарегестрирован ли пользователь"""
import json
import os


class Registration:
    """класс для регистрации студента"""

    def __init__(self, data):
        """data - это из 'async with state.proxy() as data:'
        и в ней должно быть первым элементом обязательно номер зачётки, ну и больше ничего"""
        self.num_card_student = tuple(data.values())[0]

    def check_registr(self) -> bool:
        """проверяет, есть ли этот студент в базе данных data_access_open.json (открыт ли ему доступ)"""
        with open('client/registration_of_students/data_access_open.json', 'r') as file:
            self.data_access_open = json.load(file)
        if self.num_card_student in self.data_access_open:
            return True
        return False

    def check_registr_with_answer(self):
        """проверяет, может ли данный студент зарегистрироваться в боте, и даёт ответ в том виде,
         который получит клиент"""
        if self.check_registr():
            return f"Успешно зарегистрирован! \nСтудент {self.data_access_open[self.num_card_student]['name']} " \
                   f"\nНомер зачётки {self.num_card_student}"
        return f"Вы не можете зарегистрироваться в боте, обратитесь к преподавателю"
