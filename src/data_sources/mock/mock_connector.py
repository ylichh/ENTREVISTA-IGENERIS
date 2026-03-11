from src.data_sources.base_connector import (
    DestinationSearches,
    OriginCountries,
    OriginRegions,
    TrendsConnector,
)


class MockTrendsConnector(TrendsConnector):

    def get_searches_about_destination(
        self,
        destination: str,
        from_country: str = "",
        timeframe: str = "today 12-m",
    ) -> DestinationSearches:
        print(f"[MockTrendsConnector] get_searches_about_destination(destination={destination!r}, from_country={from_country!r}, timeframe={timeframe!r})")
        return DestinationSearches(
            destination=destination,
            from_country=from_country,
            timeframe=timeframe,
            top_queries=[
                {"query": f"{destination} hoteles", "value": 100},
                {"query": f"{destination} playas", "value": 85},
                {"query": f"{destination} gastronomía", "value": 70},
            ],
            rising_queries=[
                {"query": f"{destination} turismo sostenible", "value": 250},
                {"query": f"{destination} enoturismo", "value": 180},
            ],
        )

    def get_interest_by_origin_country(
        self,
        destination: str,
        timeframe: str = "today 12-m",
    ) -> OriginCountries:
        print(f"[MockTrendsConnector] get_interest_by_origin_country(destination={destination!r}, timeframe={timeframe!r})")
        return OriginCountries(
            destination=destination,
            top_origin_countries=[
                {"geoName": "Germany", "value": 100},
                {"geoName": "United Kingdom", "value": 92},
                {"geoName": "France", "value": 78},
                {"geoName": "Netherlands", "value": 65},
                {"geoName": "United States", "value": 54},
            ],
        )

    def get_interest_by_origin_region(
        self,
        destination: str,
        country: str,
        timeframe: str = "today 12-m",
    ) -> OriginRegions:
        print(f"[MockTrendsConnector] get_interest_by_origin_region(destination={destination!r}, country={country!r}, timeframe={timeframe!r})")
        return OriginRegions(
            destination=destination,
            country=country,
            top_origin_regions=[
                {"geoName": "Bavaria", "value": 100},
                {"geoName": "Berlin", "value": 88},
                {"geoName": "Hamburg", "value": 74},
                {"geoName": "North Rhine-Westphalia", "value": 61},
            ],
        )
