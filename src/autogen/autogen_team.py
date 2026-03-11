"""
AutogenAgent: runner genérico para cualquier team de AutoGen.

Instancia el team en cada llamada a handle(), carga el estado previo
(save_state / load_state) y lo persiste tras la ejecución.
"""
import asyncio

from autogen_agentchat.base import TaskResult

from src.use_cases.port.chat_handler import ChatHandler


class AutogenAgent(ChatHandler):

    def __init__(self, team_builder) -> None:
        """
        team_builder: objeto con un método build() que devuelve un RoundRobinGroupChat.
        """
        self._team_builder = team_builder
        self._state: dict = {}

    def handle(self, user_input: str, state: dict) -> tuple[str, dict]:
        return asyncio.run(self._run(user_input, state))

    async def _run(self, user_input: str, state: dict) -> tuple[str, dict]:
        team = self._team_builder.build()
        if state:
            await team.load_state(state)
        result = await self._ask(team, user_input)
        new_state = await team.save_state()
        return result.removesuffix("TERMINATE").strip(), new_state

    async def _ask(self, team, task: str) -> str:
        result_agent = getattr(self._team_builder, "result_agent", None)
        final = ""
        async for message in team.run_stream(task=task):
            if isinstance(message, TaskResult):
                if result_agent:
                    expert_messages = [m for m in message.messages if getattr(m, "source", None) == result_agent]
                    final = expert_messages[-1].content if expert_messages else message.messages[-1].content
                else:
                    final = message.messages[-1].content
            else:
                self._print_message(message)
        return final

    def _print_message(self, message) -> None:
        msg_type = type(message).__name__
        source = getattr(message, "source", "")
        content = getattr(message, "content", "")

        if msg_type == "ToolCallRequestEvent":
            for call in content:
                print(f"\n[tool_call] {call.name}({call.arguments})")
        elif msg_type == "ToolCallExecutionEvent":
            for result in content:
                print(f"[tool_result] {result.call_id}: {str(result.content)[:300]}")
        elif content:
            print(f"\n[{source}] {content}")
