from data_base.in_json import InJson


class Moderator:
    def update_moderator(self, id_telegram):
        """изменить модератора (админа)"""
        self.ID_MODERATOR = id_telegram
        file = InJson('data_base/moderator.json')
        file.write_list([self.ID_MODERATOR])

    def check_moderator(self, id_telegram):
        """провека на модератора (админа), если чел админ, то True, иначе False"""
        file = InJson('data_base/moderator.json')
        self.ID_MODERATOR = file.reed_json()[0]
        if id_telegram == self.ID_MODERATOR:
            return True
        else:
            return False

    def get_moderator_id(self):
        file = InJson('data_base/moderator.json')
        return file.reed_json()[0]
