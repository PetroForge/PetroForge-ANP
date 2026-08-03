from collections.abc import Callable

import pandas as pd
import plotly.graph_objects as go
import pytest

from src.analysis.production import (
    oil_gas_by_month,
    oil_heatmap_state_month,
    oil_production_by_basin,
    oil_production_by_field,
    oil_production_by_month,
    oil_production_by_state,
    oil_production_by_well,
    oil_production_treemap,
)
from src.visualization.plots import (
    plot_heatmap_state_month,
    plot_monthly_oil_production,
    plot_oil_by_basin,
    plot_oil_by_field,
    plot_oil_by_state,
    plot_oil_by_well,
    plot_oil_vs_gas,
    plot_treemap_oil,
)


AnalysisFunction = Callable[[pd.DataFrame], pd.DataFrame]
PlotFunction = Callable[[pd.DataFrame], go.Figure]


@pytest.fixture
def production_dataframe() -> pd.DataFrame:
    """Cria dados compatíveis com todas as visualizações."""

    return pd.DataFrame(
        {
            "Mês/Ano": [
                pd.Timestamp("2026-01-01"),
                pd.Timestamp("2026-01-01"),
                pd.Timestamp("2026-02-01"),
                pd.Timestamp("2026-02-01"),
            ],
            "Estado": [
                "Rio de Janeiro",
                "Rio de Janeiro",
                "São Paulo",
                "São Paulo",
            ],
            "Bacia": [
                "Santos",
                "Santos",
                "Santos",
                "Campos",
            ],
            "Campo": [
                "CAMPO A",
                "CAMPO A",
                "CAMPO B",
                "CAMPO C",
            ],
            "Poço": [
                "POÇO 1",
                "POÇO 2",
                "POÇO 3",
                "POÇO 4",
            ],
            "Produção de Óleo (m³)": [
                100.0,
                50.0,
                80.0,
                40.0,
            ],
            "Produção de Gás Associado (Mm³)": [
                10.0,
                5.0,
                8.0,
                4.0,
            ],
            "Produção de Gás Não Associado (Mm³)": [
                2.0,
                1.0,
                3.0,
                1.0,
            ],
        }
    )


@pytest.mark.parametrize(
    ("analysis_function", "plot_function"),
    [
        (
            oil_production_by_month,
            plot_monthly_oil_production,
        ),
        (
            oil_production_by_state,
            plot_oil_by_state,
        ),
        (
            oil_production_by_basin,
            plot_oil_by_basin,
        ),
        (
            oil_production_by_field,
            plot_oil_by_field,
        ),
        (
            oil_production_by_well,
            plot_oil_by_well,
        ),
        (
            oil_gas_by_month,
            plot_oil_vs_gas,
        ),
        (
            oil_heatmap_state_month,
            plot_heatmap_state_month,
        ),
        (
            oil_production_treemap,
            plot_treemap_oil,
        ),
    ],
    ids=[
        "monthly-oil",
        "oil-by-state",
        "oil-by-basin",
        "oil-by-field",
        "oil-by-well",
        "oil-vs-gas",
        "state-month-heatmap",
        "state-field-treemap",
    ],
)
def test_plot_function_returns_valid_figure(
    production_dataframe: pd.DataFrame,
    analysis_function: AnalysisFunction,
    plot_function: PlotFunction,
) -> None:
    """Verifica a criação das figuras utilizadas no dashboard."""

    analysis_result = analysis_function(production_dataframe)
    figure = plot_function(analysis_result)

    assert isinstance(figure, go.Figure)
    assert len(figure.data) > 0
    assert figure.layout.title.text