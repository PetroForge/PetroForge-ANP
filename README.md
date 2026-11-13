# PetroForge-ANP

Dashboard de produção marítima de petróleo e gás natural no Brasil, baseado nos [dados abertos oficiais da ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/fase-de-desenvolvimento-e-producao). Reúne coleta automática, tratamento com Pandas, indicadores técnicos e visualizações interativas em Streamlit e Plotly. É o primeiro módulo do ecossistema PetroForge.

## Escopo

O dashboard utiliza os arquivos anuais de **produção em mar**, não a produção terrestre ou toda a produção nacional. O filtro de ano escolhe o arquivo da ANP; mês, estado, bacia, campo e poço são filtros locais e não provocam download a cada clique. A produção por poço representa a soma dos registros no período escolhido, não uma taxa diária.

A ANP publica dados com defasagem e pode revisar um arquivo já disponível. Confira o período efetivo apresentado no filtro. As unidades seguem as colunas de origem: óleo em m³, gás associado e não associado em Mm³. Consulte também os [metadados da ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/producao-de-petroleo-e-gas-natural-por-poco).

## Instalação e execução no Windows

Requer Python 3.11 ou versão compatível. No PowerShell:

```powershell
git clone https://github.com/PetroForge/PetroForge-ANP.git
cd PetroForge-ANP
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run src/dashboard/app.py
```

Para executar os testes:

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Fonte e atualização

O aplicativo consulta a [página oficial da ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/fase-de-desenvolvimento-e-producao) para descobrir os arquivos anuais no formato suportado (2022 em diante). Selecione um ano inicial e um final para construir uma linha do tempo contínua, inclusive para acompanhar o mesmo poço entre 2025 e 2026. Os arquivos do intervalo são baixados quando não há cópia local recente. O cache em `data/cache/` não é versionado e tem validade de 24 horas; o botão **Atualizar dados da ANP** força uma nova tentativa. O cache em memória do Streamlit expira em uma hora.

Se a ANP estiver indisponível, a aplicação usa a última cópia válida. Para 2026 existe também uma fotografia em `data/raw/producao-mar-2026.csv`. A interface informa a origem utilizada. A primeira consulta de outro ano exige internet. O histórico anterior a 2022 usa formatos diferentes, ainda não compatibilizados.

## Estrutura

```text
src/data/           catálogo, download, cache e leitura
src/processing/     limpeza e tipagem
src/analysis/       agrupamentos e indicadores
src/visualization/  gráficos Plotly
src/dashboard/      interface Streamlit e filtros
src/utils/          formatação
tests/              testes automatizados
data/raw/           fotografia de referência
data/cache/         downloads locais (ignorados pelo Git)
```

## Limitações e próximos passos

- A produção em terra é publicada em arquivos trimestrais e exige integração própria.
- Em hospedagens com disco temporário, o cache pode ser refeito após reiniciar a instância.
- Publicação do dashboard, capturas de tela e portal do ecossistema serão etapas próprias.

Veja o [ROADMAP.md](ROADMAP.md). O código do PetroForge-ANP é de autoria de Rafael Fernandes. Nenhuma licença de reutilização do código é concedida neste momento. Os dados de produção são disponibilizados pela ANP e devem ser atribuídos à fonte oficial.
