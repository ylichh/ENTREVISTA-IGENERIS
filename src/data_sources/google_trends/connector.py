from pytrends.request import TrendReq
import pandas as pd
from src.utils.geo_resolver import resolve_geo_code


class GoogleTrendsConnector:
    """
    Connector para Google Trends usando pytrends (no requiere API key).

    Casos de uso principales:
    - Qué busca la gente SOBRE un destino (ej: qué buscan sobre Andalucía)
    - Qué busca la gente DESDE una región (ej: qué buscan los andaluces)
    - Interés por país de origen → proxy de nacionalidad del turista
    - Tendencias temporales y estacionalidad
    """

    def __init__(self, hl: str = "es", tz: int = 60):
        """
        Args:
            hl: idioma de la interfaz de Google Trends (ej: "es", "en", "de")
            tz: timezone offset en minutos (60 = Europa Central)
        """
        self.pytrends = TrendReq(hl=hl, tz=tz)

    def _build_payload(
        self,
        keywords: list[str],
        geo: str = "",
        timeframe: str = "today 12-m",
        cat: int = 67,
    ):
        """
        Args:
            keywords: lista de hasta 5 términos
            geo: código ISO de país/región (ej: "ES", "ES-AN", "DE"). "" = mundial
            timeframe: "today 12-m", "today 3-m", "today 5-y", "2023-01-01 2023-12-31"
            cat: categoría Google Trends. 67 = Travel & Tourism, 0 = todas
        """
        if len(keywords) > 5:
            raise ValueError("Google Trends admite máximo 5 keywords por consulta")

        self.pytrends.build_payload(
            kw_list=keywords,
            geo=geo,
            timeframe=timeframe,
            cat=cat,
        )

    # ------------------------------------------------------------------
    # QUÉ BUSCAN SOBRE UN DESTINO
    # ------------------------------------------------------------------

    def get_searches_about_destination(
        self,
        destination: str,
        from_country: str = "",
        timeframe: str = "today 12-m",
    ) -> dict[str, pd.DataFrame | None]:
        """
        Qué busca la gente SOBRE un destino turístico.

        Usa el nombre del destino como keyword y extrae las queries relacionadas:
        esto revela qué aspectos interesan (playas, gastronomía, hoteles, etc.)

        Args:
            destination: nombre del destino (ej: "Andalucía", "Sevilla", "Costa del Sol")
            from_country: filtrar por país de origen del buscador (ej: "DE", "GB", "FR").
                          "" = búsquedas desde cualquier país
            timeframe: rango temporal

        Returns:
            dict con:
                - "top": queries más buscadas junto al destino (DataFrame)
                - "rising": queries que más están creciendo (DataFrame)
        """
        self._build_payload([destination], geo=from_country, timeframe=timeframe)
        related = self.pytrends.related_queries()
        result = related.get(destination, {})
        return {
            "destination": destination,
            "from_country": from_country or "worldwide",
            "timeframe": timeframe,
            "top": result.get("top"),
            "rising": result.get("rising"),
        }

    def get_interest_by_origin_country(
        self,
        destination: str,
        timeframe: str = "today 12-m",
    ) -> pd.DataFrame:
        """
        Desde qué países buscan más sobre un destino (índice 0-100 por país).

        Útil para identificar los mercados emisores más relevantes
        → proxy de la nacionalidad del turista potencial.

        Args:
            destination: nombre del destino (ej: "Andalucía", "Mallorca")
            timeframe: rango temporal

        Returns:
            DataFrame con columna del destino indexado por país (geoName)
        """
        self._build_payload([destination], geo="", timeframe=timeframe)
        return self.pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True)



    # ------------------------------------------------------------------
    # QUÉ BUSCA LA GENTE DESDE UNA REGIÓN
    # ------------------------------------------------------------------

    def get_trending_in_region(
        self,
        region: str,
        keywords: list[str],
        timeframe: str = "today 12-m",
        cat: int = 67,
    ) -> pd.DataFrame:
        """
        Interés de búsqueda de keywords concretas DESDE cualquier lugar del mundo.

        Útil para entender qué buscan los turistas potenciales de una región concreta.

        Args:
            region: nombre del lugar en cualquier idioma o código ISO directo
                    (ej: "Germany", "Bavaria", "Berlin", "Andalucía", "DE", "DE-BY")
            keywords: términos a analizar (ej: ["playa", "montaña", "gastronomía"])
            timeframe: rango temporal
            cat: categoría (67 = Travel, 0 = todas)

        Returns:
            DataFrame con evolución temporal del interés
        """
        geo = resolve_geo_code(region)
        self._build_payload(keywords, geo=geo, timeframe=timeframe, cat=cat)
        df = self.pytrends.interest_over_time()
        if "isPartial" in df.columns:
            df = df.drop(columns=["isPartial"])
        return df

    # ------------------------------------------------------------------
    # PERFIL COMPLETO DE UN DESTINO
    # ------------------------------------------------------------------

    def get_destination_profile(
        self,
        destination: str,
        from_country: str = "",
        timeframe: str = "today 12-m",
    ) -> dict:
        """
        Perfil completo de tendencias para un destino turístico.

        Combina:
        - Evolución temporal del interés
        - Países que más buscan el destino (mercados emisores)
        - Queries relacionadas top y en alza

        Args:
            destination: nombre del destino (ej: "Andalucía", "Costa del Sol")
            from_country: filtrar búsquedas desde un país (ej: "DE"). "" = mundial
            timeframe: rango temporal
        """
        interest_time = self.get_interest_over_time(
            [destination], geo=from_country, timeframe=timeframe
        )
        interest_by_country = self.get_interest_by_origin_country(destination, timeframe)
        searches_about = self.get_searches_about_destination(
            destination, from_country=from_country, timeframe=timeframe
        )

        return {
            "destination": destination,
            "geo_filter": from_country or "worldwide",
            "timeframe": timeframe,
            "interest_over_time": interest_time,
            "interest_by_country": interest_by_country,
            "related_queries_top": searches_about["top"],
            "related_queries_rising": searches_about["rising"],
        }


if __name__ == "__main__":
    connector = GoogleTrendsConnector()
    destination="liliput"
    origin_country="bayern"
    destination_code = resolve_geo_code(destination)
    origin_code = resolve_geo_code(origin_country)
    print(f"Código geo para {destination}: {destination_code}")
    print(f"Código geo para {origin_country}: {origin_code}")
    queries = connector.get_searches_about_destination(destination, from_country=origin_code)
    print(f"Tendencias de búsqueda SOBRE {destination} desde {origin_country}:")
    print(queries)
    print()
    interest_by_country = connector.get_interest_by_origin_country(destination)
    print(f"Interés por {destination} según país de origen:")
