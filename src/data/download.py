"""Descoberta e cache dos CSVs oficiais de produção marítima da ANP."""

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "producao-mar-2026.csv"
CACHE_DIR = PROJECT_ROOT / "data" / "cache"
CATALOG_URL = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
    "fase-de-desenvolvimento-e-producao"
)
DEFAULT_URL = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
    "arquivos/arquivos-fase-de-desenvolvimento-e-producao/"
    "arquivos-producao-de-petroleo-e-gas-natural-nacional/"
    "pm/producao-mar-2026.csv"
)
CACHE_MAX_AGE_SECONDS = 24 * 60 * 60
REQUIRED_COLUMNS = {
    "[Mês/Ano]", "[Estado]", "[Bacia]", "[Campo]", "[Poço]",
    "[Produção de Óleo (m³)]",
}
FILE_PATTERN = re.compile(
    r"/pm/(?:producao-mar-(\d{4})|producao_por_poco_(2024))\.csv(?:$|[/?#])", re.I
)


def _year_from_url(url: str) -> int | None:
    """Extrai o ano dos dois padrões de nome usados desde 2022."""

    match = FILE_PATTERN.search(url)
    return int(match.group(1) or match.group(2)) if match else None


class AnpDataError(RuntimeError):
    """Falha na obtenção ou validação de dados da ANP."""


@dataclass(frozen=True)
class DataFile:
    """Arquivo selecionado e sua proveniência."""

    path: Path
    origin: str
    url: str


class _CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def _read_url(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "PetroForge-ANP/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def offshore_sources() -> dict[int, str]:
    """Obtém os CSVs anuais no esquema atual da página da ANP."""

    parser = _CatalogParser()
    parser.feed(_read_url(CATALOG_URL).decode("utf-8"))
    sources: dict[int, str] = {}
    for href in parser.links:
        url = urljoin(CATALOG_URL, href)
        year = _year_from_url(url)
        if year and year >= 2022 and urlparse(url).hostname == "www.gov.br":
            sources[year] = url.removesuffix("/view")
    if not sources:
        raise AnpDataError("A página da ANP não apresentou arquivos marítimos.")
    return sources


def available_sources() -> dict[int, str]:
    """Combina o catálogo online com os anos armazenados localmente."""

    try:
        sources = offshore_sources()
    except (HTTPError, URLError, TimeoutError, UnicodeError, AnpDataError):
        sources = {}
    for cached_file in CACHE_DIR.glob("producao-mar-*.csv"):
        match = re.fullmatch(r"producao-mar-(\d{4})\.csv", cached_file.name)
        if match and int(match.group(1)) >= 2022:
            year = int(match.group(1))
            filename = "producao_por_poco_2024.csv" if year == 2024 else f"producao-mar-{year}.csv"
            sources.setdefault(year, DEFAULT_URL.replace("producao-mar-2026.csv", filename))
    sources.setdefault(2026, DEFAULT_URL)
    return sources


def _validate_csv(path: Path) -> None:
    """Rejeita respostas vazias ou arquivos com esquema inesperado."""

    if path.stat().st_size == 0:
        raise AnpDataError("O arquivo da ANP está vazio.")
    columns = set(pd.read_csv(path, nrows=0, encoding="utf-8").columns)
    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise AnpDataError(f"Colunas ausentes no arquivo da ANP: {sorted(missing)}")
    if pd.read_csv(path, nrows=1, encoding="utf-8").empty:
        raise AnpDataError("O arquivo da ANP não contém registros.")


def get_offshore_file(year: int, url: str, *, force: bool = False) -> DataFile:
    """Atualiza o CSV anual e preserva a última cópia válida se a ANP falhar."""

    source_year = _year_from_url(url)
    if source_year is None or urlparse(url).hostname != "www.gov.br":
        raise AnpDataError("Endereço de dados da ANP inválido.")
    if source_year != year:
        raise AnpDataError("Ano do arquivo diferente do ano solicitado.")

    path = CACHE_DIR / f"producao-mar-{year}.csv"
    if path.is_file() and not force and time.time() - path.stat().st_mtime < CACHE_MAX_AGE_SECONDS:
        return DataFile(path, "cache", url)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".csv.tmp")
    try:
        temporary.write_bytes(_read_url(url))
        _validate_csv(temporary)
        temporary.replace(path)
        return DataFile(path, "ANP", url)
    except (HTTPError, URLError, TimeoutError, OSError, UnicodeError, pd.errors.ParserError, AnpDataError) as exc:
        temporary.unlink(missing_ok=True)
        if path.is_file():
            return DataFile(path, "cache desatualizado", url)
        if year == 2026 and RAW_PATH.is_file():
            return DataFile(RAW_PATH, "amostra incluída no projeto", url)
        raise AnpDataError(f"Não foi possível obter os dados de {year} da ANP.") from exc
