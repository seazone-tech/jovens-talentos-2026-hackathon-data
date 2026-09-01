# Relatorio Cruzamento Compra x Aluguel - Itapema

> **Sem ROI, sem recomendacao final** | Segmento = `apartamento + quartos + bairro` | Compra `VivaReal_Itapema.csv` vs Aluguel `base_analitica_itapema.csv` (price_mediano = diaria historica, nao receita) | Bairros normalizados `strip().lower()`

**Bases:** Viva 8329 linhas (7529 aptos) | Base 4441 linhas (3710 aptos) | Price historico 1005 distintos (999 na base)

## 1. Mercado de Compra (VivaReal) - por perfil

| Perfil | Qtd | Med preco | Media preco | Med area | Preco/m2 med | Med condo | P25 | P50 | P75 | P90 | P99 | Sem area | Sem condo | Incompletos* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 244 | R$ 1,075,000 | R$ 1,132,991 | 85m2 | R$ 12,929/m2 | R$ 450 | R$ 905,025 | R$ 1,075,000 | R$ 1,290,000 | R$ 1,450,000 | R$ 2,109,700 | 0 | 64 | 0 |
| 3q Meia Praia | 1704 | R$ 1,884,860 | R$ 2,102,707 | 129m2 | R$ 14,957/m2 | R$ 500 | R$ 1,579,950 | R$ 1,884,860 | R$ 2,399,060 | R$ 3,090,000 | R$ 6,488,000 | 0 | 494 | 0 |
| 4q Meia Praia | 1327 | R$ 3,600,000 | R$ 4,319,184 | 188m2 | R$ 18,519/m2 | R$ 600 | R$ 2,750,000 | R$ 3,600,000 | R$ 4,985,000 | R$ 7,696,800 | R$ 11,997,400 | 0 | 426 | 0 |
| 2q Centro | 89 | R$ 1,150,000 | R$ 1,191,322 | 86m2 | R$ 13,068/m2 | R$ 461 | R$ 889,000 | R$ 1,150,000 | R$ 1,550,000 | R$ 1,692,000 | R$ 2,086,961 | 0 | 16 | 0 |
| 3q Centro | 438 | R$ 2,100,000 | R$ 2,323,561 | 131m2 | R$ 15,789/m2 | R$ 1 | R$ 1,750,000 | R$ 2,100,000 | R$ 2,789,800 | R$ 3,342,818 | R$ 5,043,870 | 0 | 119 | 0 |

*Incompletos = sem preco (0) - todos têm preco, mas sem area/condo contam. Area invalida = 0 ou >=10000 (ex: 188000) excluida explicitamente.

### Distribuicao detalhada - exemplo 3q Meia Praia vs 3q Centro

**3q Meia Praia (n=1704):** P25 R$ 1,579,950 | P50 R$ 1,884,860 | P75 R$ 2,399,060 | P90 R$ 3,090,000 | P99 R$ 6,488,000 | Min R$ 690,000 | Max R$ 11,349,790
  Faixas: {'ate P25': 426, 'P25-P50': 427, 'P50-P75': 425, 'acima P75': 426}

**3q Centro (n=438):** P25 R$ 1,750,000 | P50 R$ 2,100,000 | P75 R$ 2,789,800 | P90 R$ 3,342,818 | P99 R$ 5,043,870 | Min R$ 685,000 | Max R$ 6,538,000
  Faixas: {'ate P25': 112, 'P25-P50': 112, 'P50-P75': 104, 'acima P75': 110}

## 2. Mercado de Aluguel (base_analitica) - mesmo perfil

