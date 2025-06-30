from pymongo import MongoClient, ASCENDING
from typing import List, Tuple
import os

class RecordsDB:
    def __init__(self, mongo_uri=None, db_name='records_db'):
        mongo_uri = mongo_uri or os.getenv("MONGO_URI", "mongodb://localhost:27017")
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.collection = self.db['leaderboard']
            self._init_db()
            print("Успешное соединение с MongoDB")
        except Exception as e:
            print("Ошибка соединения с MongoDB:", e)
            raise

    def _init_db(self):
        try:
            self.collection.create_index(
                [('player_name', ASCENDING)],
                unique=True,
                name="unique_player_name"
            )
            print("Создан уникальный индекс по player_name")
        except Exception as e:
            print("Ошибка создания индекса:", e)

        self.collection.create_index([('time_seconds', ASCENDING)])

    def add_record(self, name: str, time: float):
        try:
            result = self.collection.update_one(
                {'player_name': name},
                {'$min': {'time_seconds': time}},
                upsert=True
            )

            if result.upserted_id:
                print(f"Добавлен новый игрок: {name} со временем {time}")
            elif result.modified_count > 0:
                print(f"Обновлен рекорд для {name}: новое время {time}")
            else:
                print(f"Рекорд {name} не нуждается в обновлении (текущий лучше)")
            return True
        except Exception as e:
            print(f"Ошибка при добавлении записи {name}: {e}")
            return False

    def get_top(self, limit=10) -> List[Tuple[str, float]]:
        try:
            cursor = self.collection.find(
                {},
                {'_id': 0, 'player_name': 1, 'time_seconds': 1}
            ).sort('time_seconds', ASCENDING).limit(limit)

            results = []
            for doc in cursor:
                results.append((doc['player_name'], doc['time_seconds']))

            print(f"Получено топ-{len(results)} записей")
            return results
        except Exception as e:
            print("Ошибка при получении топа:", e)
            return []

    def clear_collection(self):
        try:
            result = self.collection.delete_many({})
            print(f"Очищено {result.deleted_count} записей")
            return result.deleted_count
        except Exception as e:
            print("Ошибка при очистке коллекции:", e)
            return 0

    def close(self):
        try:
            self.client.close()
            print("Соединение с MongoDB закрыто")
        except:
            pass