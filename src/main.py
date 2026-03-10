import asyncio
from src.config import create_analysis_agent
from src.autogen.teams.analysis_team import TASK_TEMPLATE


async def main():
    agent = create_analysis_agent()

    task = TASK_TEMPLATE.format(destination="Andalucía")

    print("=== Lanzando análisis de demanda turística ===\n")
    response = await agent.ask(task)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