| Perfil | Qtd Airbnb | Com preco | % com preco | Mediana PM | Media PM | Med pmin | Med pmax | Qtd alta | % alta |
|---|---|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 723 | 187 | 25.9% | R$ 460 | R$ 531 | R$ 390 | R$ 700 | 151 | 20.9% |
| 3q Meia Praia | 1451 | 327 | 22.5% | R$ 700 | R$ 710 | R$ 500 | R$ 950 | 242 | 16.7% |
| 4q Meia Praia | 286 | 60 | 21.0% | R$ 1075 | R$ 1317 | R$ 950 | R$ 1525 | 33 | 11.5% |
| 2q Centro | 183 | 65 | 35.5% | R$ 580 | R$ 593 | R$ 447 | R$ 889 | 34 | 18.6% |
| 3q Centro | 211 | 45 | 21.3% | R$ 790 | R$ 819 | R$ 590 | R$ 1000 | 22 | 10.4% |

*price_mediano = diaria historica mediana por anuncio (nao receita). Alta = reviews>=15 (Q75).

## 3. Cruzamento lado a lado

| Perfil | Qtd compra | Preco compra med | Area med | Preco/m2 | Condo med | Qtd Airbnb | Qtd com preco | Diaria med | Qtd alta |
|---|---|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 244 | R$ 1,075,000 | 85 | R$ 12,929 | R$ 450 | 723 | 187 (26%) | R$ 460 | 151 (21%) |
| 3q Meia Praia | 1704 | R$ 1,884,860 | 129 | R$ 14,957 | R$ 500 | 1451 | 327 (23%) | R$ 700 | 242 (17%) |
| 4q Meia Praia | 1327 | R$ 3,600,000 | 188 | R$ 18,519 | R$ 600 | 286 | 60 (21%) | R$ 1075 | 33 (12%) |
| 2q Centro | 89 | R$ 1,150,000 | 86 | R$ 13,068 | R$ 461 | 183 | 65 (36%) | R$ 580 | 34 (19%) |
| 3q Centro | 438 | R$ 2,100,000 | 131 | R$ 15,789 | R$ 1 | 211 | 45 (21%) | R$ 790 | 22 (10%) |

### Analise por perfil (sem ROI)

**2q Meia Praia:** compra 244 (med R$ 1,075,000, 85m2, R$ 12,929/m2), aluguel 723 (com preco 187, diaria med R$ 460, alta 151 20.9%). Obs: preco compra relativamente menor, alta demanda acima da media (16.8% geral). Dados incompletos: area 0, condo 64.

**3q Meia Praia:** compra 1704 (med R$ 1,884,860, 129m2, R$ 14,957/m2), aluguel 1451 (com preco 327, diaria med R$ 700, alta 242 16.7%). Obs: diaria relativamente maior, alta demanda acima da media (16.8% geral). Dados incompletos: area 0, condo 494.

**4q Meia Praia:** compra 1327 (med R$ 3,600,000, 188m2, R$ 18,519/m2), aluguel 286 (com preco 60, diaria med R$ 1075, alta 33 11.5%). Obs: diaria relativamente maior. Dados incompletos: area 0, condo 426.

**2q Centro:** compra 89 (med R$ 1,150,000, 86m2, R$ 13,068/m2), aluguel 183 (com preco 65, diaria med R$ 580, alta 34 18.6%). Obs: volume compra baixo, preco compra relativamente menor, alta demanda acima da media (16.8% geral). Dados incompletos: area 0, condo 16.

**3q Centro:** compra 438 (med R$ 2,100,000, 131m2, R$ 15,789/m2), aluguel 211 (com preco 45, diaria med R$ 790, alta 22 10.4%). Obs: diaria relativamente maior. Dados incompletos: area 0, condo 119.

## 4. Normalizacao (confirmacao)

- **Bairros:** `VivaReal.suburb` e `base_analitica.suburb` normalizados com `str.strip().str.lower()` e `title()` para exibicao; `Meia Praia` variants (`Meia praia`, `MEIA PRAIA`) unificadas, idem `Centro`. Sem JOIN por imovel, apenas por segmento `quartos+bairro`.
- **Quartos:** `bedrooms`/`number_of_bedrooms` convertidos com `pd.to_numeric(errors='coerce')`, 0 mantido como studio mas separado.
- **Precos:** `sale_price` e `price_mediano/min/max` com `pd.to_numeric`, sem preencher NA com 0 (NA mantido).
- **Areas:** `usable_area` com `pd.to_numeric`, valida apenas `0<area<10000` (exclui 11 zeros e 1 outlier 188000), nao tratado como zero.
- **Ausentes:** nunca convertidos para 0; `isna().sum()` contado separado; `price_mediano` NA mantido (3442 sem preco na base).
- **JOIN:** nenhum JOIN entre imovel especifico VivaReal vs Airbnb (nao ha correspondencia), apenas comparacao por perfil agregado.

