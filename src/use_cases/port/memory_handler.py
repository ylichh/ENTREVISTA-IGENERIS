"""
MemoryHandler: puerto abstracto para recuperar el historial de conversación.

Implementaciones concretas gestionarán la persistencia (in-memory, Redis, BD, etc.).
"""
from abc import ABC, abstractmethod


class MemoryHandler(ABC):

    @abstractmethod
    def get_state(self):
        """Devuelve el estado de la conversación (formato dependiente del framework)."""

    @abstractmethod
    def add(self, message) -> None:
        """Añade un mensaje al historial."""

    @abstractmethod
    def update_state(self, state) -> None:
        """Reemplaza el estado completo de la conversación."""
