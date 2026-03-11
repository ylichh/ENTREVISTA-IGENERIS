"""
Composition Root para la rama LangChain.

Instancia y cablea: InMemoryHandler + AnalysisLangchainHandler + IterateAnalysis.
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
    from src.langchain.tools.trends_tool import TrendsTools
    from src.langchain.analysis_langchain_handler import AnalysisLangchainHandler
    from src.memory.in_memory_handler import InMemoryHandler
    from src.use_cases.iterate_analysis import IterateAnalysis

    connector = _resolve_trends_connector()
    tools = TrendsTools(connector).get_tools()
    memory = InMemoryHandler()
    handler = AnalysisLangchainHandler(tools=tools)
    return IterateAnalysis(chat_handler=handler, memory_handler=memory)