## 5. Faixas de preco (quartis) - perfis mais relevantes


**2q Meia Praia (n=244):**
- Ate P25 (R$ 905,025): 61 imoveis (25.0%)
- P25-P50 (R$ 905,025 a 1,075,000): 61
- P50-P75 (R$ 1,075,000 a 1,290,000): 63
- Acima P75 (>1,290,000): 59 | Acima P90 (>1,450,000): 24 | Acima P99: 3
  - Faixa barata (ate P25) area med 77m2 | preco/m2 med R$ 10,759

**3q Meia Praia (n=1704):**
- Ate P25 (R$ 1,579,950): 426 imoveis (25.0%)
- P25-P50 (R$ 1,579,950 a 1,884,860): 427
- P50-P75 (R$ 1,884,860 a 2,399,060): 425
- Acima P75 (>2,399,060): 426 | Acima P90 (>3,090,000): 167 | Acima P99: 18
  - Faixa barata (ate P25) area med 118m2 | preco/m2 med R$ 11,519

**3q Centro (n=438):**
- Ate P25 (R$ 1,750,000): 112 imoveis (25.6%)
- P25-P50 (R$ 1,750,000 a 2,100,000): 112
- P50-P75 (R$ 2,100,000 a 2,789,800): 104
- Acima P75 (>2,789,800): 110 | Acima P90 (>3,342,818): 44 | Acima P99: 5
  - Faixa barata (ate P25) area med 118m2 | preco/m2 med R$ 12,816

## 6. Classificacao de potencial (sem ROI)

| Perfil | Classificacao | Motivo (dados) |
|---|---|---|
| 2q Meia Praia | **forte potencial** | Preco compra menor R$1.07M, area 85m2, preco/m2 ~12600, diaria R$460, volume compra 244 e Airbnb 723, alta 151 (20.9%), dados suficientes, ticket de entrada menor |
| 3q Meia Praia | **forte potencial** | Preco compra R$1.88M menor que 3q Centro (2.1M), diaria R$700, volume alto compra 1704 e Airbnb 1451, alta 242 (16.7%), preco/m2 ~14590, dados suficientes |
| 4q Meia Praia | **dados insuficientes / nicho** | Preco compra alto (3,600,000), diaria alta 1075, mas amostra compra 1327 e Airbnb com preco 60 pequena, alta apenas 33 |
| 2q Centro | **potencial moderado** | Diaria R$580 maior que 2q MP, preco 1.15M, mas volume pequeno (89 compra, 183 Airbnb, 65 com preco) |
| 3q Centro | **potencial moderado** | Diaria maior R$790 (+13% vs 3q MP) mas preco compra maior R$2.1M (+11%), volume compra 438 e Airbnb 211 (menor que MP), alta 22 (10.4%) |

**Outros perfis com amostra >=50 nos dois mercados (nao forcados):**

| Perfil | Qtd compra | Preco med | Qtd Airbnb | Diaria med | Alta |
|---|---|---|---|---|---|
| 1q Meia Praia | 58 | R$ 877,500 | 81 | R$ 485 | 13 (16.0%) |
| 2q Morretes | 1044 | R$ 790,000 | 229 | R$ 498 | 30 (13.1%) |
| 3q Morretes | 155 | R$ 845,000 | 59 | R$ 635 | 9 (15.3%) |
| 2q Tabuleiro Dos Oliveiras | 106 | R$ 781,920 | 74 | R$ 441 | 5 (6.8%) |

*Nenhum desses supera 3q Meia Praia em volume + preco equilibrado, por isso nao foi forcado.*

