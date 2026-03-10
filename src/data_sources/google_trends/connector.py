from pytrends.request import TrendReq
import pandas as pd
from src.utils.geo_resolver import resolve_geo_code
from src.data_sources.base_connector import TrendsConnector


class GoogleTrendsConnector(TrendsConnector):
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
        self._hl = hl
        self._tz = tz

    def _fresh_client(self) -> TrendReq:
        """Instancia nueva por llamada para evitar filtrado de estado entre requests."""
        return TrendReq(hl=self._hl, tz=self._tz)

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

        self.pytrends = self._fresh_client()
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
    ) -> dict:
        """
        Qué busca la gente SOBRE un destino turístico.

        Args:
            destination: nombre del destino (ej: "Andalucía", "Sevilla", "Costa del Sol")
            from_country: filtrar por país de origen del buscador (ej: "DE", "GB", "FR").
                          "" = búsquedas desde cualquier país
            timeframe: rango temporal

        Returns:
            dict con: destination, from_country, top_queries, rising_queries
        """
        self._build_payload([destination], geo=from_country, timeframe=timeframe)
        related = self.pytrends.related_queries()
        result = related.get(destination, {})
        top_df = result.get("top")
        rising_df = result.get("rising")
        return {
            "destination": destination,
            "from_country": from_country or "worldwide",
            "timeframe": timeframe,
            "top_queries": top_df.head(10).to_dict("records") if top_df is not None else [],
            "rising_queries": rising_df.head(10).to_dict("records") if rising_df is not None else [],
        }

    def _get_interest_by_origin(
        self,
        destination: str,
        geo: str,
        resolution: str,
        timeframe: str,
    ) -> list:
        self._build_payload([destination], geo=geo, timeframe=timeframe)
        df = self.pytrends.interest_by_region(resolution=resolution, inc_low_vol=False)
        return (
            df[df[destination] > 0]
            .sort_values(by=destination, ascending=False)
            .head(10)
            .reset_index()
            .to_dict("records")
            if not df.empty else []
        )

    def get_interest_by_origin_country(
        self,
        destination: str,
        timeframe: str = "today 12-m",
    ) -> dict:
        """
        Desde qué países buscan más sobre un destino (índice 0-100 por país).

        Args:
            destination: nombre del destino (ej: "Andalucía", "Mallorca")
            timeframe: rango temporal
        """
        results = self._get_interest_by_origin(destination, geo="", resolution="COUNTRY", timeframe=timeframe)
        return {"destination": destination, "top_origin_countries": results}

    def get_interest_by_origin_region(
        self,
        destination: str,
        country: str,
        timeframe: str = "today 12-m",
    ) -> dict:
        """
        Desde qué regiones de un país buscan más sobre un destino (índice 0-100 por región).

        Args:
            destination: nombre del destino (ej: "Andalucía", "Mallorca")
            country: país a desglosar por regiones (ej: "Germany", "DE")
            timeframe: rango temporal
        """
        geo = resolve_geo_code(country)
        results = self._get_interest_by_origin(destination, geo=geo, resolution="REGION", timeframe=timeframe)
        return {"destination": destination, "country": country, "top_origin_regions": results}

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
    import json

    connector = GoogleTrendsConnector()
    destination = "Andalucía"
    from_country = "Germany"

    from_country_code = resolve_geo_code(from_country)

    print(f"=== get_searches_about_destination ===")
    print(f"Destino: {destination} | Desde: {from_country} ({from_country_code})\n")
    searches = connector.get_searches_about_destination(destination, from_country=from_country_code)
    print(json.dumps(searches, ensure_ascii=False, indent=2, default=str))

    print(f"\n=== get_interest_by_origin_country ===")
    print(f"Destino: {destination}\n")
    origins = connector.get_interest_by_origin_country(destination)
    print(json.dumps(origins, ensure_ascii=False, indent=2, default=str))

    print(f"\n=== get_interest_by_origin_region ===")
    print(f"Destino: {destination} | País: {from_country}\n")
    regions = connector.get_interest_by_origin_region(destination, from_country)
    print(json.dumps(regions, ensure_ascii=False, indent=2, default=str))
