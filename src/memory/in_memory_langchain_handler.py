from src.use_cases.port.memory_handler import MemoryHandler


class InMemoryLangchainHandler(MemoryHandler):

    def __init__(self) -> None:
        self._state: dict[str, list] = {}

    def get_state(self, conversation_id: str) -> list:
        return self._state.get(conversation_id, [])

    def add(self, message) -> None:
        raise NotImplementedError("LangChain usa update_state() para persistir el estado completo.")

    def update_state(self, conversation_id: str, state) -> None:
        self._state[conversation_id] = state