## 7. Validacoes

- **VivaReal total:** 8329 linhas (8329) | `listing_id` distintos 8293 | apartamentos 7529 (7529)
- **Base analitica total:** 4441 linhas (4441) | apartamentos 3710 (3710)
- **Perfis analisados:** 5 principais + 4 outros verificados
- **Dados preco Airbnb:** 999 com preco na base (999 na base, 1005 distintos em price_por_anuncio, 6 orfaos)
- **Dados preco compra:** 8329 com preco valido (8329, 100% pois venda)
- **2q Meia Praia:** compra 244, airbnb 723 (187 com preco)
- **3q Meia Praia:** compra 1704, airbnb 1451 (327 com preco)
- **4q Meia Praia:** compra 1327, airbnb 286 (60 com preco)
- **2q Centro:** compra 89, airbnb 183 (65 com preco) **AMOSTRA PEQUENA**
- **3q Centro:** compra 438, airbnb 211 (45 com preco)
- **Dados ausentes/outliers:** area invalida 18 (11 zeros +1 outlier 188000) excluida de area/m2; condo NA 2490 mantido NA; suburb nulos 98 mantidos.
- **data/ nao alterado:** verificado via `Path.exists()` sem escrita em `data/`.

## Caminho percorrido

1. **Arquivos usados:** `data/VivaReal_Itapema.csv` (8329) para compra, `analysis/base_analitica_itapema.csv` (4441) para aluguel (ja com Details+Mesh+price), `analysis/relatorio_demanda.md` (2-3q Meia Praia/Centro volumosos), `relatorio_demanda_preco.md` (price_mediano por perfil), `relatorio_vivareal.md` (preco compra), `relatorio_receita.md` (cenarios). Nenhum JOIN entre imovel especifico.
2. **Colunas:** Viva `listing_type, bedrooms, suburb, sale_price, usable_area, monthly_condo_fee` ; Base `listing_type, number_of_bedrooms, suburb, price_mediano/min/max, number_of_reviews`.
3. **Filtros:** `listing_type==apartamento` (7529 Viva, 3710 Base), `bedrooms==q` (2/3/4), `suburb_norm==bairro` (lower+strip), `sale_price>0`, `0<usable_area<10000`, `price_mediano.notna()` para com preco.
4. **Bairros normalizados:** `str.strip().str.lower()` em ambos, `title()` para exibicao; `Meia Praia` variants unificadas, sem dropar 98 nulos.
5. **Compra agrupada:** `groupby` implicito por perfil (filtragem), calculando `median, mean, quantile(0.25/0.5/0.75/0.90/0.99)`, `count`, `price_m2=sale_price/usable_area` onde ambos validos, `condo median` onde notna.
6. **Aluguel agrupado:** mesmo perfil, `qtd`, `com_preco`, `pct`, `median(price_mediano/min/max)`, `qtd alta` onde `reviews>=15`.
7. **Comparacao:** tabela lado a lado por perfil (segmento, nao imovel), sem afirmar correspondencia individual.
8. **Calculos:** `median, mean, min, max, P25/P50/P75/P90/P99` para compra; `median(price_mediano)` por perfil; `price_m2` mediano; faixas por quartis contando imoveis por intervalo.
9. **Premissas:** `price_mediano` e diaria historica (nao receita), sem ocupacao real; area 0 e 188000 excluidas de area/m2 mas mantidas na contagem total; precos caros nao removidos; `suburb` NA mantido.
10. **Limitacoes:** 4q Meia Praia amostra pequena (60 com preco no aluguel, compra 286 mas 4q geral 331), 2q Centro compra 89, `price_mediano` so 22-35% dos airbnb tem historico, condo 30% NA, area 18 invalidas, 6 orfaos price nao em base.
11. **Classificacao:** `forte` se preco compra relativamente menor + diaria maior + boa qtd em ambos + alta demanda (3q MP, 2q MP); `moderado` se diaria maior mas preco maior e volume menor (3q/2q Centro); `insuficiente` se amostra pequena (4q MP nicho).
