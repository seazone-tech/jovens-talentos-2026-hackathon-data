# Relatorio VivaReal - Mercado de Compra Itapema

> **Sem ROI/receita** | **Sem alteracao em `data/`** | Arquivo: `data/VivaReal_Itapema.csv` | Gerado por `analysis/analisar_vivareal.py`

## 1. O que cada coluna representa

| Coluna | Descricao | Tipo | Observacao |
|---|---|---|---|
| `listing_id` | ID do anuncio no VivaReal (PK, string) | str |  |
| `link_url` | URL do anuncio | str |  |
| `listing_title` | Titulo do anuncio | str |  |
| `business_types` | Tipo de negocio (Venda/Ambos) | str |  |
| `listing_type` | Tipo de imovel (apartamento/casa/terreno/comercial/outros) | str |  |
| `property_type` | Subtipo (UNIT = unidade) | str |  |
| `sale_price` | Preco de venda (R$) - numerico | float64 |  |
| `rental_price` | Preco de aluguel (R$) - 99.98% vazio pois base e Venda | float64 |  |
| `rental_period` | Periodo aluguel (<NA> 99.98%) | str |  |
| `yearly_iptu` | IPTU anual (R$) - 32.6% vazio | float64 |  |
| `monthly_condo_fee` | Condominio mensal (R$) - 29.9% vazio | float64 |  |
| `amenities` | Lista de comodidades (string JSON-like, ex: ["POOL","ELEVATOR"]) - 5037 categorias, 420 vazios [] | str |  |
| `usable_area` | Area util (m2) - numerico, 11 zeros invalidos | int64 |  |
| `bathrooms` | Qtd banheiros - 2.07% zeros | int64 |  |
| `bedrooms` | Qtd quartos - 2.76% zeros | int64 |  |
| `parking_spaces` | Vagas garagem - 3.71% zeros | int64 |  |
| `state` | Estado (SC, 2 nulos) | str |  |
| `city` | Cidade (Itapema, 100%) | str |  |
| `suburb` | Bairro - 25 categorias, 98 nulos 1.18%, inconsistentes Meia Praia/Meia praia | str |  |
| `advertiser_name` | Anunciante - 471 anunciantes, top NEWCORE 625 | str |  |
| `portal` | Portal (GRUPOZAP 100%) | str |  |
| `aquisition_date` | Data de coleta | str |  |

## 2. Quantos imoveis

- **Total de linhas (anuncios): 8329**
- **IDs distintos (`listing_id`): 8293**
- **IDs duplicados: 36** (36 ids aparecem 2x)
- **Linhas 100% duplicadas (todas colunas iguais): 70 linhas em 70 ocorrencias / 35 grupos** (ex: id `2687011752` aparece 2x com mesma URL)
- **Base e predominantemente VENDA:** `business_types` Venda=8327 (100.0%), Ambos=2
- **Tipo imovel:** apartamento 7529 (90.4%), casa 547, terreno 164

## 3. Informacoes disponiveis

### Preco de venda (`sale_price`)
- Validos (>0): 8329 / 8329 (100.0%) | Nulos/invalidos: 0
- Todos sao venda, entao `sale_price` e a metrica central para posterior cruzamento com aluguel

### Quartos (`bedrooms`)
- Distribuicao: {0: 230, 1: 179, 2: 2076, 3: 3435, 4: 2240, 5: 136, 6: 24, 7: 7, 8: 1, 11: 1} | 0 quartos (invalido) 230 (2.8%)
- 3 quartos (foco): 3435 imoveis (41.2%) | Apartamentos 3q: 3205 (38.5%)

### Area (`usable_area`)
- Valida (0<area<10000): 8311 | Invalida/0/suspeita: 18 (11 zeros + 1 outlier 188000 m2)
- Mediana area (todos validos): 128 m2 | Media: 156 m2

### Bairro (`suburb`)
- 25 bairros + 98 vazios (1.18%) | Top: Meia Praia 3452 (41.4%), Morretes 1777, Centro 1009
- Inconsistencias case: `Meia Praia` aparece como `Meia Praia` (3452), `Meia praia` (pequeno), `MEIA PRAIA`; `Centro` vs `CENTRO` - normalizar com `.str.strip().str.lower()` antes de agrupar

