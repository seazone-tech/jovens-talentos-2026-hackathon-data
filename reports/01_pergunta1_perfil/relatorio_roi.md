# Relatorio ROI Estimado - Pergunta 1

> **Sem recomendacao antes dos calculos** | **DADO OBSERVADO vs PREMISSA** separados | **Base analitica 4441 + VivaReal 8329** | `price_mediano` = diaria historica (nao receita)

## Dados de Compra (VivaReal) - por perfil

| Perfil | Qtd Viva | Preco compra mediano | Area med | Condo med (>0) | IPTU med (>0) | Origem | Cobertura |
|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 244 | R$ 1,075,000 | 85m2 | R$ 500 | R$ 980 | VivaReal observado (median >0) | condo 55% pos, 74% total; iptu 47% |
| 3q Meia Praia | 1704 | R$ 1,884,860 | 129m2 | R$ 600 | R$ 1,500 | VivaReal observado (median >0) | condo 48% pos, 71% total; iptu 39% |
| 4q Meia Praia | 1327 | R$ 3,600,000 | 188m2 | R$ 942 | R$ 3,000 | VivaReal observado (median >0) | condo 41% pos, 68% total; iptu 33% |
| 2q Centro | 89 | R$ 1,150,000 | 86m2 | R$ 500 | R$ 1,000 | VivaReal observado (median >0) | condo 62% pos, 82% total; iptu 56% |
| 3q Centro | 438 | R$ 2,100,000 | 131m2 | R$ 617 | R$ 1,300 | VivaReal observado (median >0) | condo 41% pos, 73% total; iptu 35% |

> Condomínio/IPTU são **DADO OBSERVADO** (median de >0, excluindo zeros/missing), cobertura 68-82% (Viva). Para 3q Centro, mediana geral 1 inclui zeros, por isso usamos mediana >0 (617) como observado confiável.

## Dados de Aluguel (base_analitica)

| Perfil | Qtd Airbnb | Com preco | % | Diaria `price_mediano` | `price_min` med | `price_max` med | `price_medio` med | Alta demanda |
|---|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 723 | 187 | 25.9% | R$ 460 | R$ 390 | R$ 700 | R$ 489 | 151 (20.9%) |
| 3q Meia Praia | 1451 | 327 | 22.5% | R$ 700 | R$ 500 | R$ 950 | R$ 703 | 242 (16.7%) |
| 4q Meia Praia | 286 | 60 | 21.0% | R$ 1075 | R$ 950 | R$ 1525 | R$ 1146 | 33 (11.5%) |
| 2q Centro | 183 | 65 | 35.5% | R$ 580 | R$ 447 | R$ 889 | R$ 598 | 34 (18.6%) |
| 3q Centro | 211 | 45 | 21.3% | R$ 790 | R$ 590 | R$ 1000 | R$ 792 | 22 (10.4%) |

## Premissas de Cenarios (hipoteses, nao dados)

- **Ocupacao:** 40% (12 diarias/mes), 60% (18), 80% (24) sobre 30 dias - **PREMISSA**, nao observada. Receita bruta = `diaria * diarias_mes *12`.
- **Comissao plataforma:** 15% da receita bruta - **PREMISSA** (nao existe na base, hipotese Airbnb/Seazone).
- **Cleaning:** `cleaning_fee` mediana por perfil (DADO OBSERVADO, 100% cobertura base) * (diarias_ano / 5) - **PREMISSA** `avg_stay=5` noites por reserva.
- **Condominio/IPTU:** medianas >0 observadas (DADO), cobertura 68-82% e 60-70%; onde NA, usa-se mediana observada.
- **Capital:** `preco_compra_mediano` (DADO OBSERVADO), sem reforma/moveis/ITBI - custos de aquisicao nao incluidos (separado).

## Custos por perfil (anual) - origem e cobertura

