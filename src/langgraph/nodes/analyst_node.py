"""
analyst_node: nodo LLM con tools de Google Trends.

Recibe la pregunta del usuario, llama a las tools necesarias
y escribe la recommendation en el estado.
"""
import os

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode

from src.langgraph.state.analysis_state import AnalysisState

ANALYST_PROMPT = """
Eres un analista senior de demanda turística para una empresa europea de experiencias de viaje.

Usa las tools disponibles para recopilar datos reales antes de producir el análisis.
No inventes ni asumas información: si no tienes el dato, llama a la tool correspondiente.

Produce una recomendación clara y accionable sobre qué experiencia promocionar,
para qué tipo de cliente y por qué.
"""


def make_analyst_node(tools: list):
    """
    Factory que devuelve el nodo analyst y su tool_node asociado.
    Recibe las tools ya instanciadas desde el Composition Root.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
    ).bind_tools(tools)

    def analyst_node(state: AnalysisState) -> dict:
        messages = [SystemMessage(content=ANALYST_PROMPT)] + state["messages"]
        response = llm.invoke(messages)
        return {
            "messages": [response],
            "recommendation": response.content if not response.tool_calls else "",
        }

    tool_node = ToolNode(tools)

    return analyst_node, tool_node
