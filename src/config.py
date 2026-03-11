"""
Composition Root: único punto donde se instancian y cablean las dependencias.

Controla qué adaptadores se usan mediante variables de entorno:
    TRENDS_CONNECTOR = "google" (default) | "mock"
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _resolve_trends_connector():
    connector_type = os.environ.get("TRENDS_CONNECTOR", "google")
    if connector_type == "mock":
        from src.data_sources.mock.mock_connector import MockTrendsConnector
        return MockTrendsConnector()
    from src.data_sources.google_trends.connector import GoogleTrendsConnector
    return GoogleTrendsConnector()


def create_iterate_analysis():
    from src.autogen.tools.trends_tool import TrendsTools
    from src.autogen.teams.analysis_team import AnalysisTeam
    from src.memory.in_memory_autogen_handler import InMemoryAutogenHandler
    from src.autogen.autogen_team import AutogenAgent
    from src.use_cases.iterate_analysis import IterateAnalysis

    connector = _resolve_trends_connector()
    tools = TrendsTools(connector).get_tools()
    memory = InMemoryAutogenHandler()
    handler = AutogenAgent(team_builder=AnalysisTeam(tools))
    return IterateAnalysis(chat_handler=handler, memory_handler=memory)
