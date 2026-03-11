"""
ChatHandler: puerto abstracto para el manejo de conversaciones con IA.

Implementaciones concretas: LangchainChatHandler, AutogenChatHandler, etc.
"""
from abc import ABC, abstractmethod


class ChatHandler(ABC):

    @abstractmethod
    def handle(self, question: str, state) -> tuple[str, any]:
        """Envía la pregunta al modelo con el estado y devuelve (respuesta, nuevo_estado)."""
