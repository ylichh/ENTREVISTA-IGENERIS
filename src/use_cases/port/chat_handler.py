"""
ChatHandler: puerto abstracto para el manejo de conversaciones con IA.

Implementaciones concretas: LangchainChatHandler, AutogenChatHandler, etc.
"""
from abc import ABC, abstractmethod


class ChatHandler(ABC):

    @abstractmethod
    def handle(self, question: str, history: list) -> str:
        """Envía la pregunta al modelo con el historial y devuelve la respuesta."""
