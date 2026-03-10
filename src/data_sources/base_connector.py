from abc import ABC, abstractmethod
from typing import TypedDict


class SearchQuery(TypedDict):
    query: str
    value: int


class DestinationSearches(TypedDict):
    destination: str
    from_country: str
    timeframe: str
    top_queries: list[SearchQuery]
    rising_queries: list[SearchQuery]


class OriginCountry(TypedDict):
    geoName: str
    value: int


class OriginCountries(TypedDict):
    destination: str
    top_origin_countries: list[OriginCountry]


class OriginRegions(TypedDict):
    destination: str
    country: str
    top_origin_regions: list[OriginCountry]


class TrendsConnector(ABC):

    @abstractmethod
    def get_searches_about_destination(
        self,
        destination: str,
        from_country: str = "",
        timeframe: str = "today 12-m",
    ) -> DestinationSearches:
        ...

    @abstractmethod
    def get_interest_by_origin_country(
        self,
        destination: str,
        timeframe: str = "today 12-m",
    ) -> OriginCountries:
        ...

    @abstractmethod
    def get_interest_by_origin_region(
        self,
        destination: str,
        country: str,
        timeframe: str = "today 12-m",
    ) -> OriginRegions:
        ...
