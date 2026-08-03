import pandas as pd
import pytest

from src.analysis.production import (
    oil_gas_by_month,
    oil_heatmap_state_month,
    oil_production_by,
    oil_production_by_month,
    oil_production_by_well,
    oil_production_treemap,
)


OIL_COLUMN = "Produção de Óleo (m³)"
SHARE_COLUMN = "Participação (%)"


def test_oil_production_by_groups_and_orders_values() -> None:
    """Verifica soma, ordenação e preservação de categoria ausente."""

    dataframe = pd.DataFrame(
        {
            "Estado": [
                "Rio de Janeiro",
                "São Paulo",
                "Rio de Janeiro",
                None,
            ],
            OIL_COLUMN: [100.0, 50.0, 25.0, 25.0],
        }
    )

    result = oil_production_by(dataframe, "Estado")

    assert result[OIL_COLUMN].tolist() == [125.0, 50.0, 25.0]
    assert result[SHARE_COLUMN].tolist() == [62.5, 25.0, 12.5]
    assert pd.isna(result.iloc[-1]["Estado"])


def test_oil_production_by_top_n_uses_complete_total() -> None:
    """Verifica que o ranking mantém a participação sobre o total."""

    dataframe = pd.DataFrame(
        {
            "Campo": ["CAMPO A", "CAMPO B", "CAMPO C"],
            OIL_COLUMN: [100.0, 60.0, 40.0],
        }
    )

    result = oil_production_by(
        dataframe,
        group_by="Campo",
        top_n=2,
    )

    assert result["Campo"].tolist() == ["CAMPO A", "CAMPO B"]
    assert result[OIL_COLUMN].tolist() == [100.0, 60.0]
    assert result[SHARE_COLUMN].tolist() == [50.0, 30.0]


def test_oil_production_by_handles_zero_total() -> None:
    """Verifica a participação quando a produção total é zero."""

    dataframe = pd.DataFrame(
        {
            "Bacia": ["BACIA A", "BACIA B"],
            OIL_COLUMN: [0.0, 0.0],
        }
    )

    result = oil_production_by(dataframe, "Bacia")

    assert result[OIL_COLUMN].tolist() == [0.0, 0.0]
    assert result[SHARE_COLUMN].isna().all()


def test_oil_production_by_month_calculates_variation() -> None:
    """Verifica agregação, ordenação e variação mensal."""

    dataframe = pd.DataFrame(
        {
            "Mês/Ano": [
                pd.Timestamp("2026-02-01"),
                pd.Timestamp("2026-01-01"),
                pd.Timestamp("2026-03-01"),
                pd.Timestamp("2026-01-01"),
            ],
            OIL_COLUMN: [165.0, 100.0, 132.0, 50.0],
        }
    )

    result = oil_production_by_month(dataframe)

    assert result["Mês/Ano"].tolist() == [
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-02-01"),
        pd.Timestamp("2026-03-01"),
    ]

    assert result[OIL_COLUMN].tolist() == [
        150.0,
        165.0,
        132.0,
    ]

    assert pd.isna(result.loc[0, "Variação (%)"])
    assert result.loc[1, "Variação (%)"] == pytest.approx(10.0)
    assert result.loc[2, "Variação (%)"] == pytest.approx(-20.0)


def test_oil_production_by_well_applies_ranking() -> None:
    """Verifica o ranking dos poços e o limite top_n."""

    dataframe = pd.DataFrame(
        {
            "Poço": ["POÇO 1", "POÇO 2", "POÇO 1", "POÇO 3"],
            OIL_COLUMN: [100.0, 50.0, 25.0, 10.0],
        }
    )

    result = oil_production_by_well(
        dataframe,
        top_n=2,
    )

    assert result["Poço"].tolist() == ["POÇO 1", "POÇO 2"]
    assert result[OIL_COLUMN].tolist() == [125.0, 50.0]
    assert result.loc[0, SHARE_COLUMN] == pytest.approx(
        125.0 / 185.0 * 100
    )
    assert result.loc[1, SHARE_COLUMN] == pytest.approx(
        50.0 / 185.0 * 100
    )

def test_oil_gas_by_month_calculates_total_gas() -> None:
    """Verifica a agregação mensal de óleo e gás."""

    dataframe = pd.DataFrame(
        {
            "Mês/Ano": [
                pd.Timestamp("2026-01-01"),
                pd.Timestamp("2026-01-01"),
                pd.Timestamp("2026-02-01"),
            ],
            OIL_COLUMN: [100.0, 50.0, 80.0],
            "Produção de Gás Associado (Mm³)": [
                10.0,
                None,
                20.0,
            ],
            "Produção de Gás Não Associado (Mm³)": [
                5.0,
                7.0,
                None,
            ],
        }
    )

    result = oil_gas_by_month(dataframe)

    assert result["Mês/Ano"].tolist() == [
        pd.Timestamp("2026-01-01"),
        pd.Timestamp("2026-02-01"),
    ]

    assert result[OIL_COLUMN].tolist() == [150.0, 80.0]

    assert result[
        "Produção Total de Gás (Mm³)"
    ].tolist() == [22.0, 20.0]


def test_oil_heatmap_state_month_creates_matrix() -> None:
    """Verifica a matriz de produção por estado e mês."""

    january = pd.Timestamp("2026-01-01")
    february = pd.Timestamp("2026-02-01")

    dataframe = pd.DataFrame(
        {
            "Estado": [
                "Rio de Janeiro",
                "Rio de Janeiro",
                "São Paulo",
                None,
            ],
            "Mês/Ano": [
                january,
                february,
                january,
                january,
            ],
            OIL_COLUMN: [100.0, 200.0, 50.0, 25.0],
        }
    )

    result = oil_heatmap_state_month(dataframe)

    assert result.loc["Rio de Janeiro", january] == pytest.approx(100.0)
    assert result.loc["Rio de Janeiro", february] == pytest.approx(200.0)
    assert result.loc["São Paulo", january] == pytest.approx(50.0)
    assert pd.isna(result.loc["São Paulo", february])
    assert result.index.isna().any()


def test_oil_production_treemap_removes_incomplete_hierarchies() -> None:
    """Verifica a remoção de hierarquias incompatíveis com o Treemap."""

    dataframe = pd.DataFrame(
        {
            "Estado": [
                "Rio de Janeiro",
                "Rio de Janeiro",
                None,
                "São Paulo",
            ],
            "Campo": [
                "CAMPO A",
                None,
                "CAMPO C",
                "CAMPO B",
            ],
            OIL_COLUMN: [100.0, 50.0, 25.0, 75.0],
        }
    )

    result = oil_production_treemap(dataframe)

    assert len(result) == 2
    assert not result[["Estado", "Campo"]].isna().any().any()

    production_by_field = result.set_index("Campo")[OIL_COLUMN]

    assert production_by_field["CAMPO A"] == pytest.approx(100.0)
    assert production_by_field["CAMPO B"] == pytest.approx(75.0)