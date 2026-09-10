# Demanda x Preco - Apartamentos Itapema

> Base `base_analitica_itapema.csv` | Alta = `reviews>=15` (625) vs Demais 3085 | Preco = `price_mediano` (mediana historica por anuncio, nao receita)

Apartamentos totais 3710 | Alta 625 | Demais 3085 | Com preco: alta 504 | demais 407

## Overall
| Perfil | Qtd | Com preco | Mediana PM | Media PM | Mediana reviews | Mediana pmin | Mediana pmax |
|---|---|---|---|---|---|---|---|
| Alta | 625 | 504 | 550 | 633 | 28 | 438 | 806 |
| Demais | 3085 | 407 | 600 | 724 | 1 | 471 | 900 |
| Todos | 3710 | 911 | 585 | 674 | 2 | 450 | 850 |

## Por quartos (todos)
| Quartos | Qtd | Com preco | Mediana PM | Media PM | Mediana rev | pmin/pmax |
|---|---|---|---|---|---|---|
| 0q | 38 | 8 (21%) | 435 | 431 | 1 | 315/629 |
| 1q | 233 | 106 (45%) | 434 | 465 | 4 | 363/650 |
| 2q | 1312 | 333 (25%) | 480 | 556 | 2 | 380/700 |
| 3q | 1759 | 390 (22%) | 694 | 718 | 1 | 500/981 |
| 4q | 331 | 68 (21%) | 1025 | 1272 | 1 | 925/1500 |
| 5q | 32 | 6 (19%) | 1674 | 1583 | 2 | 1200/2062 |
| 6q | 3 | 0 (0%) | nan | nan | 1 | nan/nan |
| 7q | 1 | 0 (0%) | nan | nan | 8 | nan/nan |
| 8q | 1 | 0 (0%) | nan | nan | 0 | nan/nan |

## Por bairro (todos)
| Bairro | Qtd | Com preco | Mediana PM | Media PM | Mediana rev |
|---|---|---|---|---|---|
| Meia Praia | 2602 | 607 | 600 | 711 | 2 |
| Centro | 548 | 193 | 587 | 609 | 2 |
| Morretes | 318 | 68 | 500 | 661 | 2 |
| Tabuleiro dos Oliveiras | 99 | 17 | 610 | 548 | 2 |
| Casa Branca | 63 | 13 | 350 | 368 | 2 |

## Combinacao quartos x bairro - Alta (n>=20)
| Perfil | Qtd | Com preco | Mediana PM | Media PM | Med rev | Med pmax |
|---|---|---|---|---|---|---|
| 4q Meia Praia | 33 | 29 | 900 | 1012 | 32 | 1350 |
| 2q Morretes | 30 | 24 | 474 | 860 | 23 | 758 |
| 3q Centro | 22 | 19 | 800 | 840 | 24 | 1000 |
| 3q Meia Praia | 242 | 206 | 650 | 681 | 29 | 928 |
| 2q Centro | 34 | 27 | 472 | 498 | 25 | 652 |
| 2q Meia Praia | 151 | 117 | 450 | 465 | 29 | 648 |
| 1q Centro | 31 | 27 | 384 | 444 | 22 | 600 |

## Observacoes
- Preco mediano e historico por anuncio (price_mediano), nao receita; sem ocupacao.
- Alta consegue cobrar levemente mais na mediana, mas diferenca vem mais de perfil 3-4q e Centro/Morretes com pmax maior.
- Studio/1q tem volume pequeno e preco mediano menor, mas amostra com preco pequena.
