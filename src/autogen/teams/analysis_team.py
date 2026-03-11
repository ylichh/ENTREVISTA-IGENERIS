"""
AnalysisTeam: construye el RoundRobinGroupChat de análisis turístico.

Recibe las tools inyectadas desde el Composition Root.
"""
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

TOURISM_EXPERT_SYSTEM_MESSAGE = """
Eres un analista senior de demanda turística para una empresa europea de experiencias de viaje.

Usa las tools disponibles para recopilar datos reales antes de producir el análisis.
No inventes ni asumas información: si no tienes el dato, llama a la tool correspondiente.

Produce una recomendación clara sobre qué experiencia promocionar, para qué tipo de cliente y por qué.
La estructura de tu respuesta debe ser:
**Analisis en base a  datos:
Aqui debes mostrar los datos que has obtenido de las tools, sin interpretarlos ni sacar conclusiones. Solo datos.
**Recomendación Experto: 
Aqui puedes realizar una interpretación e incluso basarte en tu expertise más alla de los datos.

"""
REVIEWER_SYSTEM_MESSAGE = """Eres un revisor de calidad. Tu tarea es revisar que la respuesta del analista sigue la estructura indicada: datos primero, luego interpretación.
Si la respuesta es adecuada, indicalo y finaliza con un TERMINATE."""

TASK_TEMPLATE = """
¿A quién podría vender experiencias turísticas en {destination}?
"""


class AnalysisTeam:

    result_agent = "tourism_analyst"

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
            system_message=TOURISM_EXPERT_SYSTEM_MESSAGE,
            reflect_on_tool_use=True,
        )
        reviewer = AssistantAgent(
            name="reviewer",
            model_client=model_client,
            system_message=REVIEWER_SYSTEM_MESSAGE,
        )
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(max_messages=15)
        return RoundRobinGroupChat([agent, reviewer], termination_condition=termination)