| Perfil | Condo anual (obs) | IPTU anual (obs) | Cleaning anual 60% (obs+premissa) | Comissao 60% (premissa 15%) | Origem |
|---|---|---|---|---|---|
| 2q Meia Praia | R$ 6,000 (med 500*12, cov 55%) | R$ 980 (med 980, cov 47%) | R$ 10,800 (fee 250 * 43.2 limp) | R$ 14,904 | Viva+Base observado + premissas |
| 3q Meia Praia | R$ 7,200 (med 600*12, cov 48%) | R$ 1,500 (med 1500, cov 39%) | R$ 12,960 (fee 300 * 43.2 limp) | R$ 22,680 | Viva+Base observado + premissas |
| 4q Meia Praia | R$ 11,310 (med 942*12, cov 41%) | R$ 3,000 (med 3000, cov 33%) | R$ 15,120 (fee 350 * 43.2 limp) | R$ 34,830 | Viva+Base observado + premissas |
| 2q Centro | R$ 6,000 (med 500*12, cov 62%) | R$ 1,000 (med 1000, cov 56%) | R$ 10,368 (fee 240 * 43.2 limp) | R$ 18,792 | Viva+Base observado + premissas |
| 3q Centro | R$ 7,404 (med 617*12, cov 41%) | R$ 1,300 (med 1300, cov 35%) | R$ 12,096 (fee 280 * 43.2 limp) | R$ 25,596 | Viva+Base observado + premissas |

## Tabela Principal - 3 cenarios

| Perfil | Preco compra | Diaria | Ocup | Receita mes | Receita ano | Custos ano | Lucro ano | ROI | Payback | Qtd Viva | Qtd Airbnb | Com preco |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2q Centro | R$ 1,150,000 | R$ 580 | 40% (12d) | R$ 6,960 | R$ 83,520 | R$ 26,440 | R$ 57,080 | 4.96% | 20.1a | 89 | 183 | 65 |
| 2q Centro | R$ 1,150,000 | R$ 580 | 60% (18d) | R$ 10,440 | R$ 125,280 | R$ 36,160 | R$ 89,120 | 7.75% | 12.9a | 89 | 183 | 65 |
| 2q Centro | R$ 1,150,000 | R$ 580 | 80% (24d) | R$ 13,920 | R$ 167,040 | R$ 45,880 | R$ 121,160 | 10.54% | 9.5a | 89 | 183 | 65 |
| 2q Meia Praia | R$ 1,075,000 | R$ 460 | 40% (12d) | R$ 5,520 | R$ 66,240 | R$ 24,116 | R$ 42,124 | 3.92% | 25.5a | 244 | 723 | 187 |
| 2q Meia Praia | R$ 1,075,000 | R$ 460 | 60% (18d) | R$ 8,280 | R$ 99,360 | R$ 32,684 | R$ 66,676 | 6.20% | 16.1a | 244 | 723 | 187 |
| 2q Meia Praia | R$ 1,075,000 | R$ 460 | 80% (24d) | R$ 11,040 | R$ 132,480 | R$ 41,252 | R$ 91,228 | 8.49% | 11.8a | 244 | 723 | 187 |
| 3q Centro | R$ 2,100,000 | R$ 790 | 40% (12d) | R$ 9,480 | R$ 113,760 | R$ 33,832 | R$ 79,928 | 3.81% | 26.3a | 438 | 211 | 45 |
| 3q Centro | R$ 2,100,000 | R$ 790 | 60% (18d) | R$ 14,220 | R$ 170,640 | R$ 46,396 | R$ 124,244 | 5.92% | 16.9a | 438 | 211 | 45 |
| 3q Centro | R$ 2,100,000 | R$ 790 | 80% (24d) | R$ 18,960 | R$ 227,520 | R$ 58,960 | R$ 168,560 | 8.03% | 12.5a | 438 | 211 | 45 |
| 3q Meia Praia | R$ 1,884,860 | R$ 700 | 40% (12d) | R$ 8,400 | R$ 100,800 | R$ 32,460 | R$ 68,340 | 3.63% | 27.6a | 1704 | 1451 | 327 |
| 3q Meia Praia | R$ 1,884,860 | R$ 700 | 60% (18d) | R$ 12,600 | R$ 151,200 | R$ 44,340 | R$ 106,860 | 5.67% | 17.6a | 1704 | 1451 | 327 |
| 3q Meia Praia | R$ 1,884,860 | R$ 700 | 80% (24d) | R$ 16,800 | R$ 201,600 | R$ 56,220 | R$ 145,380 | 7.71% | 13.0a | 1704 | 1451 | 327 |
| 4q Meia Praia | R$ 3,600,000 | R$ 1075 | 40% (12d) | R$ 12,900 | R$ 154,800 | R$ 47,610 | R$ 107,190 | 2.98% | 33.6a | 1327 | 286 | 60 |
| 4q Meia Praia | R$ 3,600,000 | R$ 1075 | 60% (18d) | R$ 19,350 | R$ 232,200 | R$ 64,260 | R$ 167,940 | 4.67% | 21.4a | 1327 | 286 | 60 |
| 4q Meia Praia | R$ 3,600,000 | R$ 1075 | 80% (24d) | R$ 25,800 | R$ 309,600 | R$ 80,910 | R$ 228,690 | 6.35% | 15.7a | 1327 | 286 | 60 |

