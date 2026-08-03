"""Indicadores gerais da produção de petróleo."""

from typing import TypedDict

import pandas as pd


class ProductionKPIs(TypedDict):
    """Estrutura dos indicadores consumidos pelo dashboard."""

    oil_total_m3: float
    oil_average_m3: float
    oil_maximum_m3: float
    oil_minimum_m3: float
    producing_states: int
    basins: int
    fields: int
    wells: int


def production_kpis(df: pd.DataFrame) -> ProductionKPIs:
    """Calcula os principais indicadores de produção."""

    oil = df["Produção de Óleo (m³)"]

    producing_states = (
        df.loc[oil > 0, "Estado"]
        .dropna()
        .nunique()
    )

    return {
        "oil_total_m3": float(oil.sum()),
        "oil_average_m3": float(oil.mean()),
        "oil_maximum_m3": float(oil.max()),
        "oil_minimum_m3": float(oil.min()),
        "producing_states": int(producing_states),
        "basins": int(df["Bacia"].nunique()),
        "fields": int(df["Campo"].nunique()),
        "wells": int(df["Poço"].nunique()),
    }