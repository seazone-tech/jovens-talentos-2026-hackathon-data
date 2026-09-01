
## Pergunta 3 — Quais características explicam as melhores receitas?

Os dados indicam que **número de quartos e área do imóvel estão associados a maiores receitas estimadas**, principalmente porque imóveis maiores tendem a apresentar diárias históricas mais altas.

Em Meia Praia, a receita anual estimada a 60% de ocupação aumenta de aproximadamente **R$ 99,4 mil em imóveis de 2 quartos**, para **R$ 151,2 mil em 3 quartos** e **R$ 232,2 mil em 4 quartos**. As áreas medianas também aumentam, de **85 m² para 129 m² e 188 m²**, respectivamente.

Ao mesmo tempo, os dados sugerem **retorno decrescente**: de 2 para 3 quartos, o preço de compra aumenta cerca de 75%, enquanto a receita cresce 52%; de 3 para 4 quartos, o preço aumenta 91%, contra 53% de crescimento da receita. Essa é uma tendência observada nos dados, e não uma relação causal.

Assim, **imóveis maiores e com mais quartos apresentam maior potencial de receita**, mas o aumento do investimento não gera crescimento proporcional da receita. Considerando também volume e robustez dos dados, **3 quartos em Meia Praia se destaca como o perfil mais equilibrado**, enquanto 4 quartos apresenta maior receita estimada, porém em um segmento menor.

## Onde conferir / Evidências

- **Receita anual estimada 2q: R$ 99,4 mil; 3q: R$ 151,2 mil; 4q: R$ 232,2 mil** (60% ocupação): tabela completa em `reports/03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md:7–13` (linhas 9–13).
- **Diária mediana: 2q R$ 460; 3q R$ 700; 4q R$ 1075** — `reports/03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md:9–13`; cálculo `median(price_mediano)` por segmento em `analysis/analisar_caracteristicas_receita.py`.
- **Área mediana: 85 m² (2q); 129 m² (3q); 188 m² (4q)** — `reports/03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md:7`; fonte `data/VivaReal_Itapema.csv` `usable_area` por perfil (proxy por quartos); correlação área-diária r=0,98 — `:37` do relatório.
- **Preço compra mediano: 2q R$ 1,07M; 3q R$ 1,88M; 4q R$ 3,6M** — `reports/03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md:9–13`; fonte `reports/01_pergunta1_perfil/cruzamento_perfil.csv:2–6` (coluna `preco_compra_mediano`); também `data/VivaReal_Itapema.csv`.
- **Retorno decrescente 2→3 quartos**: preço +75% (1,07M→1,88M) vs receita +52% (99k→151k) — `reports/03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md:49` (linha 49).
- **Retorno decrescente 3→4 quartos**: preço +91% (1,88M→3,6M) vs receita +53% (151k→232k) — `:49` (linha 49).
- **Classificação por força da evidência** (tabela final do relatório): `reports/03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md:75–86` — quartos (forte), área (forte), diária (forte), localização (moderada), preço compra (moderada), demanda/reviews (moderada), condomínio/IPTU (insuficiente).
- **Hipótese: maior receita vs melhor perfil econômico** — `:107–111` do relatório: 4q tem maior receita bruta (232k), mas 3q/2q têm melhor equilíbrio receita+preço+volume.
- **Script gerador**: `analysis/analisar_caracteristicas_receita.py` — gera `relatorio_caracteristicas_receita.md` e `caracteristicas_receita.csv`.
- **Premissa de ocupação 60% (18 dias/mês)**: explicitada em todos os relatórios (P1, P2, P3, P4) como hipótese, não dado observado.
- **Base Viva usada como proxy de área para Airbnb**: `:130–131` do relatório — `data/VivaReal_Itapema.csv` `usable_area` não disponível em base Airbnb; usada por perfil (ex: 2q MP 85m², 3q 129m²).

