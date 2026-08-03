import pytest

from src.utils.formatters import format_integer, format_volume


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (850.5, "850.50 m³"),
        (1_500, "1.50 mil m³"),
        (2_500_000, "2.50 milhões m³"),
    ],
)
def test_format_volume(value: float, expected: str) -> None:
    """Verifica a formatação de diferentes escalas de volume."""

    assert format_volume(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, "0"),
        (887, "887"),
        (1_000, "1.000"),
        (1_234_567, "1.234.567"),
    ],
)
def test_format_integer(value: int, expected: str) -> None:
    """Verifica a formatação de números inteiros."""

    assert format_integer(value) == expected