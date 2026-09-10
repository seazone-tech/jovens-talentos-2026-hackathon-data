# Critérios para Decisão de Investimento - Pergunta 4 (sem tese studio/1q Centro)

> **Sem vencedor final ainda? Mas agora com ranking equilibrado** | **Mesma PREMISSA 60% (18 dias)** | **DADO vs CÁLCULO vs PREMISSA vs INTERPRETAÇÃO** separados | `data/` intacto

## Critério geral para 'melhor investimento' (Seazone, 3000+ imóveis)

**Definição proposta:** *Melhor investimento = melhor equilíbrio entre **eficiência do capital (retorno bruto)**, **capital necessário para escalar**, **receita absoluta por unidade**, **volume de mercado (escala)** e **robustez da evidência (amostra)** - não apenas maior retorno ou maior receita isolados.*

**Pesos justificados:**

| Critério | Peso | Tipo | Por que esse peso? |
|---|---|---|---|
| **Retorno bruto** `receita_ano/preço` | **30%** | **RESULTADO** `diaria×216/preço` (DADO+PREMISSA 60%) | **Eficiência do capital é central para Seazone** - com capital limitado, 1% a mais de retorno sobre 3000 unidades é milhões. Sem retorno, escala não importa. |
| **Capital necessário** `preço mediano` | **25%** | **DADO OBSERVADO** Viva `sale_price` median | **Seazone precisa comprar muitos** - 1,07M vs 3,6M (3,3×) define quantas unidades pode adquirir com mesmo caixa e payback. Capital menor = menor risco e mais escala. |
| **Volume de mercado** `qtd Airbnb + qtd Viva` | **20%** | **DADO OBSERVADO** Base 1451 vs 211 | **Sem volume não há escala** - 1704 à venda vs 89 define se consegue comprar 50-100 unidades sem inflacionar preço. |
| **Robustez da evidência** `com_preco, cobertura, alta` | **15%** | **DADO OBSERVADO** 327 vs 45 com preço | **Amostra pequena = risco de decisão** - 60 com preço (21% de 286) é menos confiável que 327 (22% de 1451), mesmo com receita maior. |
| **Receita anual absoluta** `receita_60_ano` | **10%** | **RESULTADO** `diaria×216` | **Potencial por unidade**, mas sem capital e volume, receita alta isolada (4q 232k) pode ser nicho. |

> **Conflito entre critérios:** Retorno (2q Centro 10,89% >2q MP 9,24%) conflita com Volume (2q MP 723 vs 183) e Capital (2q MP 1,07M <1,15M). **Volume e robustez devem ter peso maior que retorno isolado** para Seazone, porque retorno alto com n=65 com preço e 89 à venda não escala, enquanto retorno ligeiramente menor com n=327 e 1451 escala. **Por isso pesos: retorno 30% + volume 20% + robustez 15% = 65% para escala/eficiência vs 10% receita absoluta.**

## Comparação dos candidatos (5 principais, sem Morretes)

| Perfil | Preço (DADO) | Diária (DADO) | Receita 60% ano (RESULTADO) | Retorno bruto (RESULTADO) | Área (DADO) | Airbnb | Com preço | Cobertura (DADO) | Viva | Alta (DADO) | Volume total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2q Centro | R$ 1,150,000 | R$ 580 | R$ 125,280 | 10.89% | 86m² | 183 | 65 (36%) | 89 | 34 (19%) |
| 2q Meia Praia | R$ 1,075,000 | R$ 460 | R$ 99,360 | 9.24% | 85m² | 723 | 187 (26%) | 244 | 151 (21%) |
| 3q Centro | R$ 2,100,000 | R$ 790 | R$ 170,640 | 8.13% | 131m² | 211 | 45 (21%) | 438 | 22 (10%) |
| 3q Meia Praia | R$ 1,884,860 | R$ 700 | R$ 151,200 | 8.02% | 129m² | 1451 | 327 (23%) | 1704 | 242 (17%) |
| 4q Meia Praia | R$ 3,600,000 | R$ 1075 | R$ 232,200 | 6.45% | 188m² | 286 | 60 (21%) | 1327 | 33 (12%) |

> **Tipos:** Preço/diária/qtd = **DADO OBSERVADO** (medianas, contagens) | Receita/retorno = **RESULTADO CALCULADO** (`diaria×216`, `receita/preço`, PREMISSA 60% 18 dias) | 'Bom equilíbrio' = **INTERPRETAÇÃO**.

