"""
IterateAnalysis: caso de uso que itera sobre una pregunta del usuario
delegando la conversación al ChatHandler inyectado.
"""
from src.use_cases.port.analysis_use_case import AnalysisUseCase
from src.use_cases.port.chat_handler import ChatHandler
from src.use_cases.port.memory_handler import MemoryHandler


class IterateAnalysis(AnalysisUseCase):

    def __init__(self, chat_handler: ChatHandler, memory_handler: MemoryHandler) -> None:
        self._chat_handler = chat_handler
        self._memory_handler = memory_handler

    def execute(self, question: str) -> str:
        state = self._memory_handler.get_state()
        response, new_state = self._chat_handler.handle(question, state)
        self._memory_handler.update_state(new_state)
        return response
