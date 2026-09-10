# Hackathon Jovens Talentos AI Builder — Seazone


## Link do Vídeo 

https://drive.google.com/file/d/1cGT1vfXav85NNuXM1tORG09AUGGoG52t/view?usp=sharing

Este projeto analisa dados do mercado imobiliário de **Itapema - SC** para identificar oportunidades de investimento para a Seazone.

A análise utiliza as bases fornecidas no desafio, processamento em Python e apoio de Inteligência Artificial para exploração, tratamento, análise e interpretação dos dados.


## Perguntas do desafio

A análise responde às quatro perguntas propostas:

1. Qual o melhor perfil de imóvel para investir?
2. Qual a melhor localização em termos de receita?
3. Quais características dos imóveis devem ser consideradas?
4. Se fosse necessário investir hoje, qual imóvel/perfil eu compraria e por quê?

As análises detalhadas e os resultados estão disponíveis na pasta `reports/`.


## Dados utilizados

As bases originais utilizadas no desafio estão na pasta `data/`.

Também foi consultada a documentação/metodologia de métricas disponibilizada pela própria Seazone para auxiliar na interpretação e no cálculo dos indicadores utilizados na análise.

Quando aplicável, as fontes e premissas utilizadas são identificadas nos respectivos relatórios.

## Metodologia

O processo de análise foi dividido nas seguintes etapas:

1. Auditoria e entendimento das bases;
2. Tratamento e organização dos dados;
3. Construção da base analítica;
4. Análise de demanda;
5. Análise de preços;
6. Cruzamento entre oferta, demanda e preços;
7. Estimativa de receita;
8. Análise de retorno;
9. Comparação entre perfis e localidades;
10. Definição dos critérios para decisão de investimento;
11. Avaliação da tese de apartamentos compactos no Centro.

Durante a análise, os resultados foram classificados entre **dados observados, cálculos, premissas e interpretações**, evitando tratar estimativas como dados reais.


## Como executar

Os scripts da pasta `analysis/` estão organizados por etapas. Para reproduzir a análise, execute os comandos abaixo **na ordem apresentada**, a partir da raiz do repositório.

### Auditoria dos dados

```bash
py analysis/audit.py
```


### Construção da base analítica

```bash
py analysis/resumir_precos.py
py analysis/criar_base_analitica.py
```


### Visualizações

```bash
py analysis/visualizar_dados.py
py analysis/visualizar_html.py
py analysis/visualizar_precos.py
```


### Pergunta 1 — Melhor perfil de imóvel

```bash
py analysis/analise_demanda.py
py analysis/cruzar_demanda_preco.py
py analysis/analisar_vivareal.py
py analysis/analisar_cruzamento_compra_aluguel.py
py analysis/analisar_receita.py
py analysis/analisar_roi.py
```


### Pergunta 2 — Melhor localização

```bash
py analysis/analisar_localizacao_receita.py
```


### Pergunta 3 — Características relevantes

```bash
py analysis/analisar_caracteristicas_receita.py
```


### Pergunta 4 — Decisão de investimento

```bash
py analysis/analisar_candidatos_investimento.py
py analysis/analisar_decisao_criterios.py
py analysis/analisar_tese_compactos_centro.py
py analysis/analisar_tese_independente.py
```


## Resultados

Os resultados detalhados das análises estão disponíveis na pasta `reports/`.


### Pergunta 1 — Melhor perfil

A resposta e os cálculos utilizados para identificar o perfil mais adequado estão documentados nos relatórios gerados a partir das análises de demanda, receita e retorno.


### Pergunta 2 — Melhor localização

A comparação entre as localidades é apresentada na análise de receita por localização.


### Pergunta 3 — Características

A análise avalia as características dos imóveis relacionadas ao potencial de receita e ao perfil de investimento.


### Pergunta 4 — Decisão de investimento

A decisão final considera o equilíbrio entre:

* eficiência do capital investido;
* receita potencial;
* volume de imóveis;
* disponibilidade de dados;
* sinais de demanda;
* possibilidade de escala;
* robustez da amostra;
* riscos e limitações dos dados.

A análise detalhada está nos relatórios de decisão de investimento.


## Tese dos compactos no Centro

Foi realizada uma análise específica da tese:

> **"Apartamentos compactos (studio/1 quarto) no Centro são a aposta mais eficiente."**

A conclusão foi de que **os dados não sustentam a tese como a alternativa mais eficiente de forma geral**.

O 1 quarto no Centro apresenta retorno bruto estimado de **10,92%**, praticamente empatado com 2 quartos no Centro (**10,89%**). Entretanto, existem limitações importantes de volume de imóveis à venda e ausência de dados suficientes para avaliar studios.

Além disso, outros perfis apresentam retorno superior, como **1 quarto em Meia Praia (11,94%)** e **2 quartos em Morretes (13,62%)**.

A análise completa está disponível em:

* `reports/relatorio_tese_compactos_centro.md`
* `reports/relatorio_tese_independente.md`


## Premissas e limitações

As análises diferenciam dados observados de valores calculados e premissas utilizadas.

Entre as principais limitações:

