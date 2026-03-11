"""
Wrapper de TrendsConnector como tools de LangChain.

El conector se inyecta desde el Composition Root.
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
        def get_destination_searches(destination: str, from_country: str = "", timeframe: str = "today 12-m") -> str:
            """
            Devuelve qué busca la gente sobre un destino turístico: temas top y queries en alza.
            Usar para conocer los intereses reales y tendencias emergentes asociadas al destino.
            Llamar sin from_country para visión global; con from_country para ver qué busca un mercado concreto.

            Args:
                destination: nombre del destino (ej: "Andalucía", "Mallorca")
                from_country: país de origen del buscador en inglés o código ISO (ej: "Germany", "DE"). Vacío = mundial.
                timeframe: rango temporal (ej: "today 12-m", "today 3-m")
            """
            return json.dumps(connector.get_searches_about_destination(destination, from_country, timeframe), ensure_ascii=False, default=str)

        @tool
        def get_top_origin_countries(destination: str, timeframe: str = "today 12-m") -> str:
            """
            Devuelve los países que más buscan un destino turístico (proxy de mercado emisor).

            Args:
                destination: nombre del destino (ej: "Andalucía", "Costa del Sol")
                timeframe: rango temporal (ej: "today 12-m", "today 3-m")
            """
            return json.dumps(connector.get_interest_by_origin_country(destination, timeframe), ensure_ascii=False, default=str)

        @tool
        def get_interest_by_origin_region(destination: str, country: str, timeframe: str = "today 12-m") -> str:
            """
            Devuelve las regiones de un país que más buscan un destino turístico.
            Útil para afinar la segmentación geográfica dentro de un mercado emisor clave.

            Args:
                destination: nombre del destino (ej: "Andalucía", "Mallorca")
                country: país a desglosar por regiones en inglés o código ISO (ej: "Germany", "DE")
                timeframe: rango temporal (ej: "today 12-m", "today 3-m")
            """
            return json.dumps(connector.get_interest_by_origin_region(destination, country, timeframe), ensure_ascii=False, default=str)

        return [get_destination_searches, get_top_origin_countries, get_interest_by_origin_region]
