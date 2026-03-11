
import uuid

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from src.use_cases.port.add_use_case import AddUseCase
from src.use_cases.port.analysis_use_case import AnalysisUseCase


class QuestionRequest(BaseModel):
    question: str
    conversation_id: str


class AddRequest(BaseModel):
    analysis: str
    conversation_id: str


class ConversationResponse(BaseModel):
    conversation_id: str


class AnalysisResponse(BaseModel):
    analysis: str


class AddResponse(BaseModel):
    image_url: str


class AnalysisController:

    def __init__(self, use_case: AnalysisUseCase, add_use_case: AddUseCase) -> None:
        self._use_case = use_case
        self._add_use_case = add_use_case
        self._app = FastAPI()
        self._register_routes()

    def _register_routes(self) -> None:
        @self._app.post("/conversation")
        def new_conversation() -> ConversationResponse:
            return ConversationResponse(conversation_id=str(uuid.uuid4()))

        @self._app.post("/analyze")
        def analyze(request: QuestionRequest) -> AnalysisResponse:
            response = self._use_case.execute(request.question, request.conversation_id)
            return AnalysisResponse(analysis=response)

        @self._app.post("/generate_add")
        def generate_add(request: AddRequest) -> AddResponse:
            image_url = self._add_use_case.generate(request.analysis, request.conversation_id)
            return AddResponse(image_url=image_url)

    def run(self, host: str, port: int) -> None:
        uvicorn.run(self._app, host=host, port=port)