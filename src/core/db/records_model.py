from .database import RecordsDB

class RecordsModel:
    def __init__(self, mongo_uri=None):
        self.db = RecordsDB(mongo_uri=mongo_uri)

    def save(self, name: str, time: float):
        self.db.add_record(name, time)

    def load(self) -> list:
        return self.db.get_top()

    def clear(self):
        self.db.clear_collection()

    def cleanup(self):
        self.db.close()