### Condominio (`monthly_condo_fee`)
- Validos: 5839 (70.1%) | Vazios: 2490 (29.9%) | Zeros validos (sem condominio): 2364 (inclui casas/terrenos)
- Mediana condominio (validos): 290 | Media: 2373

### Outras relevantes para comparar com aluguel
- `bathrooms` mediana 3 (todos) | `parking_spaces` mediana 2 | `amenities` 5037 categorias, 420 `[]` vazios
- `property_type` sempre `UNIT` (8329) - nao diferencia
- `state` SC 8327 + 2 nulos | `city` Itapema 100% | `portal` GRUPOZAP 100% (sem variacao)

## 4. Qualidade dos dados

| Problema | Quantidade | % | Gravidade | Precisa tratar? | Tratamento |
|---|---|---|---|---|---|
| `rental_price` nulos | 8327 | 99.98% | baixa | Nao | Base e Venda, manter vazio |
| `rental_period` <NA> | 0 | 99.98% | baixa | Nao | Sentinela |
| `yearly_iptu` nulos | 2714 | 32.6% | media | Sinalizar | Manter NaN, usar mediana por bairro se precisar |
| `monthly_condo_fee` nulos | 2490 | 29.9% | media | Sinalizar | Idem |
| `sale_price` invalidos (0/NaN) | 0 | 0.0% | alta | Sim | Excluir de calculo de compra (0 nao existe) |
| `usable_area` 0 ou 188000 | 12 | 0.14% | alta | Sim | Excluir 0 e >10000 da analise de area |
| `bathrooms` 0 | 172 | 2.07% | media | Sinalizar | Pode ser studio sem banheiro? Verificar, mas manter com flag |
| `bedrooms` 0 | 230 | 2.76% | media | Sinalizar | Studio 0q, manter mas separar |
| `suburb` nulos | 98 | 1.18% | media | Sim | Criar SEM_BAIRRO/flag, nao dropar linha |
| `suburb` inconsistentes case | 3 bairros com variacoes | - | baixa | Sim | Normalizar lower+strip antes de agrupar |
| `listing_id` duplicados | 36 | 0.4% | media | Sim | Deduplicar mantendo 1 (ou flag), 35 linhas 100% dup |
| `state` nulos | 2 | 0.02% | baixa | Nao | Manter |
| `usable_area` outlier 188000 | 1 | 0.01% | alta | Sim | Excluir, erro de digitacao |

**Precos suspeitos:** max 44.000.000 (alto mas pode ser cobertura frente mar), min 10.000 (muito baixo, mas 1 terreno) - manter mas sinalizar P99.

## 5. Analise exploratoria preco de compra

- **Qtd com preco valido:** 8329 / 8329
- **Mediana:** R$ 1,750,000
- **Media:** R$ 2,450,770
- **Minimo:** R$ 10,000
- **Maximo:** R$ 44,000,000
- **P99 (observacoes):** R$ 12,990,736 | P90: R$ 4,891,000
- **Distribuicao:** 25% ate R$ 900,000 | 75% ate R$ 2,890,000

### Por tipo de imovel
| Tipo | Qtd | Mediana | Media | Min | Max |
|---|---|---|---|---|---|
| apartamento | 7529 | R$ 1,833,150 | R$ 2,478,629 | R$ 10,000 | R$ 44,000,000 |
| casa | 547 | R$ 743,000 | R$ 2,238,719 | R$ 290,000 | R$ 25,000,000 |
| terreno | 164 | R$ 737,500 | R$ 1,663,030 | R$ 265,575 | R$ 39,499,800 |

## 6. Imoveis de 3 quartos

- **Todos 3q (qualquer tipo):** 3435 | Com preco valido: 3205
- **Apartamentos 3q:** 3205 total | 3205 com preco valido
  - Mediana preco 3q apto: R$ 1,800,000 | Media: R$ 1,994,913 | Min: R$ 429,000 | Max: R$ 11,349,790
  - Mediana area 3q apto: 127 m2 | Media: 136 m2 | Mediana condominio: R$ 450

### 3 quartos por bairro (apartamento)
| Bairro | Qtd apto 3q | Com preco | Mediana preco | Media preco | Mediana area | Mediana condominio |
|---|---|---|---|---|---|---|
| Meia Praia | 1704 | 1704 | R$ 1,884,860 | R$ 2,102,707 | 129 | R$ 500 |
| Centro | 438 | 438 | R$ 2,100,000 | R$ 2,323,561 | 131 | R$ 1 |
| Morretes | 155 | 155 | R$ 845,000 | R$ 1,276,781 | 70 | R$ 300 |
| Andorinha | 473 | 473 | R$ 1,700,000 | R$ 1,763,616 | 122 | R$ 490 |
| Castelo Branco | 299 | 299 | R$ 1,679,750 | R$ 1,747,194 | 125 | R$ 391 |

