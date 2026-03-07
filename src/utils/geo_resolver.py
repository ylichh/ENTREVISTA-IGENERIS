import pycountry


def _find_country(place: str) -> str | None:
    try:
        return pycountry.countries.lookup(place).alpha_2
    except LookupError:
        return None


def _find_subdivision(place: str) -> str | None:
    try:
        results = pycountry.subdivisions.search_fuzzy(place)
        return results[0].code.replace("_", "-") if results else None
    except LookupError:
        return None


def resolve_geo_code(place: str) -> str:
    """
    Resuelve un nombre de lugar al código geo de Google Trends.

    Acepta nombres de país o región en cualquier idioma, o código ISO directo.
    Ejemplos:
        "Germany"   → "DE"
        "Alemania"  → "DE"
        "Berlin"    → "DE-BE"
        "Bavaria"   → "DE-BY"
        "Andalucía" → "ES-AN"
        "DE"        → "DE"

    Raises:
        ValueError: si no se encuentra el lugar
    """
    geo = _find_country(place) or _find_subdivision(place)
    if geo:
        return geo
    raise ValueError(
        f"No se encontró el código geo para '{place}'. "
        "Prueba con el nombre en inglés o el código ISO directamente (ej: 'DE', 'ES-AN')."
    )

if __name__ == "__main__":
    test_places = [
        "Germany",
        "Berlin",
        "bavaria",
        "Andalucía",
        "DE",
        "áncash",
        "ES-AN",
        "UnknownPlace"
    ]
    for place in test_places:
        try:
            code = resolve_geo_code(place)
            print(f"{place} → {code}")
        except ValueError as e:
            print(e)
