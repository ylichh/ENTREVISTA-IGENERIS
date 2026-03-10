"""
AutogenAgent: wrapper genérico sobre cualquier team de AutoGen 0.7.5.

Acepta AssistantAgent, RoundRobinGroupChat, SelectorGroupChat, etc.
Todos comparten la misma interfaz run_stream() → AsyncGenerator, por lo que
el método ask() funciona sin cambios independientemente del team inyectado.
"""
from autogen_agentchat.base import TaskResult


class AutogenAgent:
    def __init__(self, team):
        self._team = team

    async def ask(self, task: str) -> str:
        final = ""
        async for message in self._team.run_stream(task=task):
            if isinstance(message, TaskResult):
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
