from abc import ABC, abstractmethod


class AnalysisUseCase(ABC):

    @abstractmethod
    def execute(self, question: str, conversation_id: str) -> str:
        """Procesa la pregunta del usuario y devuelve la respuesta del análisis."""