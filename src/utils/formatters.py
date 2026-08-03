"""Formatação de valores apresentados na interface."""

def format_volume(value: float) -> str:
    """Formata um volume em m³, milhares ou milhões."""

    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} milhões m³"

    if value >= 1_000:
        return f"{value / 1_000:.2f} mil m³"

    return f"{value:.2f} m³"


def format_integer(value: int) -> str:
    """Formata um número inteiro com separador de milhar."""

    return f"{value:,}".replace(",", ".")