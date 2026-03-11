"""
AnalysisLangchainHandler: implementación de ChatHandler usando LangChain.

Mantiene el historial de la conversación. El caso de uso es responsable
de inyectar y persistir la lista de mensajes entre turnos.

Prompt análogo al de analysis_team.py (AutoGen).
"""
import os

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from src.use_cases.port.chat_handler import ChatHandler

SYSTEM_PROMPT = """
Eres un analista senior de demanda turística para una empresa europea de experiencias de viaje.

Usa las tools disponibles para recopilar datos reales antes de producir el análisis.
No inventes ni asumas información: si no tienes el dato, llama a la tool correspondiente.

Produce una recomendación clara y accionable sobre qué experiencia promocionar, para qué tipo de cliente y por qué.
"""


class AnalysisLangchainHandler(ChatHandler):

    def __init__(self, tools: list) -> None:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        self._agent = create_agent(
            model=llm,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def handle(self, user_input: str, state: list[BaseMessage]) -> tuple[str, list[BaseMessage]]:
        result = self._agent.invoke({"messages": [*state, HumanMessage(content=user_input)]})
        new_state = result["messages"]
        return new_state[-1].content, new_state
