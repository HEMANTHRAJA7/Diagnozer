"""
In-memory mock database for local development.
Replaces Motor/MongoDB with simple Python dicts.
Swap back to mongodb.py when connecting to Atlas.
"""
from datetime import datetime

# In-memory collections
_store = {
    "users": [],
    "history": [],
    "chats": [],
}

class MockCollection:
    def __init__(self, name):
        self.name = name
    
    async def find_one(self, query, sort=None):
        items = _store[self.name]
        # Filter
        matches = []
        for item in items:
            match = all(item.get(k) == v for k, v in query.items())
            if match:
                matches.append(item)
        if not matches:
            return None
        if sort:
            key, direction = sort[0]
            matches.sort(key=lambda x: x.get(key, datetime.min), reverse=(direction == -1))
        return matches[0]
    
    async def insert_one(self, doc):
        doc = dict(doc)
        doc["_id"] = f"mock_{self.name}_{len(_store[self.name]) + 1}"
        _store[self.name].append(doc)
        
        class Result:
            inserted_id = doc["_id"]
        return Result()

class MockDB:
    def __getitem__(self, collection_name):
        if collection_name not in _store:
            _store[collection_name] = []
        return MockCollection(collection_name)

_mock_db = MockDB()

async def get_database():
    return _mock_db

async def connect_to_mongo():
    print("Using IN-MEMORY mock database (no MongoDB required)")

async def close_mongo_connection():
    print("Mock database cleared.")
