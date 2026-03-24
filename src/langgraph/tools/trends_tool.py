"""
TrendsTools: wrappea TrendsConnector como tools de LangGraph.

El conector se inyecta desde el Composition Root para mantener
la arquitectura hexagonal — las tools no instancian dependencias.
"""
import json

from langchain_core.tools import tool

from src.data_sources.base_connector import TrendsConnector


class TrendsTools:

    def __init__(self, connector: TrendsConnector) -> None:
        self._connector = connector

    def get_tools(self) -> list:
        connector = self._connector

        @tool
        def get_destination_searches(
            destination: str,
            from_country: str = "",
            timeframe: str = "today 12-m",
        ) -> str:
            """
            Devuelve qué busca la gente sobre un destino turístico: temas top y queries en alza.
            Usar para conocer los intereses reales y tendencias emergentes del destino.
            Sin from_country = visión global. Con from_country = mercado concreto.

            Args:
                destination: nombre del destino (ej: "Andalucía", "Mallorca")
                from_country: país emisor en inglés o ISO (ej: "Germany", "DE"). Vacío = mundial.
                timeframe: rango temporal (ej: "today 12-m", "today 3-m")
            """
            result = connector.get_searches_about_destination(destination, from_country, timeframe)
            return json.dumps(result, ensure_ascii=False, default=str)

        @tool
        def get_top_origin_countries(
            destination: str,
            timeframe: str = "today 12-m",
        ) -> str:
            """
            Devuelve los países que más buscan un destino turístico (proxy de mercado emisor).

            Args:
                destination: nombre del destino (ej: "Andalucía", "Costa del Sol")
                timeframe: rango temporal (ej: "today 12-m", "today 3-m")
            """
            result = connector.get_interest_by_origin_country(destination, timeframe)
            return json.dumps(result, ensure_ascii=False, default=str)

        @tool
        def get_interest_by_region(
            destination: str,
            country: str,
            timeframe: str = "today 12-m",
        ) -> str:
            """
            Devuelve las regiones de un país que más buscan un destino turístico.
            Útil para afinar segmentación geográfica dentro de un mercado emisor clave.

            Args:
                destination: nombre del destino (ej: "Andalucía", "Mallorca")
                country: país a desglosar por regiones en inglés o ISO (ej: "Germany", "DE")
                timeframe: rango temporal (ej: "today 12-m", "today 3-m")
            """
            result = connector.get_interest_by_origin_region(destination, country, timeframe)
            return json.dumps(result, ensure_ascii=False, default=str)

        return [get_destination_searches, get_top_origin_countries, get_interest_by_region]
