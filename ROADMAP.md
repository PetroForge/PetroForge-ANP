# ROADMAP — PetroForge-ANP

## Etapa 0 — Planejamento

- [x] Criar o repositório no GitHub
- [x] Configurar o ambiente virtual
- [x] Definir o objetivo e o escopo do projeto
- [x] Definir a estrutura inicial de pastas
- [x] Escolher as principais tecnologias
- [x] Criar os arquivos-base do repositório

## Versão 1 — Coleta, tratamento e análise exploratória

### Leitura e tratamento

- [x] Adicionar o arquivo CSV público da ANP
- [x] Implementar o carregamento dos dados com Pandas
- [x] Interpretar vírgula decimal e ponto de milhar
- [x] Padronizar os nomes das colunas
- [x] Converter a coluna `Mês/Ano` para `datetime`
- [x] Investigar valores ausentes
- [x] Investigar registros repetidos
- [x] Preservar valores ausentes com significado operacional
- [ ] Implementar download automático dos dados da ANP

### Análises de produção

- [x] Produção de óleo por estado
- [x] Produção de óleo por bacia
- [x] Produção de óleo por campo
- [x] Produção de óleo por poço
- [x] Produção mensal de óleo
- [x] Variação percentual mensal
- [x] Produção mensal de óleo e gás
- [x] Produção por estado e mês
- [x] Produção hierárquica por estado e campo
- [x] Calcular participação percentual sobre a produção total
- [x] Preservar categorias ausentes nos agrupamentos
- [x] Diferenciar produção zero de produção ausente

### Indicadores

- [x] Criar módulo de estatísticas gerais
- [x] Criar módulo de KPIs
- [x] Calcular produção total
- [x] Calcular produção média, máxima e mínima
- [x] Contabilizar estados produtores
- [x] Contabilizar bacias, campos e poços
- [x] Criar logger centralizado

## Versão 2 — Visualizações

- [x] Adotar Plotly como biblioteca de visualização
- [x] Criar módulo reutilizável de gráficos
- [x] Criar gráfico de produção mensal
- [x] Criar gráfico de produção por estado
- [x] Criar gráfico de produção por bacia
- [x] Criar gráfico dos principais campos
- [x] Criar gráfico dos principais poços
- [x] Criar comparação mensal entre óleo e gás
- [x] Criar heatmap de produção por estado e mês
- [x] Criar Treemap por estado e campo
- [x] Revisar títulos, unidades e formatação dos gráficos
- [x] Validar a interpretação técnica de cada visualização
- [x] Integrar todos os gráficos ao dashboard

## Versão 3 — Dashboard Streamlit

- [x] Criar a estrutura inicial do dashboard
- [x] Configurar a página do Streamlit
- [x] Adicionar título e descrição do projeto
- [x] Integrar o pipeline de carregamento e limpeza
- [x] Adicionar cache para carregamento e processamento
- [x] Criar cards de KPIs
- [x] Exibir produção total, poços, campos e estados
- [x] Criar formatadores reutilizáveis para os KPIs
- [x] Registrar Plotly e Streamlit nas dependências
- [x] Adicionar todos os gráficos Plotly
- [x] Criar sidebar
- [x] Adicionar filtros em cascata
- [x] Adicionar filtro por estado
- [x] Adicionar filtro por bacia
- [x] Adicionar filtro por campo
- [x] Adicionar filtro por poço
- [x] Adicionar filtro por período
- [x] Exibir inicialmente todo o período disponível
- [x] Validar o intervalo temporal selecionado
- [x] Atualizar KPIs e gráficos dinamicamente
- [x] Tratar combinações de filtros sem resultados
- [x] Exibir a quantidade de registros analisados
- [x] Organizar os gráficos em layout responsivo
- [x] Refinar o layout e a hierarquia visual


## Versão 4 — Refinamento e publicação

- [ ] Revisar desempenho
- [x] Adicionar testes automatizados
- [x] Revisar type hints e docstrings
- [x] Remover código e dependências não utilizados
- [ ] Atualizar o README
- [ ] Documentar a fonte e o período dos dados
- [ ] Documentar instalação e execução
- [ ] Adicionar capturas de tela ou GIF do dashboard
- [ ] Preencher e revisar a licença
- [ ] Preparar o projeto para deploy
- [ ] Publicar o dashboard
- [ ] Preparar a apresentação para LinkedIn e portfólio