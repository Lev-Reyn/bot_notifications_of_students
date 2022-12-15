from aiogram import types
from data_base.sqllite_db import sql_get_groups_of_student, sql_update_row
import datetime


class YesNoOther:
    def answer(self, callback_query: types.CallbackQuery, other_answer: str = False):
        """работает только на такие ответы как Да и Нет от студентов"""
        self.callback_query = callback_query
        self.message_for_student = ''
        button_touch = callback_query.data.replace('yes_no_other_', '')
        # ну и тут надо будет добавлять в базу данных
        self.data = self.scrap(callback_data=button_touch)  # инфа о том на какой вопрос это ответ
        if 'no' in button_touch:
            self.write_answer_in_data(answer='no')
            self.message_for_student += f'Ответ <b>нет</b> учтён на вопрос ' \
                                        f'<b>{callback_query.message.text}</b> {self.data}'
        elif 'yes' in button_touch:
            self.write_answer_in_data(answer='yes')
            self.message_for_student += f'Ответ <b>Да</b> учтён на вопрос ' \
                                        f'<b>{callback_query.message.text}</b> {self.data}'
        elif 'other' in button_touch:
            self.write_answer_in_data(answer=other_answer)

            self.message_for_student += f'Ответ <b>{other_answer}</b> учтён на вопрос ' \
                                        f'<b>{callback_query.message.text}</b> {self.data}'
        return self.message_for_student

    def write_answer_in_data(self, answer: str):
        """метод закидывает ответ студента в базу данных"""
        print(self.callback_query.from_user.id)
        groups = sql_get_groups_of_student(id_telegram=self.callback_query.from_user.id)
        groups_for_question = []  # здесь группы в которых состоит студент и в какие группы отправлялось (одновременно)
        for group in self.data['groups']:
            if group in groups:
                groups_for_question.append(group)
        for group in groups_for_question:
            data = {
                'name_table': f'group_{group}',
                'column_primary': 'id_telegram',
                'primary_value': self.callback_query.from_user.id,
                'columns': {
                    f'answer_{self.data["all_info"][group]}': f"'{answer}'",
                    f'datetime_{self.data["all_info"][group]}': f"'{datetime.datetime.now()}'"
                }
            }
            sql_update_row(data)

        # pass

    def scrap(self, callback_data: str) -> dict:
        """распарсит callback, что бы понять для какой группы был вопрос и номера вопросов
        принимает такой формат строки yes_group_0_1_4<>question_13_17_9"""
        callback_data = callback_data.replace('yes_', '').replace('no_', '').replace('other_', '')
        groups = [int(i) for i in callback_data.split('<>')[0].replace('group_', '').split('_')]  # группы
        questions = [int(i) for i in callback_data.split('<>')[1].replace('question_', '').split('_')]  # группы
        data = {'all_info': {}}
        for i, group in enumerate(groups):
            data['all_info'][group] = questions[i]
        data = data | {'groups': groups, 'questions': questions}
        return data