* não há dados observados de ocupação nas bases utilizadas;
* a ocupação de 60%, quando utilizada, é uma **premissa para estimativa**, não um dado observado;
* receita e retorno estimados dependem dessas premissas;
* algumas categorias possuem amostras pequenas;
* Airbnb e dados de venda representam mercados diferentes e não devem ser somados como se fossem o mesmo universo;
* a ausência de dados suficientes para determinados perfis impede conclusões robustas.

Essas limitações foram consideradas na definição da recomendação final.

---

## Como executar as análises

Tabela resumida dos 18 scripts disponíveis em `analysis/`, com suas perguntas associadas, comandos de execução, entradas e saídas:

| Script | Pergunta | Comando para executar | Entrada | Saída |
|--------|----------|----------------------|---------|-------|
| `audit.py` | Auditoria | `py analysis/audit.py` | `data/` (5 CSVs) | `reports/00_auditoria/relatorio_auditoria.md` |
| `resumir_precos.py` | P1 | `py analysis/resumir_precos.py` | `Price_AV_Itapema.csv` | `price_por_anuncio.csv` (1005 linhas) |
| `criar_base_analitica.py` | P1 | `py analysis/criar_base_analitica.py` | `price_por_anuncio.csv` + Details + Mesh | `base_analitica_itapema.csv` (4441 linhas, 51 cols) |
| `analise_demanda.py` | P1 | `py analysis/analise_demanda.py` | `base_analitica_itapema.csv` | `relatorio_demanda.md` |
| `cruzar_demanda_preco.py` | P1 | `py analysis/cruzar_demanda_preco.py` | `base_analitica_itapema.csv` | `relatorio_demanda_preco.md` |
| `analisar_vivareal.py` | P1 | `py analysis/analisar_vivareal.py` | `VivaReal_Itapema.csv` | `relatorio_vivareal.md` |
| `analisar_receita.py` | P1 | `py analysis/analisar_receita.py` | `base_analitica_itapema.csv` | `relatorio_receita.md` |
| `analisar_roi.py` | P1 | `py analysis/analisar_roi.py` | `base_analitica_itapema.csv` + VivaReal | `roi_perfil.csv` (15 linhas) |
| `analisar_caracteristicas_receita.py` | P3 | `py analysis/analisar_caracteristicas_receita.py` | `base_analitica_itapema.csv` | `relatorio_caracteristicas_receita.md` |
| `analisar_localizacao_receita.py` | P2 | `py analysis/analisar_localizacao_receita.py` | `base_analitica_itapema.csv` + VivaReal | `relatorio_localizacao_receita.md` + `localizacao_receita.csv` |
| `visualizar_dados.py` | Todas | `py analysis/visualizar_dados.py` | 5 CSVs em `data/` | `visualizacao_dados.html` |
| `visualizar_html.py` | Todas | `py analysis/visualizar_html.py` | 5 CSVs em `data/` | `visualizacao_dados.html` |
| `visualizar_precos.py` | P1 | `py analysis/visualizar_precos.py` | `price_por_anuncio.csv` | `visualizacao_precos.html` |
| `analisar_candidatos_investimento.py` | P4 | `py analysis/analisar_candidatos_investimento.py` | `base_analitica_itapema.csv` + VivaReal | `relatorio_candidatos_investimento.md` + `candidatos_investimento.csv` |
| `analisar_decisao_criterios.py` | P4 | `py analysis/analisar_decisao_criterios.py` | `base_analitica_itapema.csv` | `relatorio_criterios_investimento.md` |
| `analisar_tese_independente.py` | P4 | `py analysis/analisar_tese_independente.py` | `base_analitica_itapema.csv` + VivaReal | `relatorio_tese_independente.md` + `tese_independente.csv` |
| `analisar_tese_compactos_centro.py` | P4 | `py analysis/analisar_tese_compactos_centro.py` | `base_analitica_itapema.csv` + VivaReal | `relatorio_tese_compactos_centro.md` + `tese_compactos_centro.csv` |

**Observações gerais:**

- Nenhum script altera arquivos em `data/`. Todos os CSVs de entrada permanecem intactos.
- A ordem recomendada de execução respeita as dependências: `audit.py` → `resumir_precos.py` → `criar_base_analitica.py` → scripts das perguntas 1‑4.
- Os cenários de receita (40 % / 60 % / 80 %) utilizam a premissa de **ocupação de 60 % (18 dias/mês)**, que é hipotética e não um dado observado nas bases.
- Para rodar todos os scripts da raiz do repositório: `py analysis/*.py` (na ordem desejada).

## Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como parte do processo de desenvolvimento e análise para:

* explorar as bases de dados;
* auxiliar na criação e revisão dos scripts;
* identificar e calcular métricas;
* formular e testar hipóteses;
* questionar resultados;
* identificar inconsistências;
* revisar interpretações;
* apoiar a organização das conclusões.

O histórico completo das interações com a IA está disponível na pasta:

```text
ai-log/
```

O objetivo do registro é permitir a avaliação do processo de trabalho, incluindo as iterações, obstáculos, questionamentos, correções e decisões tomadas durante a análise.


## Estrutura do projeto

```text
├── data/
│   └── Bases utilizadas
│
├── analysis/
│   └── Scripts de análise
│
├── reports/
│   └── Relatórios e resultados
│
├── ai-log/
│   └── Histórico das interações com IA
│
└── README.md
```

## Tecnologias utilizadas

* Python
* Pandas
* CSV
* Git
* GitHub
* Inteligência Artificial Generativa
