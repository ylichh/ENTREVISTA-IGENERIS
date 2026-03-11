"""
AnalysisTeam: construye el RoundRobinGroupChat de análisis turístico.

Recibe las tools inyectadas desde el Composition Root.
"""
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

SYSTEM_MESSAGE = """
Eres un analista senior de demanda turística para una empresa europea de experiencias de viaje.

Usa las tools disponibles para recopilar datos reales antes de producir el análisis.
No inventes ni asumas información: si no tienes el dato, llama a la tool correspondiente.

Produce una recomendación clara y accionable sobre qué experiencia promocionar, para qué tipo de cliente y por qué.
Termina con TERMINATE.
"""

TASK_TEMPLATE = """
¿A quién podría vender experiencias turísticas en {destination}?
Usa las tools disponibles para identificar los mercados de origen con mayor interés y elabora una recomendación accionable.
Dime que paises están buscando sobre andalucia y ademas en que regiones se estan buscnado.
"""


class AnalysisTeam:

    def __init__(self, tools: list) -> None:
        self._tools = tools

    def build(self) -> RoundRobinGroupChat:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        agent = AssistantAgent(
            name="tourism_analyst",
            model_client=model_client,
            tools=self._tools,
            system_message=SYSTEM_MESSAGE,
            reflect_on_tool_use=True,
        )
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(max_messages=15)
        return RoundRobinGroupChat([agent], termination_condition=termination)