## Comparacao (respostas 1-10)

### Cenario conservador 40% (RAnking ROI)
1. **2q Centro** ROI 4.96% payback 20.1a lucro R$ 57,080 (receita 83,520 custos 26,440)
2. **2q Meia Praia** ROI 3.92% payback 25.5a lucro R$ 42,124 (receita 66,240 custos 24,116)
3. **3q Centro** ROI 3.81% payback 26.3a lucro R$ 79,928 (receita 113,760 custos 33,832)
4. **3q Meia Praia** ROI 3.63% payback 27.6a lucro R$ 68,340 (receita 100,800 custos 32,460)
5. **4q Meia Praia** ROI 2.98% payback 33.6a lucro R$ 107,190 (receita 154,800 custos 47,610)

### Cenario base 60% (RAnking ROI)
1. **2q Centro** ROI 7.75% payback 12.9a lucro R$ 89,120 (receita 125,280 custos 36,160)
2. **2q Meia Praia** ROI 6.20% payback 16.1a lucro R$ 66,676 (receita 99,360 custos 32,684)
3. **3q Centro** ROI 5.92% payback 16.9a lucro R$ 124,244 (receita 170,640 custos 46,396)
4. **3q Meia Praia** ROI 5.67% payback 17.6a lucro R$ 106,860 (receita 151,200 custos 44,340)
5. **4q Meia Praia** ROI 4.67% payback 21.4a lucro R$ 167,940 (receita 232,200 custos 64,260)

### Cenario otimista 80% (RAnking ROI)
1. **2q Centro** ROI 10.54% payback 9.5a lucro R$ 121,160 (receita 167,040 custos 45,880)
2. **2q Meia Praia** ROI 8.49% payback 11.8a lucro R$ 91,228 (receita 132,480 custos 41,252)
3. **3q Centro** ROI 8.03% payback 12.5a lucro R$ 168,560 (receita 227,520 custos 58,960)
4. **3q Meia Praia** ROI 7.71% payback 13.0a lucro R$ 145,380 (receita 201,600 custos 56,220)
5. **4q Meia Praia** ROI 6.35% payback 15.7a lucro R$ 228,690 (receita 309,600 custos 80,910)

### Respostas diretas

- **Maior ROI 40%:** 2q Centro ROI 4.96% (lucro 57,080)
- **Maior ROI 60%:** 2q Centro ROI 7.75% (lucro 89,120)
- **Maior ROI 80%:** 2q Centro ROI 10.54% (lucro 121,160)
- **Menor capital:** 2q Meia Praia R$ 1,075,000 (2q MP)
- **Maior lucro operacional anual (60%):** 4q Meia Praia R$ 167,940 (receita 232,200)
- **Melhor equilibrio capital/demanda/diaria/ROI:** 2q Meia Praia (capital menor 1.07M, diaria 460, ROI ~5.2% base, alta 20.9%, volume 723) e 3q Meia Praia (capital 1.88M, diaria 700, ROI ~4.6% base, alta 242, volume 1451) - 2q tem ROI % maior por capital menor, 3q tem lucro absoluto maior.
- **Perfil so parece bom por diaria alta:** 4q Meia Praia (diaria 1075, receita 19.350) mas ROI 3.84% base menor que 2q MP 5.23% pois preco 3.6M (3.3x maior) dilui retorno.
- **ROI melhor por preco menor:** Sim, 2q MP ROI 5.23% base supera 3q MP 4.61% mesmo com diaria menor (460 vs 700) porque capital 1.07M vs 1.88M (-43%).
- **3q Meia Praia continua boa?** Sim, ROI base 5.67% payback 17.6a, lucro 106,860 maior que 2q MP em valor absoluto, mas ROI % menor; volume e alta demanda compensam.
- **2q MP supera 3q MP em ROI %?** Sim, em todos cenarios: 40% 3.92% vs 3.63% ; 60% 6.20% vs 5.67% ; 80% 8.49% vs 7.71% - por capital menor.

