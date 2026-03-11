"""
MemoryHandler: puerto abstracto para recuperar el historial de conversación.

Implementaciones concretas gestionarán la persistencia (in-memory, Redis, BD, etc.).
"""
from abc import ABC, abstractmethod


class MemoryHandler(ABC):

    @abstractmethod
    def get_history(self) -> list:
        """Devuelve el historial de mensajes de la conversación."""

    @abstractmethod
    def add(self, message) -> None:
        """Añade un mensaje al historial."""
