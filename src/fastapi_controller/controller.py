
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from src.use_cases.port.analysis_use_case import AnalysisUseCase


class QuestionRequest(BaseModel):
    question: str


class AnalysisController:

    def __init__(self, use_case: AnalysisUseCase) -> None:
        self._use_case = use_case
        self._app = FastAPI()
        self._register_routes()

    def _register_routes(self) -> None:
        @self._app.post("/analyze")
        def analyze(request: QuestionRequest) -> dict:
            response = self._use_case.execute(request.question)
            return {"response": response}

    def run(self, host: str, port: int) -> None:
        uvicorn.run(self._app, host=host, port=port)