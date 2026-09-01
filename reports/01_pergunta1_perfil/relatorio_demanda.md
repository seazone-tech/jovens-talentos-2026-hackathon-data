# Analise de Demanda por Reviews - Apartamentos Itapema

> Base: `analysis/base_analitica_itapema.csv` | Filtro: `listing_type==apartamento` (3710) | Alta demanda: `number_of_reviews >= 15` (Q75, n=625) vs Demais n=3085
> **Limitacao:** `number_of_reviews` e proxy acumulado, nao mede reservas/ocupacao, vies de tempo de anuncio e incentivo a avaliar.

## 1. Quartos
| Quartos | Alta 625 | Demais 3085 | Todos 3710 |
|---|---|---|---|
| 0q | 4 (0.6%) | 34 (1.1%) | 38 (1.0%) |
| 1q | 56 (9.0%) | 177 (5.7%) | 233 (6.3%) |
| 2q | 239 (38.2%) | 1073 (34.8%) | 1312 (35.4%) |
| 3q | 279 (44.6%) | 1480 (48.0%) | 1759 (47.4%) |
| 4q | 39 (6.2%) | 292 (9.5%) | 331 (8.9%) |
| 5q | 8 (1.3%) | 24 (0.8%) | 32 (0.9%) |
| 6q | 0 (0.0%) | 3 (0.1%) | 3 (0.1%) |
| 7q | 0 (0.0%) | 1 (0.0%) | 1 (0.0%) |
| 8q | 0 (0.0%) | 1 (0.0%) | 1 (0.0%) |

## 2. Bairro top
| Bairro | Alta | Demais | Todos |
|---|---|---|---|
| Meia Praia | 450 (72.0%) | 2152 (69.8%) | 2602 (70.1%) |
| Centro | 92 (14.7%) | 456 (14.8%) | 548 (14.8%) |
| Morretes | 45 (7.2%) | 273 (8.8%) | 318 (8.6%) |
| Tabuleiro dos Oliveiras | 6 (1.0%) | 93 (3.0%) | 99 (2.7%) |
| Casa Branca | 11 (1.8%) | 52 (1.7%) | 63 (1.7%) |

## Conclusao
- Associado: 2-3q, 6 hosp, Meia Praia leve vantagem, Guest Favorite 67% vs 10%, fotos 24 vs 11, Wi-Fi/Ar/Maquina como commodity.
- Nao diferencia: bairro Centro, is_professional (diferenca pequena), cleaning_fee, lat/lon.