## 7. Foco Meia Praia e Centro

- **Meia Praia (todos):** 3467 total | 3467 com preco | Mediana R$ 2,300,000 | Media R$ 3,056,153 | Min R$ 557,957 | Max R$ 44,000,000 | Area med 145 m2
- **Meia Praia (apto):** 3414 total | 3414 com preco | Mediana R$ 2,306,900 | Media R$ 3,047,081 | Min R$ 557,957 | Max R$ 44,000,000 | Area med 144 m2
- **Meia Praia (apto 3q):** 1704 total | 1704 com preco | Mediana R$ 1,884,860 | Media R$ 2,102,707 | Min R$ 690,000 | Max R$ 11,349,790 | Area med 129 m2
- **Centro (todos):** 1010 total | 1010 com preco | Mediana R$ 2,600,000 | Media R$ 3,416,479 | Min R$ 250,000 | Max R$ 17,500,000 | Area med 149 m2
- **Centro (apto):** 985 total | 985 com preco | Mediana R$ 2,600,000 | Media R$ 3,409,492 | Min R$ 250,000 | Max R$ 17,500,000 | Area med 149 m2
- **Centro (apto 3q):** 438 total | 438 com preco | Mediana R$ 2,100,000 | Media R$ 2,323,561 | Min R$ 685,000 | Max R$ 6,538,000 | Area med 131 m2

### Meia Praia 3q detalhado (comparar com 2q para investimento)
- Meia Praia apto 2q: 244 total | 244 com preco | Mediana R$ 1,075,000 | Area med 85 m2 | Cond med R$ 450
- Meia Praia apto 3q: 1704 total | 1704 com preco | Mediana R$ 1,884,860 | Area med 129 m2
- Centro apto 2q: 89 total | 89 com preco | Mediana R$ 1,150,000
- Centro apto 3q: 438 total | 438 com preco | Mediana R$ 2,100,000

## 8. Caminho seguido (raciocinio)

- **Arquivos:** `data/VivaReal_Itapema.csv` (8329) como base unica, sem JOIN com Details/Mesh/Price nesta etapa. `analysis/base_analitica_itapema.csv` usado apenas como referencia para saber que demanda foca em 2-3q Meia Praia/Centro, mas nao foi unido aqui.
- **Colunas:** `sale_price` (preco), `bedrooms` (filtro 3q), `usable_area` (comparacao tamanho), `suburb` (bairro), `monthly_condo_fee` (custo), `listing_type` (filtrar apartamento), `bathrooms/parking_spaces/amenities` (contexto). `rental_price` ignorada (99.98% vazio).
- **Filtros:** `listing_type==apartamento` para comparar com aluguel (7529 de 8329); `bedrooms==3` para foco (cerca 40% dos aptos); `suburb.lower()==meia praia/centro` para foco demanda; `sale_price>0` para validos; `0<usable_area<10000` para area valida.
- **Metricas:** `count`, `median`, `mean`, `min`, `max`, `quantile(0.99)` para preco; `median` para area/condominio; `value_counts` para bairros/quartos.
- **Decisoes:** Manter `suburb` nulos como SEM_BAIRRO (nao dropar), normalizar `suburb` com lower+strip para agrupar `Meia Praia` variants, nao excluir precos altos (44M) mas sinalizar, excluir area 0 e 188000, manter `amenities=[]` como legitimo, nao calcular ROI (so preco de compra).
- **Como levou aos resultados:** Primeiro inventariou colunas e qualidade (mostrou que preco e quartos estao 97% validos, mas condominio 30% falha), depois explorou preco geral (mediana 1.75M), depois filtrou 3q (mediana ~1.9M para apto 3q), depois quebrou por bairro (Meia Praia 3q ~1.8M vs Centro 3q ~2.1M) - mostrou que Meia Praia tem mais volume e preco ligeiramente menor que Centro para mesmo 3q, preparando cruzamento futuro com `price_mediano` de aluguel (2-3q Meia Praia) sem recomendar ainda.
