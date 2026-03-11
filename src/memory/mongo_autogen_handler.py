from pymongo import MongoClient

from src.use_cases.port.memory_handler import MemoryHandler

COLLECTION = "conversacion"


class MongoAutogenHandler(MemoryHandler):

    def __init__(self, uri: str, db_name: str) -> None:
        self._collection = MongoClient(uri)[db_name][COLLECTION]

    def get_state(self, conversation_id: str):
        doc = self._collection.find_one({"_id": conversation_id})
        return doc["state"] if doc else None

    def update_state(self, conversation_id: str, state) -> None:
        self._collection.replace_one(
            {"_id": conversation_id},
            {"_id": conversation_id, "state": state},
            upsert=True,
        )

    def add(self, message) -> None:
        raise NotImplementedError("Mongo usa update_state() para persistir el estado completo.")
