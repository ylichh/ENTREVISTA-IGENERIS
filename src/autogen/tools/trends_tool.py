"""
Wrapper de TrendsConnector para su uso como tools de AutoGen.
La serialización a dict ocurre dentro del conector, no aquí.
El conector se inyecta en TrendsTools desde el Composition Root (src/config.py).
"""
import json
from src.data_sources.base_connector import TrendsConnector


class TrendsTools:
    def __init__(self, connector: TrendsConnector):
        self._connector = connector

    def get_destination_searches(self, destination: str, from_country: str = "", timeframe: str = "today 12-m") -> str:
        """
        Devuelve qué busca la gente sobre un destino turístico: temas top y queries en alza.
        Usar para conocer los intereses reales y tendencias emergentes asociadas al destino.
        Llamar sin from_country para visión global; con from_country para ver qué busca un mercado concreto.

        Args:
            destination: nombre del destino (ej: "Andalucía", "Mallorca")
            from_country: país de origen del buscador en inglés o código ISO (ej: "Germany", "DE"). Vacío = mundial.
            timeframe: rango temporal (ej: "today 12-m", "today 3-m")
        """
        return json.dumps(self._connector.get_searches_about_destination(destination, from_country, timeframe), ensure_ascii=False, default=str)

    def get_top_origin_countries(self, destination: str, timeframe: str = "today 12-m") -> str:
        """
        Devuelve los países que más buscan un destino turístico (proxy de mercado emisor).

        Args:
            destination: nombre del destino (ej: "Andalucía", "Costa del Sol")
            timeframe: rango temporal (ej: "today 12-m", "today 3-m")
        """
        return json.dumps(self._connector.get_interest_by_origin_country(destination, timeframe), ensure_ascii=False, default=str)

    def get_interest_by_origin_region(self, destination: str, country: str, timeframe: str = "today 12-m") -> str:
        """
        Devuelve las regiones de un país que más buscan un destino turístico.
        Útil para afinar la segmentación geográfica dentro de un mercado emisor clave.

        Args:
            destination: nombre del destino (ej: "Andalucía", "Mallorca")
            country: país a desglosar por regiones en inglés o código ISO (ej: "Germany", "DE")
            timeframe: rango temporal (ej: "today 12-m", "today 3-m")
        """
        return json.dumps(self._connector.get_interest_by_origin_region(destination, country, timeframe), ensure_ascii=False, default=str)

    def get_tools(self) -> list:
        """Devuelve los métodos como tools listas para inyectar en AssistantAgent."""
        return [self.get_destination_searches, self.get_top_origin_countries, self.get_interest_by_origin_region]
