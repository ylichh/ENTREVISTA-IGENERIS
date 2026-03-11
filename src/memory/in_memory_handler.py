from src.use_cases.port.memory_handler import MemoryHandler


class InMemoryHandler(MemoryHandler):

    def __init__(self) -> None:
        self._history: list = []

    def get_history(self) -> list:
        return self._history

    def add(self, message) -> None:
        self._history.append(message)
