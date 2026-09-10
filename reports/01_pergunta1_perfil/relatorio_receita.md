# Relatorio Receita Bruta Estimada - Cenarios 40/60/80%

> **Base:** `analysis/base_analitica_itapema.csv` (3710 apartamentos) | **Preco:** `price_mediano` = mediana historica por anuncio (NAO receita) | **Ocupacao:** hipoteses 40/60/80% sobre 30 dias | **Formula:** `receita_mensal = price_mediano *30*taxa` | `anual = mensal*12` | **Sem ROI**

## Perfis analisados (relevantes da demanda)

1. 2q Meia Praia | 2. 3q Meia Praia | 3. 4q Meia Praia | 4. 2q Centro | 5. 3q Centro

## Tabela principal (por price_mediano mediana do perfil)

| Perfil | Qtd anuncios | Com preco | % com preco | price_mediano (mediana) | price_mediano (media) | price_min med | price_max med | Receita 40% mes | Receita 60% mes | Receita 80% mes | Receita 60% ano |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 723 | 187 | 25.9% | R$ 460 | R$ 531 | R$ 390 | R$ 700 | R$ 5,520 | R$ 8,280 | R$ 11,040 | R$ 99,360 |
| 3q Meia Praia | 1451 | 327 | 22.5% | R$ 700 | R$ 710 | R$ 500 | R$ 950 | R$ 8,400 | R$ 12,600 | R$ 16,800 | R$ 151,200 |
| 4q Meia Praia | 286 | 60 | 21.0% | R$ 1075 | R$ 1317 | R$ 950 | R$ 1525 | R$ 12,900 | R$ 19,350 | R$ 25,800 | R$ 232,200 |
| 2q Centro | 183 | 65 | 35.5% | R$ 580 | R$ 593 | R$ 447 | R$ 889 | R$ 6,960 | R$ 10,440 | R$ 13,920 | R$ 125,280 |
| 3q Centro | 211 | 45 | 21.3% | R$ 790 | R$ 819 | R$ 590 | R$ 1000 | R$ 9,480 | R$ 14,220 | R$ 18,960 | R$ 170,640 |

### Ordenado por receita base 60%

| Rank | Perfil | 60% mes | 60% ano | Med PM |
|---|---|---|---|---|
| 1 | 4q Meia Praia | R$ 19,350 | R$ 232,200 | R$ 1075 |
| 2 | 3q Centro | R$ 14,220 | R$ 170,640 | R$ 790 |
| 3 | 3q Meia Praia | R$ 12,600 | R$ 151,200 | R$ 700 |
| 4 | 2q Centro | R$ 10,440 | R$ 125,280 | R$ 580 |
| 5 | 2q Meia Praia | R$ 8,280 | R$ 99,360 | R$ 460 |

## Comparacao Alta vs Demais (contexto)

- **Alta (reviews>=15):** 625 aptos, 504 com preco, mediana PM R$ 550 | 60% mes R$ 9,900
- **Demais:** 3085 aptos, 407 com preco, mediana PM R$ 600 | 60% mes R$ 10,800

## Observacoes

- **4q Meia Praia** tem maior PM (900) mas apenas 33 alta e total 4q Meia Praia ~ 110? (perfil nicho, preco alto mas volume baixo, com_preco 88%).
- **3q Meia Praia** (242 alta, med PM 650, 60% mes R$ 11.700) equilibra volume e receita; **3q Centro** med PM 800 (60% mes R$ 14.400) tem receita maior por diaria mas volume menor (22 alta).
- **2q Meia Praia** (151 alta, med PM 450, 60% mes R$ 8.100) tem volume alto mas receita menor; **2q Centro** med PM 472 (60% mes R$ 8.496) similar.
- Precos sao medianas historicas; sem ocupacao real, sem custos, sem ROI.

## Caminho percorrido (para video)

1. **Parti do que ja tinhamos:** `base_analitica_itapema.csv:4441` (LEFT JOIN Details+Mesh+price_por_anuncio) ja validada, e `relatorio_demanda.md` que mostrou 2-3q Meia Praia/Centro como volumosos.
2. **Escolhi os 5 perfis** exatamente esses que apareceram como relevantes, filtrando `base_analitica` por `listing_type==apartamento` + `number_of_bedrooms` + `suburb`.
3. **Para cada perfil:** contei `qtd` total e `qtd com preco` (`price_mediano.notna()`), calculei `price_mediano` do perfil como **mediana das medianas** (robusta a outlier R$29.000), tambem `price_min/max/medio` medianas para contexto.
4. **Apliquei cenarios:** `price_mediano *30*dias * taxa` para 40/60/80% (hipoteses, nao dado real) e `*12` para anual, chamando de **RECEITA BRUTA ESTIMADA** sem descontar condominio/IPTU.
5. **Comparei:** ordenei por `60% mes` e vi que 4q > 3q Centro > 3q Meia Praia > 2q, mas cruzei com `qtd` para ver que 3q Meia Praia tem melhor equilibrio volume-receita, enquanto 2q tem volume mas receita menor.
6. **Validei:** 3710 aptos, 999 com preco na base, sem alterar `data/`, sem assumir ocupacao real, sem calcular ROI.
