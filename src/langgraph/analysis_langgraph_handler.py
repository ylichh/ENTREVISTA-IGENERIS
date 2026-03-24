"""
AnalysisLangGraphHandler: implementación de ChatHandler usando LangGraph.

Traduce entre el contrato del dominio (list[BaseMessage])
y el estado interno del grafo (AnalysisState).
La persistencia de mensajes es responsabilidad del MemoryHandler externo.
"""
from langchain_core.messages import BaseMessage, HumanMessage

from src.use_cases.port.chat_handler import ChatHandler
from src.langgraph.graphs.analysis_graph import build_analysis_graph


class AnalysisLangGraphHandler(ChatHandler):

    def __init__(self, tools: list) -> None:
        self._app = build_analysis_graph(tools)

    def handle(self, user_input: str, state: list[BaseMessage]) -> tuple[str, list[BaseMessage]]:
        result = self._app.invoke({
            "messages": [*state, HumanMessage(content=user_input)],
            "recommendation": "",
            "review_approved": False,
            "review_count": 0,
        })
        return result["recommendation"], result["messages"]
