import pytest
from mongomock import MongoClient
from src.core.db.database import RecordsDB

class MockRecordsDB(RecordsDB):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['test_db']
        self.collection = self.db['leaderboard']
        self._init_db()

def test_add_and_get_top():
    db = MockRecordsDB()
    db.add_record("Alice", 12.3)
    db.add_record("Bob", 10.1)
    db.add_record("Eve", 15.0)
    top = db.get_top(2)
    assert top == [("Bob", 10.1), ("Alice", 12.3)]
    db.close()