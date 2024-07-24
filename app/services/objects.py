class User():
    def __init__(self,
                 id,
                 username,
                 creation_time,
                 last_updated,
                 game_ids=[]):
        self.id = id
        self.username = username
        self.creation_time = creation_time 
        self.last_updated = last_updated
        self.game_ids = game_ids

    def to_dict(self):
        return {"id": self.id,
                "username": self.username,
                "creation_time": self.creation_time,
                "last_updated": self.last_updated,
                "game_ids": self.game_ids}

    @staticmethod
    def from_dict(source):
        return User(**source)


class GameSaveData():
    def __init__(self, id, user_id, title, 
                 creation_time, last_updated, 
                 days_left=80, journey_path=["London"]):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.creation_time = creation_time 
        self.last_updated = last_updated
        self.days_left = days_left
        self.journey_path = journey_path

    def to_dict(self):
        return {"game_id": self.id,
                "user_id": self.user_id,
                "title": self.title,
                "creation_time": self.creation_time,
                "last_updated": self.last_updated,
                "days_left": self.days_left,
                "journey_path": self.journey_path}

    @staticmethod
    def from_dict(source):
        return GameSaveData(**source)