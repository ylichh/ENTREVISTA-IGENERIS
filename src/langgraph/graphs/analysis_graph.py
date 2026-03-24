"""
analysis_graph: construye y compila el StateGraph de análisis turístico.

Flujo:
  START → analyst → [tools → analyst]* → reviewer → END
                                       ↑           |
                                       └── analyst ┘ (si REJECTED y review_count < MAX)
"""
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.langgraph.state.analysis_state import AnalysisState
from src.langgraph.nodes.analyst_node import make_analyst_node
from src.langgraph.nodes.reviewer_node import make_reviewer_node


def _route_reviewer(state: AnalysisState) -> str:
    return END if state["review_approved"] else "analyst"


def build_analysis_graph(tools: list):
    analyst_node, _ = make_analyst_node(tools)
    reviewer_node = make_reviewer_node()

    graph = StateGraph(AnalysisState)

    graph.add_node("analyst", analyst_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("reviewer", reviewer_node)

    graph.add_edge(START, "analyst")

    # Si el analyst emite tool_calls → tools, si no → reviewer
    graph.add_conditional_edges(
        "analyst",
        tools_condition,
        {"tools": "tools", "__end__": "reviewer"},
    )

    # Tras ejecutar tools, vuelve al analyst
    graph.add_edge("tools", "analyst")

    # reviewer decide si iterar o terminar
    graph.add_conditional_edges("reviewer", _route_reviewer)

    return graph.compile()
