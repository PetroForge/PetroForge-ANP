import pandas as pd
import pytest

from src.analysis.kpis import production_kpis


OIL_COLUMN = "Produção de Óleo (m³)"

EXPECTED_KPI_KEYS = {
    "oil_total_m3",
    "oil_average_m3",
    "oil_maximum_m3",
    "oil_minimum_m3",
    "producing_states",
    "basins",
    "fields",
    "wells",
}


@pytest.fixture
def production_dataframe() -> pd.DataFrame:
    """Cria dados controlados para os testes dos KPIs."""

    return pd.DataFrame(
        {
            OIL_COLUMN: [100.0, 0.0, 50.0, None],
            "Estado": [
                "Rio de Janeiro",
                "São Paulo",
                None,
                "Espírito Santo",
            ],
            "Bacia": [
                "Santos",
                "Campos",
                "Santos",
                None,
            ],
            "Campo": [
                "CAMPO A",
                "CAMPO B",
                "CAMPO A",
                None,
            ],
            "Poço": [
                "POÇO 1",
                "POÇO 2",
                "POÇO 3",
                None,
            ],
        }
    )


def test_production_kpis_returns_expected_keys(
    production_dataframe: pd.DataFrame,
) -> None:
    """Verifica o contrato de dados utilizado pelo dashboard."""

    result = production_kpis(production_dataframe)

    assert set(result) == EXPECTED_KPI_KEYS


def test_production_kpis_calculates_expected_values(
    production_dataframe: pd.DataFrame,
) -> None:
    """Verifica os valores calculados pelos indicadores."""

    result = production_kpis(production_dataframe)

    assert result["oil_total_m3"] == pytest.approx(150.0)
    assert result["oil_average_m3"] == pytest.approx(50.0)
    assert result["oil_maximum_m3"] == pytest.approx(100.0)
    assert result["oil_minimum_m3"] == pytest.approx(0.0)
    assert result["producing_states"] == 1
    assert result["basins"] == 2
    assert result["fields"] == 2
    assert result["wells"] == 3


def test_production_kpis_excludes_states_without_production() -> None:
    """Verifica que produção zero não caracteriza estado produtor."""

    dataframe = pd.DataFrame(
        {
            OIL_COLUMN: [0.0, 0.0],
            "Estado": ["Alagoas", "Bahia"],
            "Bacia": ["Alagoas", "Camamu"],
            "Campo": ["CAMPO A", "CAMPO B"],
            "Poço": ["POÇO 1", "POÇO 2"],
        }
    )

    result = production_kpis(dataframe)

    assert result["producing_states"] == 0