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
        from src.data_sources.mock_connector import MockTrendsConnector
        return MockTrendsConnector()
    from src.data_sources.google_trends.connector import GoogleTrendsConnector
    return GoogleTrendsConnector()


def create_analysis_agent():
    from src.autogen.tools.trends_tool import TrendsTools
    from src.autogen.teams.analysis_team import build_analysis_agent

    connector = _resolve_trends_connector()
    tools = TrendsTools(connector).get_tools()
    return build_analysis_agent(tools)
