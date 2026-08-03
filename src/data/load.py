"""Carregamento dos dados brutos disponibilizados pela ANP."""

from pathlib import Path

import pandas as pd


DATA_PATH: Path = Path("data/raw/producao-mar-2026.csv")


def load_data() -> pd.DataFrame:
    """Carrega o arquivo CSV bruto da ANP em um DataFrame."""

    return pd.read_csv(
        DATA_PATH,
        sep=",",
        encoding="utf-8",
        decimal=",",
        thousands=".",
    )