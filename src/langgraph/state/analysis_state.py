from langgraph.graph import MessagesState


class AnalysisState(MessagesState):
    """
    Estado del grafo de análisis turístico.

    - messages: historial completo de mensajes (heredado de MessagesState)
    - recommendation: respuesta final del analyst para devolver al use case
    - review_approved: flag del reviewer para el edge condicional
    - review_count: número de veces que el reviewer ha evaluado la respuesta
    """
    recommendation: str
    review_approved: bool
    review_count: int
