"""
AdTeam: construye el RoundRobinGroupChat para generación de anuncios publicitarios.

Recibe las tools inyectadas desde el Composition Root.
"""
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

AD_SYSTEM_MESSAGE = """
Eres un experto en publicidad turística. Tu tarea es generar una imagen publicitaria
a partir del análisis de demanda turística proporcionado.

Usa la tool disponible para crear la imagen. Cuando tengas la URL, devuélvela y finaliza con TERMINATE.
"""


class AdTeam:

    result_agent = "ad_creator"

    def __init__(self, tools: list) -> None:
        self._tools = tools

    def build(self) -> RoundRobinGroupChat:
        model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=os.environ["OPENAI_API_KEY"],
        )
        agent = AssistantAgent(
            name="ad_creator",
            model_client=model_client,
            tools=self._tools,
            system_message=AD_SYSTEM_MESSAGE,
            reflect_on_tool_use=True,
        )
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(max_messages=5)
        return RoundRobinGroupChat([agent], termination_condition=termination)
