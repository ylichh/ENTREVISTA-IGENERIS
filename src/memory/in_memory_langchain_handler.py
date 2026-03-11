from src.use_cases.port.memory_handler import MemoryHandler


class InMemoryLangchainHandler(MemoryHandler):

    def __init__(self) -> None:
        self._state: list = []

    def get_state(self) -> list:
        return self._state

    def add(self, message) -> None:
        self._state.append(message)

    def update_state(self, state) -> None:
        self._state = state