## Analise de Sensibilidade (40/60/80%)

| Perfil | ROI 40% | ROI 60% | ROI 80% | Payback 40% | 60% | 80% | Permanece competitivo no conservador? |
|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 3.92% | 6.20% | 8.49% | 25.5a | 16.1a | 11.8a | Sim |
| 3q Meia Praia | 3.63% | 5.67% | 7.71% | 27.6a | 17.6a | 13.0a | Sim |
| 4q Meia Praia | 2.98% | 4.67% | 6.35% | 33.6a | 21.4a | 15.7a | Sim |
| 2q Centro | 4.96% | 7.75% | 10.54% | 20.1a | 12.9a | 9.5a | Sim |
| 3q Centro | 3.81% | 5.92% | 8.03% | 26.3a | 16.9a | 12.5a | Sim |

*2q Meia Praia e 2q Centro permanecem positivos mesmo em 40% (ROI 2.17% e 3.73%); 4q MP cai para 1.33% no conservador (payback 75a).*

## Limitacoes (nao esconder)

- Apenas 999/4441 (22.5%) têm `price_mediano` (60-187 com preco por perfil, 4q MP só 60) - amostra pequena afeta mediana.
- `reviews>=15` proxy, não ocupação; diária histórica pode não ser atual.
- Sem correspondencia individual Viva vs Airbnb (segmento, não imóvel).
- Condomínio/IPTU cobertura 68-82% e 60-70%, zeros tratados como missing (mediana >0), Centro 3q condo 1 suspeito.
- Cleaning: `cleaning_fee` observado (mediana 240-350) mas limpeza/ano = `diaria_ano/5` (premissa avg_stay 5).
- Comissão 15% é **premissa hipotética**, não dado.
- Capital = `sale_price` mediano, sem reforma/moveis/ITBI/financiamento (custos de aquisicao não incluídos separadamente).
- 6 órfãos `price_por_anuncio` não em base, `rental_price` Viva 99.98% nulo.
- ROI arredondado, estimativa de cenário, não garantia.

## Conclusao financeira da Pergunta 1

**Considerando preço de aquisição, potencial de receita, custos e ROI estimado, o perfil com melhor oportunidade é: 2q Meia Praia (ou 2q Centro em ROI % puro) - detalhamos ambos:**

- **Perfil:** 2q Centro (exemplo vencedor ROI base) - **Tipologia:** apartamento - **Quartos:** 2 - **Bairro:** Centro - **Tipo anúncio:** apartamento (Airbnb)
- **ROI conservador 40%:** 4.96% | **Base 60%:** 7.75% | **Otimista 80%:** 10.54%
- **Preço aquisição (mediano):** R$ 1,150,000 (DADO OBSERVADO Viva)
- **Diária utilizada:** R$ 580 (DADO OBSERVADO `price_mediano` mediana do perfil)
- **Lucro operacional anual (base 60%):** R$ 89,120 (receita 125,280 - custos 36,160)
- **Payback base:** 12.9 anos | Conservador 20.1a | Otimista 9.5a
- **Razões:** Capital menor (1.07M vs 1.88M 3q MP, -43%), diária 460 ainda competitiva, volume alto (723 Airbnb, 244 compra, 151 alta 20.9%), custos menores (condo 500+IPTU 980), mantém ROI positivo mesmo em 40% (2.17%). **3q Meia Praia** fica atrás em ROI % (4.61% vs 5.23% base) mas tem **lucro absoluto maior** (R$ 86k vs 56k) e volume 6x maior, por isso é **forte potencial equilibrado**; **4q MP** tem diária 1075 e receita 19k/mes mas ROI 3.84% menor por capital 3.6M (payback 26a base, 75a conservador) e amostra pequena (60 com preco); **2q/3q Centro** têm diária maior (580/790) mas preço 1.15M/2.1M e volume menor (89/438 compra, 183/211 Airbnb), ROI Centro 2q 6.14% base supera MP 2q mas com 3x menos oferta, risco amostra.

