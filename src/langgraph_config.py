"""
Composition Root: único punto donde se instancian y cablean las dependencias LangGraph.

Controla qué adaptadores se usan mediante variables de entorno:
    TRENDS_CONNECTOR = "google" (default) | "mock"
    MEMORY_HANDLER   = "inmemory" (default) | "mongo"
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


def _resolve_memory_handler():
    memory_type = os.environ.get("MEMORY_HANDLER", "inmemory")
    if memory_type == "mongo":
        from src.memory.mongo_autogen_handler import MongoAutogenHandler
        uri = os.environ["MONGO_URI"]
        db_name = os.environ["MONGO_DB"]
        return MongoAutogenHandler(uri=uri, db_name=db_name)
    from src.memory.in_memory_autogen_handler import InMemoryAutogenHandler
    return InMemoryAutogenHandler()


def create_iterate_analysis():
    from src.langgraph.tools.trends_tool import TrendsTools
    from src.langgraph.analysis_langgraph_handler import AnalysisLangGraphHandler
    from src.use_cases.iterate_analysis import IterateAnalysis

    connector = _resolve_trends_connector()
    tools = TrendsTools(connector).get_tools()
    memory = _resolve_memory_handler()
    handler = AnalysisLangGraphHandler(tools=tools)
    return IterateAnalysis(chat_handler=handler, memory_handler=memory)
