"""Dashboard Streamlit para análise da produção brasileira de petróleo."""

import pandas as pd
import streamlit as st

from src.analysis.kpis import ProductionKPIs, production_kpis
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
from src.data.load import load_data
from src.processing.clean import clean_data
from src.utils.formatters import format_integer, format_volume
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


@st.cache_data
def get_data() -> pd.DataFrame:
    """Carrega, limpa e mantém os dados em cache."""

    return clean_data(load_data())


@st.cache_data
def get_kpis(df: pd.DataFrame) -> ProductionKPIs:
    """Calcula e mantém em cache os KPIs do DataFrame informado."""

    return production_kpis(df)

# ==========================
# Configuração da página
# ==========================

st.set_page_config(
    page_title="PetroForge",
    page_icon="🛢️",
    layout="wide"
)

st.title("🛢️ PetroForge")
st.subheader("Dashboard da Produção Brasileira de Petróleo (ANP)")
st.caption(
    "Produção brasileira de petróleo e gás natural com dados públicos da ANP."
)

st.divider()


# ==========================
# Carregamento dos dados
# ==========================

df = get_data()

st.sidebar.markdown("## Filtros")
st.sidebar.caption(
    "Selecione os critérios para atualizar todo o dashboard. Todos os indicadores e gráficos são atualizados automaticamente."
)

estado = st.sidebar.selectbox(
    "Estado",
    ["Todos"] + sorted(df["Estado"].dropna().unique().tolist())
)

df_filtrado = df.copy()

if estado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Estado"] == estado
    ]

bacias = sorted(
    df_filtrado["Bacia"]
    .dropna()
    .unique()
    .tolist()
)

bacia = st.sidebar.selectbox(
    "Bacia",
    ["Todos"] + bacias
)

if bacia != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Bacia"] == bacia
    ]

campos = sorted(
    df_filtrado["Campo"]
    .dropna()
    .unique()
    .tolist()
)

campo = st.sidebar.selectbox(
    "Campo",
    ["Todos"] + campos
)

if campo != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Campo"] == campo
    ]

pocos = sorted(
    df_filtrado["Poço"]
    .dropna()
    .unique()
    .tolist()
)

poco = st.sidebar.selectbox(
    "Poço",
    ["Todos"] + pocos
)

if poco != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Poço"] == poco
    ]

meses = sorted(df["Mês/Ano"].dropna().unique())

meses_dict = {
    mes.strftime("%b/%Y"): mes
    for mes in meses
}

meses_opcoes = list(meses_dict.keys())

inicio_str = st.sidebar.selectbox(
    "Mês inicial",
    meses_opcoes,
)

fim_str = st.sidebar.selectbox(
    "Mês final",
    meses_opcoes,
    index=len(meses_opcoes) - 1,
)

inicio = meses_dict[inicio_str]
fim = meses_dict[fim_str]

if inicio > fim:
    st.sidebar.error(
        "O mês inicial não pode ser maior que o mês final."
    )
    st.stop()

df_filtrado = df_filtrado[
    (df_filtrado["Mês/Ano"] >= inicio)
    & (df_filtrado["Mês/Ano"] <= fim)
]

if df_filtrado.empty:
    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )
    st.stop()

st.sidebar.divider()

kpis = get_kpis(df_filtrado)

st.header("📊 Indicadores")
# ==========================
# KPIs
# ==========================

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Produção Total",
            format_volume(kpis["oil_total_m3"]),
        )

    with col2:
        st.metric(
            "Poços",
            format_integer(kpis["wells"]),
        )

    with col3:
        st.metric(
            "Campos",
            format_integer(kpis["fields"]),
        )

    with col4:
        st.metric(
            "Estados",
            format_integer(kpis["producing_states"]),
        )

    st.caption(
        "Todos os indicadores são atualizados automaticamente "
        "conforme os filtros selecionados."
    )

    st.write(
        f"**Registros analisados:** {len(df_filtrado):,}"
    )

st.divider()

st.header("Visualizações")

state_df = oil_production_by_state(df_filtrado)

basin_df = oil_production_by_basin(df_filtrado)

field_df = oil_production_by_field(df_filtrado)

well_df = oil_production_by_well(df_filtrado)

monthly_df = oil_production_by_month(df_filtrado)

oil_gas_df = oil_gas_by_month(df_filtrado)

heatmap_df = oil_heatmap_state_month(df_filtrado)

treemap_df = oil_production_treemap(df_filtrado)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Produção Mensal")
    st.plotly_chart(
        plot_monthly_oil_production(monthly_df),
        use_container_width=True,
    )

with col2:
    st.subheader("🗺️ Produção por Estado")
    st.plotly_chart(
        plot_oil_by_state(state_df),
        use_container_width=True,
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌊 Produção por Bacia")
    st.plotly_chart(
        plot_oil_by_basin(basin_df),
        use_container_width=True,
    )

with col2:
    st.subheader("🏆 Top Campos Produtores")
    st.plotly_chart(
        plot_oil_by_field(field_df),
        use_container_width=True,
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Poços Produtores")
    st.plotly_chart(
        plot_oil_by_well(well_df),
        use_container_width=True,
    )

with col2:
    st.subheader("Óleo x Gás")
    st.plotly_chart(
        plot_oil_vs_gas(oil_gas_df),
        use_container_width=True,
    )

st.subheader("🔥 Heatmap de Produção")
st.plotly_chart(
    plot_heatmap_state_month(heatmap_df),
    use_container_width=True,
)

st.subheader("🌳 Produção por Estado e Campo")
st.plotly_chart(
     plot_treemap_oil(treemap_df),
    use_container_width=True,
)

st.divider()

st.caption(
    "PetroForge • Dados públicos da ANP • Desenvolvido por Rafael Fernandes"
)