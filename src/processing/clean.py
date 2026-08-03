"""Etapas de limpeza e padronização dos dados da ANP."""

import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Remove colchetes e espaços dos nomes das colunas."""

    df.columns = (
        df.columns
        .str.replace("[", "", regex=False)
        .str.replace("]", "", regex=False)
        .str.strip()
    )

    return df


def convert_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Converte a coluna Mês/Ano para o tipo datetime."""

    df["Mês/Ano"] = pd.to_datetime(
        df["Mês/Ano"],
        format="%m/%Y",
    )

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Executa sequencialmente todas as etapas de limpeza."""

    df = clean_column_names(df)
    df = convert_date_column(df)

    return df