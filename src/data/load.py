"""Carregamento dos dados brutos disponibilizados pela ANP."""

from pathlib import Path

import pandas as pd


DATA_PATH: Path = Path(__file__).resolve().parents[2] / "data/raw/producao-mar-2026.csv"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Carrega um arquivo CSV bruto da ANP em um DataFrame."""

    return pd.read_csv(
        path,
        sep=",",
        encoding="utf-8",
        decimal=",",
        thousands=".",
    )
