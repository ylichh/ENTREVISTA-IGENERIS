"""
reviewer_node: nodo LLM que evalúa la recommendation del analyst.

Valida que la respuesta tenga las dos secciones obligatorias:
  - **Analisis en base a datos:** datos crudos de tools, sin interpretación
  - **Recomendación Experto:** interpretación y expertise del modelo

El routing (analyst | __end__) lo gestiona el grafo via conditional_edge.
"""
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.langgraph.state.analysis_state import AnalysisState

MAX_REVIEWS = 5

REVIEWER_PROMPT = """
Eres un revisor de calidad de análisis turístico.

Tu tarea es revisar que la respuesta del analista sigue la estructura obligatoria:
  1. **Analisis en base a datos:** solo datos obtenidos de herramientas, sin interpretación ni conclusiones.
  2. **Recomendación Experto:** interpretación, conclusiones y recomendación accionable basada en expertise.

Si la respuesta contiene ambas secciones y cada una cumple su función, responde EXACTAMENTE: APPROVED
Si falta alguna sección o están mezcladas, responde REJECTED: <motivo concreto>
"""


def make_reviewer_node():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ["OPENAI_API_KEY"],
    )

    def reviewer_node(state: AnalysisState) -> dict:
        review_count = state.get("review_count", 0)

        messages = [
            SystemMessage(content=REVIEWER_PROMPT),
            HumanMessage(content=state["recommendation"]),
        ]
        response = llm.invoke(messages)
        content = response.content.strip()

        approved = content.startswith("APPROVED") or review_count >= MAX_REVIEWS - 1

        return {
            "messages": [response],
            "review_approved": approved,
            "review_count": review_count + 1,
        }

    return reviewer_node
