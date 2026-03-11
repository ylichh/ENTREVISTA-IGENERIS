"""
MemoryHandler: puerto abstracto para recuperar el historial de conversación.

Implementaciones concretas gestionarán la persistencia (in-memory, Redis, BD, etc.).
"""
from abc import ABC, abstractmethod


class MemoryHandler(ABC):

    @abstractmethod
    def get_state(self, conversation_id: str):
        """Devuelve el estado de la conversación identificada por conversation_id."""

    @abstractmethod
    def add(self, message) -> None:
        """Añade un mensaje al historial."""

    @abstractmethod
    def update_state(self, conversation_id: str, state) -> None:
        """Reemplaza el estado completo de la conversación identificada por conversation_id."""
