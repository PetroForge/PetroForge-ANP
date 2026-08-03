import pandas as pd
import pytest

from src.analysis.missing import missing_values_summary


def test_missing_values_summary_calculates_missing_data() -> None:
    """Verifica quantidade, percentual e ordenação das ausências."""

    dataframe = pd.DataFrame(
        {
            "Campo": ["CAMPO A", None, None],
            "Estado": ["Rio de Janeiro", "São Paulo", None],
        }
    )

    result = missing_values_summary(dataframe)

    assert result.index.tolist() == ["Campo", "Estado"]

    assert result.loc["Campo", "Valores Ausentes"] == 2
    assert result.loc["Campo", "Percentual (%)"] == pytest.approx(66.67)

    assert result.loc["Estado", "Valores Ausentes"] == 1
    assert result.loc["Estado", "Percentual (%)"] == pytest.approx(33.33)