"""Análises de valores ausentes nos dados de produção."""

import pandas as pd


def missing_values_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Resume quantidade e percentual de valores ausentes por coluna."""

    summary = pd.DataFrame(
        {
            "Valores Ausentes": df.isna().sum(),
            "Percentual (%)": (
                df.isna()
                .mean()
                .mul(100)
                .round(2)
            ),
        }
    )

    return summary.sort_values(
        by="Valores Ausentes",
        ascending=False,
    )