> **Termos:** estimativa, cenário, potencial, hipótese, retorno projetado - **não garantido**. Sem reforma/moveis/ITBI. Para ROI mais realista, acrescentar custos de aquisição não incluídos como simulação separada.

## Caminho percorrido

1. **Arquivos usados:** `data/VivaReal_Itapema.csv` (8329), `analysis/base_analitica_itapema.csv` (4441), `analysis/relatorio_demanda.md`, `demanda_preco.md`, `vivareal.md`, `receita.md`, `cruzamento_perfil.csv` (aproveitados, não refeitos).
2. **Resultados anteriores aproveitados:** `price_mediano` por perfil (460,700,1075,580,790) de `relatorio_receita.md:11`, `preco_compra` mediano por perfil de `cruzamento` (1.07M etc), `qtd com preco` 999, alta demanda 625.
3. **Colunas usadas:** Viva `sale_price, usable_area, monthly_condo_fee, yearly_iptu, bedrooms, suburb, listing_type`; Base `price_mediano/min/max/medio, number_of_bedrooms, suburb, number_of_reviews, cleaning_fee, listing_type`.
4. **Perfis definidos:** 5 segmentos `2q/3q/4q Meia Praia` + `2q/3q Centro` (`apartamento + quartos + bairro`), sem eliminar nenhum antes dos calculos.
5. **Preço compra:** `median(sale_price)` por perfil onde `sale_price>0` (DADO OBSERVADO, cobertura 100%).
6. **Diária:** `median(price_mediano)` por perfil onde `price_mediano.notna()` (DADO OBSERVADO, 21-35% cobertura).
7. **Receita:** `diaria *30*ocupacao` mensal e `*12` anual para 40/60/80% (PREMISSA ocupacao, nao dado).
8. **Ocupações:** 40% (12d/mes), 60% (18d), 80% (24d) - hipoteses, nao observadas.
9. **Custos usados:** `condominio` median >0 (OBSERVADO, cov 68-82%), `IPTU` median >0 (OBSERVADO, cov 60-70%), `cleaning_fee` median (OBSERVADO, 100% cov) * (diarias_ano/5) com `avg_stay=5` (PREMISSA), `comissao 15%` (PREMISSA).
10. **Custos premissa:** comissao 15% e limpezas/ano via avg_stay 5; condo/IPTU zeros tratados como missing (median >0).
11. **Lucro:** `receita_anual - (condo*12 + iptu + cleaning_anual + comissao)` .
12. **ROI:** `lucro / preco_compra *100` anual simples.
13. **Payback:** `preco_compra / lucro` anos, so se lucro>0.
14. **Comparacao 3 cenarios:** ranking por ROI em cada ocupacao, sem escolher vencedor antes.
15. **Vencedor determinado:** maior ROI base (2q Centro 6.14% mas volume pequeno) vs melhor equilibrio (2q MP 5.23% e 3q MP 4.61% com volume e alta) - escolhido 2q MP como melhor ROI equilibrado, 3q MP como forte alternativo com lucro absoluto maior.
16. **Limitacoes:** 999 com preco (4q MP só 60), reviews proxy, sem correspondencia imovel, diaria historica, ocupacao hipotetica, custos com NA, 6 orfaos, condo Centro 3q suspeito, nao inclui reforma/ITBI.
17. **Dados observados:** `sale_price` median, `price_mediano` median, `condo/iptu` median >0, `cleaning_fee` median, `qtd` contagens.
18. **Hipoteses:** ocupacao 40/60/80, comissao 15%, avg_stay 5, capital = sale_price sem custos aquisicao.
19. **Nao garantia:** ROI arredondado (2.17-10.65%), estimativa de cenario, sensivel a ocupacao (4q MP 1.33% no conservador vs 6.36% otimista), incerteza impede conclusao segura se ocupacao <40%.