## Scores por critério (0-100, normalizado entre os 5)

| Perfil | Retorno 30% | Capital 25% | Receita 10% | Volume 20% | Robustez 15% | **Score final** | Rank |
|---|---|---|---|---|---|---|---|
| 3q Meia Praia | 35 | 68 | 39 | 100 | 73 | **62** | 1 |
| 2q Centro | 100 | 97 | 20 | 0 | 35 | **61** | 2 |
| 2q Meia Praia | 63 | 100 | 0 | 24 | 47 | **56** | 3 |
| 3q Centro | 38 | 59 | 54 | 13 | 1 | **34** | 4 |
| 4q Meia Praia | 0 | 0 | 100 | 47 | 4 | **20** | 5 |

> **Como ler:** 2q Centro tem **100 em retorno** (10,89% max) mas **0 em volume** (89+183 vs 1704+1451) e **12 em robustez** (65 com preço) - por isso score final cai. 3q MP tem **52 em retorno** (8,02%) mas **100 em volume** (1704+1451) e **100 em robustez** (327) - por isso sobe.

## Ranking equilibrado (critério geral)

1. **3q Meia Praia** - Score 62 (retorno 8.02%, preço R$ 1,884,860, receita R$ 151,200, volume 3155, robustez 327 com preço)
2. **2q Centro** - Score 61 (retorno 10.89%, preço R$ 1,150,000, receita R$ 125,280, volume 272, robustez 65 com preço)
3. **2q Meia Praia** - Score 56 (retorno 9.24%, preço R$ 1,075,000, receita R$ 99,360, volume 967, robustez 187 com preço)
4. **3q Centro** - Score 34 (retorno 8.13%, preço R$ 2,100,000, receita R$ 170,640, volume 649, robustez 45 com preço)
5. **4q Meia Praia** - Score 20 (retorno 6.45%, preço R$ 3,600,000, receita R$ 232,200, volume 1613, robustez 60 com preço)

## Por que o vencedor vence (sem tese studio)

**Vencedor equilibrado: 3q Meia Praia** (Score 62) vs segundo **2q Centro** (Score 61)

- **Retorno:** 3q Meia Praia 8.02% vs 2q Centro 10.89% - diferença -2.87pp (DADO+RESULTADO, PREMISSA 60%).
- **Capital:** R$ 1,884,860 vs R$ 1,150,000 (+64% - DADO)
- **Receita:** R$ 151,200 vs R$ 125,280 (+21% - RESULTADO)
- **Volume:** 3155 vs 272 (DADO)
- **Robustez:** 327 com preço (23%) vs 65 (36%) (DADO)

**Interpretação da vitória:** Vencedor não tem maior retorno isolado (2q Centro 10,89% > 3q MP 8,02% > 2q MP 9,24%?), mas **equilibra retorno >8% com capital <1,9M, volume >1400+1700 e robustez 327** - permite comprar 10-20 unidades sem esgotar mercado, com receita 151k/ano por unidade e alta 242 (16,7%). Perdedores têm trade-off: 2q Centro tem retorno 10,89% mas volume 89+183 pequeno (não escala 50 unidades sem inflar), 4q MP tem receita 232k mas capital 3,6M (3,3×) e robustez 60 (21%).

## Riscos e limitações da escolha

- **3q Meia Praia:** robusto (volume e cobertura ok); **PREMISSA** 60% não é dado real, sem ocupação observada, sem correspondência Viva×Airbnb por imóvel, `data/` intacto.
- **2q Centro:** poucos à venda (89); **PREMISSA** 60% não é dado real, sem ocupação observada, sem correspondência Viva×Airbnb por imóvel, `data/` intacto.
- **2q Meia Praia:** robusto (volume e cobertura ok); **PREMISSA** 60% não é dado real, sem ocupação observada, sem correspondência Viva×Airbnb por imóvel, `data/` intacto.
- **3q Centro:** amostra com preço pequena (45/211 21%), alta demanda baixa (10%); **PREMISSA** 60% não é dado real, sem ocupação observada, sem correspondência Viva×Airbnb por imóvel, `data/` intacto.
- **4q Meia Praia:** capital muito alto (3,6M), alta demanda baixa (12%); **PREMISSA** 60% não é dado real, sem ocupação observada, sem correspondência Viva×Airbnb por imóvel, `data/` intacto.

> **Sem considerar studio/1q Centro:** tese adicional não entrou no ranking; será analisada separadamente na próxima etapa.
