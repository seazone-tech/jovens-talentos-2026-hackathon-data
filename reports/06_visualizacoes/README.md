# 06 Visualizações

**Propósito:** Interface sem alterar CSVs, com cabeçalho duplo (original + tradução PT-BR) e filtro.

**Principais evidências:**
* `visualizacao_dados.html` (653k) - 5 bases, 100 linhas cada, `Price_AV` 118839 linhas, `VivaReal` 8329, tradução 67 colunas
* `visualizacao_precos.html` (38k) - 1005 preços por anúncio, 100 linhas, destaque P99 2250 (30 acima), R$29.000 mantido

**O que cada arquivo demonstra:**
* `visualizacao_dados.html`: Valores exatamente do CSV original, sem limpeza, com `filtrarTabela()` por `tableId`.
* `visualizacao_precos.html`: 1 linha por `airbnb_listing_id`, `qtd, min, max, médio, mediano`, com `acima_p99` flag.
