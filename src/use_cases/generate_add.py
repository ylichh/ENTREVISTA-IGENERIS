from src.use_cases.port.add_use_case import AddUseCase
from src.use_cases.port.chat_handler import ChatHandler


class GenerateAdd(AddUseCase):

    def __init__(self, chat_handler: ChatHandler) -> None:
        self._chat_handler = chat_handler

    def generate(self, analysis: str, conversation_id: str) -> str:
        image_url, _ = self._chat_handler.handle(analysis, {})
        return image_url
