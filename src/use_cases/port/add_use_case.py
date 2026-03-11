from abc import ABC, abstractmethod


class AddUseCase(ABC):

    @abstractmethod
    def generate(self, analysis: str, conversation_id: str) -> str:
        """Genera una imagen publicitaria a partir del análisis. Devuelve URL."""
