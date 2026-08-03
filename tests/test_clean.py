import pandas as pd
import pytest

from src.processing.clean import (
    clean_column_names,
    clean_data,
    convert_date_column,
)


@pytest.fixture
def raw_dataframe() -> pd.DataFrame:
    """Cria um DataFrame bruto reutilizável pelos testes."""

    return pd.DataFrame(
        {
            " [Mês/Ano] ": ["01/2026", "02/2026"],
            " [Campo] ": ["TUPI", "MERO"],
        }
    )


def test_clean_column_names(raw_dataframe: pd.DataFrame) -> None:
    """Verifica a remoção de colchetes e espaços dos nomes."""

    result = clean_column_names(raw_dataframe)

    assert result.columns.tolist() == ["Mês/Ano", "Campo"]


def test_convert_date_column() -> None:
    """Verifica a conversão de mês e ano para datetime."""

    dataframe = pd.DataFrame(
        {
            "Mês/Ano": ["01/2026", "05/2026"],
        }
    )

    result = convert_date_column(dataframe)

    expected = pd.Series(
        [
            pd.Timestamp("2026-01-01"),
            pd.Timestamp("2026-05-01"),
        ],
        name="Mês/Ano",
    )

    pd.testing.assert_series_equal(
        result["Mês/Ano"],
        expected,
    )


def test_clean_data(raw_dataframe: pd.DataFrame) -> None:
    """Verifica a execução integrada do pipeline de limpeza."""

    result = clean_data(raw_dataframe)

    assert result.columns.tolist() == ["Mês/Ano", "Campo"]
    assert result["Mês/Ano"].tolist() == [
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-02-01"),
    ]


def test_convert_date_column_rejects_invalid_date() -> None:
    """Verifica que uma data inválida interrompe o tratamento."""

    dataframe = pd.DataFrame(
        {
            "Mês/Ano": ["data inválida"],
        }
    )

    with pytest.raises(ValueError):
        convert_date_column(dataframe)