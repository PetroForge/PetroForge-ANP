"""Visualizações Plotly para as análises de produção."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _pad_bar_axis(fig: go.Figure, values: pd.Series) -> None:
    """Reserva espaço à direita para os percentuais fora das barras."""

    maximum = values.max()
    if pd.notna(maximum) and maximum > 0:
        fig.update_xaxes(range=[0, float(maximum) * 1.22])
    fig.update_layout(margin=dict(r=65))
    fig.update_traces(cliponaxis=False)


def _add_share_column(
    fig: go.Figure,
    data: pd.DataFrame,
    category: str,
) -> None:
    """Desenha os percentuais em uma coluna dentro da área do gráfico."""

    maximum = data["Produção de Óleo (m³)"].max()
    if pd.isna(maximum) or maximum <= 0:
        return
    fig.update_traces(text=None, texttemplate=None)
    fig.update_xaxes(range=[0, float(maximum) * 1.3])
    for _, row in data.iterrows():
        share = row["Participação (%)"]
        label = f"{share:.2f}%" if pd.notna(share) else "n/d"
        fig.add_annotation(
            x=float(maximum) * 1.27,
            y=row[category],
            text=label,
            showarrow=False,
            xanchor="right",
            font=dict(color="#E5E7EB", size=12),
        )


def plot_monthly_oil_production(
    monthly_df: pd.DataFrame,
) -> go.Figure:
    """Cria o gráfico da produção mensal de óleo."""

    fig = px.line(
        monthly_df,
        x="Mês/Ano",
        y="Produção de Óleo (m³)",
        markers=True,
        title="Produção Mensal de Óleo",
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Produção (m³)",
        template="plotly_white",
    )

    return fig


def plot_oil_by_state(
    states_df: pd.DataFrame,
) -> go.Figure:
    """Cria o gráfico da produção de óleo por estado."""

    fig = px.bar(
        states_df,
        x="Produção de Óleo (m³)",
        y="Estado",
        orientation="h",
        title="Produção de Óleo por Estado",
        text="Produção de Óleo (m³)",
    )

    fig.update_layout(
        xaxis_title="Produção (m³)",
        yaxis_title="",
        template="plotly_white",
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
    )

    _pad_bar_axis(fig, states_df["Produção de Óleo (m³)"])

    return fig


def plot_oil_by_field(
    field_df: pd.DataFrame,
) -> go.Figure:
    """Cria o gráfico dos campos com maior produção de óleo."""

    fig = px.bar(
        field_df,
        x="Produção de Óleo (m³)",
        y="Campo",
        orientation="h",
        title="Top 10 Campos Produtores",
        text="Participação (%)",
    )

    fig.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Produção de Óleo (m³)",
        yaxis_title="Campo",
    )

    _pad_bar_axis(fig, field_df["Produção de Óleo (m³)"])
    _add_share_column(fig, field_df, "Campo")

    return fig


def plot_oil_by_basin(
    basin_df: pd.DataFrame,
) -> go.Figure:
    """Cria o gráfico da produção de óleo por bacia."""

    fig = px.bar(
        basin_df,
        x="Produção de Óleo (m³)",
        y="Bacia",
        orientation="h",
        title="Produção de Óleo por Bacia",
        text="Participação (%)",
    )

    fig.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"},
    )

    _pad_bar_axis(fig, basin_df["Produção de Óleo (m³)"])
    _add_share_column(fig, basin_df, "Bacia")

    return fig


def plot_oil_by_well(
    well_df: pd.DataFrame,
) -> go.Figure:
    """Cria o gráfico dos poços com maior produção de óleo."""

    fig = px.bar(
        well_df,
        x="Produção de Óleo (m³)",
        y="Poço",
        orientation="h",
        text="Participação (%)",
        title="Top 15 Poços Produtores",
    )

    fig.update_layout(
        template="plotly_white",
        yaxis={"categoryorder": "total ascending"},
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    _pad_bar_axis(fig, well_df["Produção de Óleo (m³)"])

    return fig


def plot_oil_vs_gas(
    monthly_df: pd.DataFrame,
) -> go.Figure:
    """Cria a comparação mensal entre as produções de óleo e gás."""

    fig = px.line(
        monthly_df,
        x="Mês/Ano",
        y=[
            "Produção de Óleo (m³)",
            "Produção Total de Gás (Mm³)",
        ],
        markers=True,
        title="Produção Mensal de Óleo x Gás",
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Mês",
    )

    return fig


def plot_heatmap_state_month(
    heatmap_df: pd.DataFrame,
) -> go.Figure:
    """Cria o Heatmap da produção de óleo por estado e mês."""

    fig = px.imshow(
        heatmap_df,
        aspect="auto",
        text_auto=".2s",
        title="Produção de Óleo por Estado e Mês",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        template="plotly_white",
    )

    return fig


def plot_treemap_oil(
    treemap_df: pd.DataFrame,
) -> go.Figure:
    """Cria o Treemap da produção de óleo por estado e campo."""

    fig = px.treemap(
        treemap_df,
        path=["Estado", "Campo"],
        values="Produção de Óleo (m³)",
        color="Produção de Óleo (m³)",
        color_continuous_scale="Blues",
        title="Produção de Óleo por Estado e Campo",
    )

    fig.update_layout(
        template="plotly_white",
    )

    return fig
