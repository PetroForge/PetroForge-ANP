import pandas as pd

from src.data.load import DATA_PATH, load_data
from src.processing.clean import clean_data


REQUIRED_COLUMNS = {
    "Mês/Ano",
    "Estado",
    "Bacia",
    "Campo",
    "Poço",
    "Produção de Óleo (m³)",
    "Produção de Gás Associado (Mm³)",
    "Produção de Gás Não Associado (Mm³)",
}

NUMERIC_COLUMNS = {
    "Produção de Óleo (m³)",
    "Produção de Gás Associado (Mm³)",
    "Produção de Gás Não Associado (Mm³)",
}


def test_anp_data_file_exists() -> None:
    """Verifica se o arquivo de dados esperado está disponível."""

    assert DATA_PATH.is_file()


def test_real_anp_pipeline_loads_and_cleans_data() -> None:
    """Verifica a integração entre carregamento e limpeza."""

    raw_dataframe = load_data()
    result = clean_data(raw_dataframe.copy())

    assert not result.empty
    assert REQUIRED_COLUMNS.issubset(result.columns)

    assert all(
        "[" not in column and "]" not in column
        for column in result.columns
    )

    assert pd.api.types.is_datetime64_any_dtype(
        result["Mês/Ano"]
    )

    for column in NUMERIC_COLUMNS:
        assert pd.api.types.is_numeric_dtype(result[column])