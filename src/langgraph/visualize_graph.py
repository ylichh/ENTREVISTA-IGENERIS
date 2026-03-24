"""
Utilidad para visualizar el grafo de análisis.

Uso:
    python -m src.langgraph.visualize_graph
"""
from dotenv import load_dotenv
load_dotenv()

from src.data_sources.mock.mock_connector import MockTrendsConnector
from src.langgraph.tools.trends_tool import TrendsTools
from src.langgraph.graphs.analysis_graph import build_analysis_graph

OUTPUT_PATH = "graph.png"


def main():
    tools = TrendsTools(MockTrendsConnector()).get_tools()
    app = build_analysis_graph(tools)

    mermaid = app.get_graph().draw_mermaid()
    print(mermaid)

    with open("graph.md", "w") as f:
        f.write(f"```mermaid\n{mermaid}\n```")
    print("\nGrafo guardado en graph.md — ábrelo en VSCode para verlo renderizado")


if __name__ == "__main__":
    main()
