from pymongo import MongoClient, ASCENDING
from typing import List, Tuple
import os

class RecordsDB:
    def __init__(self, mongo_uri=None, db_name='records_db'):
        mongo_uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=200)
            self.db = self.client[db_name]
            self.collection = self.db['leaderboard']
            self._init_db()
        except Exception as e:
            print("Ошибка соединения с MongoDB:", e)
            raise

    def _init_db(self):
        self.collection.create_index([('time_seconds', ASCENDING)])

    def add_record(self, name: str, time: float):
        self.collection.insert_one({
            'player_name': name,
            'time_seconds': time
        })

    def get_top(self, limit=10) -> List[Tuple[str, float]]:
        results = self.collection.find({}, {'_id': 0, 'player_name': 1, 'time_seconds': 1}) \
                                .sort('time_seconds', ASCENDING) \
                                .limit(limit)
        return [(doc['player_name'], doc['time_seconds']) for doc in results]

    def close(self):
        self.client.close()