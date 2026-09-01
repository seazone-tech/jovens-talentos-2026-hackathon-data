## Pergunta 4 - Se a Seazone fosse investir hoje, o que você compraria e por quê?

Se a Seazone fosse investir hoje, eu escolheria um **apartamento de 3 quartos em Meia Praia**. A decisão não considera apenas o maior retorno percentual, mas o equilíbrio entre **receita, volume de mercado, escala e robustez dos dados**.

O preço de compra mediano observado para esse perfil é de aproximadamente **R$ 1,88 milhão**, com diária histórica mediana de **R$ 700**. Considerando uma premissa de **60% de ocupação**, ou 18 dias por mês, a receita bruta anual estimada seria:

**R$ 700 × 18 dias × 12 meses = R$ 151.200 por ano.**

Isso representa um **retorno bruto estimado de aproximadamente 8,02% ao ano** sobre o valor de compra. Considerando as premissas de condomínio, IPTU, limpeza e comissão utilizadas na análise, o **ROI líquido estimado fica em aproximadamente 5,67% ao ano**, com payback simples de cerca de **17,6 anos**.

A escolha também é sustentada pelo volume: o perfil de 3 quartos em Meia Praia possui **1.451 anúncios de Airbnb**, sendo **327 com diária disponível**, o que oferece uma base mais robusta para a estimativa. Além disso, Meia Praia apresenta volume muito superior ao Centro, enquanto as receitas estimadas dos dois bairros são próximas.

Eu não escolheria o apartamento de 4 quartos, apesar de apresentar a maior receita estimada (**R$ 232,2 mil/ano**), porque existem apenas **60 imóveis com preço disponível** nesse perfil, tornando a estimativa menos robusta e indicando um segmento mais específico. Já o 2 quartos apresenta maior retorno percentual, mas gera uma receita menor e representa uma oportunidade de menor escala.

Portanto, minha recomendação seria **3 quartos em Meia Praia**, não por apresentar o maior ROI isolado, mas por oferecer o melhor **equilíbrio entre potencial de receita, escala de mercado e confiabilidade dos dados**.

Essa estimativa deve ser interpretada como um cenário de referência, pois a ocupação de 60% é uma premissa e os dados de venda e aluguel não possuem correspondência individual entre os imóveis.

## Onde conferir / Evidências

- **Receita bruta anual estimada R$ 151.200**: cálculo `700 × 18 × 12` — `reports/04_pergunta4_investimento/relatorio_candidatos_investimento.md:7`; tabela detalhada (40/60/80% occupancy) em `:19–25`.
- **Retorno bruto estimado 8,02%**: cálculo `receita_ano / preço_compra × 100` — `relatorio_candidatos_investimento.md:9` (linha 8 tabela); também `relatorio_criterios_investimento.md:35` (score final 62 para 3q MP).
- **ROI líquido estimado 5,67%**: considera custos de condomínio (R$ 600/ano), IPTU (R$ 1.500/ano), cleaning (R$ 12.960/ano via fee 300 * 43,2 limp) e comissão 15% — `relatorio_roi.md:39–43` (tabela de custos por perfil); `relatorio_candidatos_investimento.md:9`; premissa explicada em `:89–99` (DADO vs CÁLCULO vs PREMISSA vs INTERPRETAÇÃO).
- **Payback simples ~17,6 anos**: cálculo `preço_compra / lucro_ano` — `relatorio_roi.md:59` (linha 59 tabela); `relatorio_candidatos_investimento.md:49` score 62.
- **Volume: 1.451 anúncios Airbnb e 327 com diária**: `relatorio_candidatos_investimento.md:13` (tabela 5 perfis, linha 3q MP); `relatorio_criterios_investimento.md:35` (score 100 em volume para 3q MP com 1704+1451); origem `data/Details_Itapema.csv` via LEFT JOIN para base analítica.
- **Preço compra mediano R$ 1,884,860**: `cruzamento_perfil.csv:3` (3q Meia Praia); `data/VivaReal_Itapema.csv` coluna `sale_price` median por perfil.
- **2q Centro ROI 7,75% (base 60%) vs 3q MP 5,67%**: comparação direta — `relatorio_roi.md:75–79` (cenário base); `relatorio_candidatos_investimento.md:47–51` (score ranking).
- **2q MP ROI 6,20% base vs 3q MP 5,67%**: por capital menor (1,07M vs 1,88M) — `relatorio_roi.md:95` (linha 95 conclusão).
- **4q MP maior receita (232,2k) mas ROI menor (4,67%) e amostra pequena (60 com preço, 21%)**: `relatorio_candidatos_investimento.md:62–63`; `relatorio_criterios_investimento.md:41` (score 20, 5º lugar); `relatorio_roi.md:62` (linha 62 tabela).
- **Tese studio/1q Centro não sustentada**: ROI 10,92% ≈ 2q Centro 10,89%, mas receita menor (R$ 97k vs 125k) e apenas 22 à venda vs 89 — `reports/05_tese_compactos/relatorio_tese_compactos_centro.md:1–8`.
- **Script gerador de candidatos e critérios**: `analysis/analisar_candidatos_investimento.py` e `analysis/analisar_decisao_criterios.py` — geram `relatorio_candidatos_investimento.md` e `relatorio_criterios_investimento.md`.
- **Script gerador de ROI**: `analysis/analisar_roi.py` — gera `relatorio_roi.md` com custos e ROI em 3 cenários.
- **Premissa de ocupação 60% (18 dias/mês)**: `reports/04_pergunta4_investimento/relatorio_candidatos_investimento.md:15`; `relatorio_roi.md:29`; `relatorio_criterios_investimento.md:14` — hipótese, não dado observado; utilizada em todos os cálculos de receita (`diária × 30 × 0,60 × 12`).
- **Dado observado — Preço compra**: `data/VivaReal_Itapema.csv` — coluna `sale_price` median >0 (cobertura 100% por perfil).
- **Dado observado — Diária e Airbnb**: `data/Details_Itapema.csv` / `analysis/base_analitica_itapema.csv` — coluna `price_mediano` median por perfil/bairro/quartos; `qtd_airbnb` contagens; cobertura 21–35% por perfil onde `price_mediano.notna()`.
- **Sem correspondência individual Viva vs Airbnb**: explicitado em `:107` do relatório_roi.md e `:107` do relatorio_candidatos_investimento.md — apenas segmento `bairro×quartos`, não por `listing_id`.
- **Condomínio e IPTU medianos >0**: DADO OBSERVADO com cobertura 68–82% (condomínio) e 60–70% (IPTU), zeros tratados como missing — `relatorio_roi.md:15` e `:32`; `relatorio_candidatos_investimento.md:89–99` (DADO vs CÁLCULO vs PREMISSA vs INTERPRETAÇÃO).