"""Testes do catálogo e do cache dos dados marítimos da ANP."""

from pathlib import Path
from urllib.error import URLError

import pytest

from src.data import download


CSV = (
    "[Mês/Ano],[Estado],[Bacia],[Campo],[Poço],[Produção de Óleo (m³)]\n"
    "01/2026,Rio de Janeiro,Santos,TUPI,1-RJS-1,100\n"
).encode("utf-8")
URL = download.DEFAULT_URL


def test_offshore_sources_extracts_official_years(monkeypatch: pytest.MonkeyPatch) -> None:
    html = (
        '<a href="/anp/data/pm/producao-mar-2022.csv">2022</a>'
        '<a href="/anp/data/pm/producao_por_poco_2024.csv">2024</a>'
        '<a href="/anp/data/pm/producao-mar-2025.csv">2025</a>'
        '<a href="/anp/data/pm/producao-mar-2026.csv">2026</a>'
        '<a href="https://example.com/pm/producao-mar-2099.csv">outro</a>'
    ).encode()
    monkeypatch.setattr(download, "_read_url", lambda url: html)

    assert set(download.offshore_sources()) == {2022, 2024, 2025, 2026}


def test_2024_uses_its_official_filename() -> None:
    url = URL.replace("producao-mar-2026.csv", "producao_por_poco_2024.csv")

    assert download._year_from_url(url) == 2024


def test_download_reuses_fresh_cache(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(download, "CACHE_DIR", tmp_path)
    path = tmp_path / "producao-mar-2026.csv"
    path.write_bytes(CSV)
    monkeypatch.setattr(download, "_read_url", lambda url: pytest.fail("download indevido"))

    result = download.get_offshore_file(2026, URL)

    assert result.path == path
    assert result.origin == "cache"


def test_download_replaces_cache_only_after_validation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(download, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(download, "RAW_PATH", tmp_path / "missing.csv")
    monkeypatch.setattr(download, "_read_url", lambda url: CSV)

    result = download.get_offshore_file(2026, URL)

    assert result.origin == "ANP"
    assert result.path.read_bytes() == CSV


def test_download_failure_preserves_previous_copy(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(download, "CACHE_DIR", tmp_path)
    path = tmp_path / "producao-mar-2026.csv"
    path.write_bytes(CSV)
    monkeypatch.setattr(download, "_read_url", lambda url: (_ for _ in ()).throw(URLError("offline")))

    result = download.get_offshore_file(2026, URL, force=True)

    assert result.origin == "cache desatualizado"
    assert path.read_bytes() == CSV


def test_invalid_download_does_not_replace_cache(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(download, "CACHE_DIR", tmp_path)
    path = tmp_path / "producao-mar-2026.csv"
    path.write_bytes(CSV)
    monkeypatch.setattr(download, "_read_url", lambda url: b"<html>erro</html>")

    result = download.get_offshore_file(2026, URL, force=True)

    assert result.origin == "cache desatualizado"
    assert path.read_bytes() == CSV
