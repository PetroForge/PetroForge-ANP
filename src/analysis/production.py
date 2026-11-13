"""Agregações de produção utilizadas nas análises e visualizações."""

import pandas as pd


def oil_production_by(
    df: pd.DataFrame,
    group_by: str,
    top_n: int | None = None,
) -> pd.DataFrame:
    """Agrega produção de óleo e participação por categoria."""

    oil_column = "Produção de Óleo (m³)"

    production = (
        df.groupby(group_by, dropna=False)[oil_column]
        .sum(min_count=1)
        .reset_index()
        .sort_values(oil_column, ascending=False)
        .reset_index(drop=True)
    )

    total = production[oil_column].sum(min_count=1)

    if pd.isna(total) or total == 0:
        production["Participação (%)"] = pd.NA
    else:
        production["Participação (%)"] = (
            production[oil_column]
            .div(total)
            .mul(100)
            .round(2)
        )

    if top_n is not None:
        production = production.head(top_n).copy()

    return production.reset_index(drop=True)


def oil_production_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega a produção mensal, preservando lacunas sem presumir volume zero."""

    production = (
        df.groupby("Mês/Ano")["Produção de Óleo (m³)"]
        .sum()
        .reset_index()
        .sort_values("Mês/Ano")
    )

    months = pd.date_range(
        production["Mês/Ano"].min(),
        production["Mês/Ano"].max(),
        freq="MS",
    )
    production = (
        production.set_index("Mês/Ano")
        .reindex(months)
        .rename_axis("Mês/Ano")
        .reset_index()
    )

    production["Variação (%)"] = (
        production["Produção de Óleo (m³)"]
        .pct_change(fill_method=None)
        .mul(100)
        .round(2)
    )

    return production


def oil_production_by_well(
    df: pd.DataFrame,
    top_n: int | None = 15,
) -> pd.DataFrame:
    """Retorna o ranking dos poços com maior produção de óleo."""

    return oil_production_by(
        df,
        group_by="Poço",
        top_n=top_n,
    )


def oil_gas_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega mensalmente as produções de óleo e gás."""

    production = (
        df.groupby("Mês/Ano")[
            [
                "Produção de Óleo (m³)",
                "Produção de Gás Associado (Mm³)",
                "Produção de Gás Não Associado (Mm³)",
            ]
        ]
        .sum(min_count=1)
        .reset_index()
        .sort_values("Mês/Ano")
    )

    production["Produção Total de Gás (Mm³)"] = (
        production["Produção de Gás Associado (Mm³)"].fillna(0)
        + production["Produção de Gás Não Associado (Mm³)"].fillna(0)
    )

    return production


def oil_heatmap_state_month(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna a matriz de produção de óleo por estado e mês."""

    heatmap = (
        df.groupby(
            ["Estado", "Mês/Ano"],
            dropna=False,
        )["Produção de Óleo (m³)"]
        .sum(min_count=1)
        .reset_index()
    )

    return heatmap.pivot(
        index="Estado",
        columns="Mês/Ano",
        values="Produção de Óleo (m³)",
    )


def oil_production_treemap(df: pd.DataFrame) -> pd.DataFrame:
    """Prepara a hierarquia de produção por estado e campo."""

    treemap = (
        df.groupby(
            ["Estado", "Campo"],
            dropna=False,
        )["Produção de Óleo (m³)"]
        .sum(min_count=1)
        .reset_index()
    )

    return treemap.dropna(
        subset=["Estado", "Campo"],
    )


def oil_production_by_state(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna a produção de óleo agrupada por estado."""

    return oil_production_by(
        df,
        group_by="Estado",
    )


def oil_production_by_basin(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna a produção de óleo agrupada por bacia."""

    return oil_production_by(
        df,
        group_by="Bacia",
    )


def oil_production_by_field(
    df: pd.DataFrame,
    top_n: int | None = 10,
) -> pd.DataFrame:
    """Retorna o ranking dos campos com maior produção de óleo."""

    return oil_production_by(
        df,
        group_by="Campo",
        top_n=top_n,
    )
