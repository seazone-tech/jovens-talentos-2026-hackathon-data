# Análise Independente - Tese Compactos (studio/1q) no Centro

> **Objetivo:** Testar se dados **sustentam, enfraquecem ou não permitem concluir** que compactos Centro são mais eficientes | **Mesma metodologia e premissa 60% (18d)** que Perguntas 1-3 | **Sem score, sem escolha final automática** | `data/` intacto

## 1. Universo e amostra (DADO OBSERVADO)

| Perfil | Airbnb total | Com preço | Cobertura | Viva total | Com sale_price | Cobertura Viva | Área med | Preço/m² | Alta (≥15) |
|---|---|---|---|---|---|---|---|---|---|
| Studio Centro (0q) | 2 | 0 | 0% | 0 | 0 (0%) | nanm² | R$ nan | 0 (0%) |
| 1q Centro | 116 | 78 | 67% | 22 | 22 (100%) | 42m² | R$ 14,574 | 31 (27%) |
| Compactos Centro (0q+1q) | 118 | 78 | 66% | 22 | 22 (100%) | 42m² | R$ 14,574 | 31 (26%) |
| 2q Centro | 183 | 65 | 36% | 89 | 89 (100%) | 86m² | R$ 13,068 | 34 (19%) |
| 2q Meia Praia | 723 | 187 | 26% | 244 | 244 (100%) | 85m² | R$ 12,929 | 151 (21%) |
| 3q Meia Praia | 1451 | 327 | 23% | 1704 | 1704 (100%) | 129m² | R$ 14,957 | 242 (17%) |
| 2q Morretes | 229 | 51 | 22% | 1044 | 1044 (100%) | 69m² | R$ 11,551 | 30 (13%) |
| 4q Meia Praia | 286 | 60 | 21% | 1327 | 1327 (100%) | 188m² | R$ 18,519 | 33 (12%) |
| 3q Centro | 211 | 45 | 21% | 438 | 438 (100%) | 131m² | R$ 15,789 | 22 (10%) |

> **Cobertura pequena = risco:** Studio Centro 0% com preço (0/2) é **insuficiente** (nenhuma mediana). 1q Centro 67% (78/116) é boa para Airbnb, mas **Viva 22 (<50) é pequena** para compra. **Critério de robustez:** ≥100 Airbnb e ≥30 com preço = robusto; ≥50 e ≥20 = moderado; <15 = pequeno; 0 = insuficiente. **Compactos (0q+1q) é idêntico a 1q** porque studio contribui 0 (2 Airbnb, 0 com preço, 0 Viva).

**Comparação com 2,3,4q (mesmo critério):**
- 2q Centro: 183 Airbnb (65 com preço, 36% cobertura) - **moderado** (65≥30)
- 2q Meia Praia: 723 Airbnb (187, 26%) - **robusto**
- 3q Meia Praia: 1451 (327, 23%) - **robusto**
- 4q Meia Praia: 286 (60, 21%) - **pequeno** (60 com preço, mas 286 total <100? Na verdade 286≥100, mas 60 com preço = moderado)
- 2q Morretes: 229 (51, 22%) - **moderado**

### Volume Viva vs Airbnb (não somar)
- **Airbnb (oferta temporada):** 2q MP 723, 3q MP 1451, 4q MP 286, 2q Centro 183, 1q Centro 116, compactos 118, studio 2 - **Meia Praia 4,7× Centro**
- **Viva (oferta venda):** 2q MP 244, 3q MP 1704, 4q MP 1327, 2q Centro 89, 1q Centro 22, compactos 22, studio 0 - **Meia Praia 19× Centro para 3q**, **7× para 2q**
- **Não somar:** 723+244=967 mistura mercados diferentes (temporada vs venda) - manter separado.

## 2. Receita potencial (DADO vs PREMISSA vs RESULTADO)

| Perfil | Diária (DADO) | Receita 40% ano (RESULTADO) | Receita 60% ano | Receita 80% ano | Qtd com preço (DADO) |
|---|---|---|---|---|---|
| Studio Centro (0q) | NaN (sem dados) | R$ nan | R$ nan | R$ nan | 0/2 (0%) |
| 1q Centro | R$ 450 | R$ 64,800 | R$ 97,200 | R$ 129,600 | 78/116 (67%) |
| Compactos Centro (0q+1q) | R$ 450 | R$ 64,800 | R$ 97,200 | R$ 129,600 | 78/118 (66%) |
| 2q Centro | R$ 580 | R$ 83,520 | R$ 125,280 | R$ 167,040 | 65/183 (36%) |
| 2q Meia Praia | R$ 460 | R$ 66,240 | R$ 99,360 | R$ 132,480 | 187/723 (26%) |
| 3q Meia Praia | R$ 700 | R$ 100,800 | R$ 151,200 | R$ 201,600 | 327/1451 (23%) |
| 2q Morretes | R$ 498 | R$ 71,712 | R$ 107,568 | R$ 143,424 | 51/229 (22%) |
| 4q Meia Praia | R$ 1075 | R$ 154,800 | R$ 232,200 | R$ 309,600 | 60/286 (21%) |
| 3q Centro | R$ 790 | R$ 113,760 | R$ 170,640 | R$ 227,520 | 45/211 (21%) |

> **Diária:** `price_mediano` median por anúncio onde `com_preco>0` (DADO OBSERVADO, 21-67% cobertura). **Receita:** `diária×30×occ×12` (RESULTADO) com **PREMISSA 60% =18 dias/mês** (não dado real, sem ocupação observada). **Studio: NaN** - sem diária, sem receita estimável.

**Comparação receita 60% (RESULTADO):**
- 1q Centro: R$ 97,200/ano (450×216) - robusto
- Compactos Centro (0q+1q): R$ 97,200/ano (450×216) - pequeno (Viva <30)
- 2q Centro: R$ 125,280/ano (580×216) - robusto
- 2q Meia Praia: R$ 99,360/ano (460×216) - robusto
- 3q Meia Praia: R$ 151,200/ano (700×216) - robusto
- 2q Morretes: R$ 107,568/ano (498×216) - robusto
- 4q Meia Praia: R$ 232,200/ano (1075×216) - robusto
- 3q Centro: R$ 170,640/ano (790×216) - moderado

## 3. Investimento (compra e retorno, sem inventar)

| Perfil | Preço compra med (DADO) | Receita 60% ano (RESULTADO) | Retorno bruto 60% (RESULTADO) | Lucro 60% (RESULTADO) | ROI 60% (RESULTADO) | Payback 60% | Robustez |
|---|---|---|---|---|---|---|---|
| Studio Centro (0q) | NaN | NaN | NaN | NaN | NaN | NaN | insuficiente |
| 1q Centro | R$ 890,000 | R$ 97,200 | 10.92% | R$ 67,844 | 7.62% | 13.1a | robusto |
| Compactos Centro (0q+1q) | R$ 890,000 | R$ 97,200 | 10.92% | R$ 67,844 | 7.62% | 13.1a | pequeno (Viva <30) |
| 2q Centro | R$ 1,150,000 | R$ 125,280 | 10.89% | R$ 89,120 | 7.75% | 12.9a | robusto |
| 2q Meia Praia | R$ 1,075,000 | R$ 99,360 | 9.24% | R$ 66,676 | 6.20% | 16.1a | robusto |
| 3q Meia Praia | R$ 1,884,860 | R$ 151,200 | 8.02% | R$ 106,860 | 5.67% | 17.6a | robusto |
| 2q Morretes | R$ 790,000 | R$ 107,568 | 13.62% | R$ 77,893 | 9.86% | 10.1a | robusto |
| 4q Meia Praia | R$ 3,600,000 | R$ 232,200 | 6.45% | R$ 167,940 | 4.67% | 21.4a | robusto |
| 3q Centro | R$ 2,100,000 | R$ 170,640 | 8.13% | R$ 124,244 | 5.92% | 16.9a | moderado |

> **Custos usados exatamente como em `analisar_roi.py`:** `condo_med (>0) ×12` (DADO Viva, cov 41-62% pos), `IPTU median (>0)` (DADO, 33-56% pos), `cleaning_fee median × (diárias_ano/5)` (DADO `cleaning_fee` 240-350 + PREMISSA `avg_stay=5`), `comissão 15%` (PREMISSA). **Studio sem diária/preço: sem receita/lucro/ROI calculável.**

**Note:** Retorno bruto = `receita/preço` (sem custos), ROI = `(receita - custos)/preço` (com custos). **Não inventado:** studio 0 Viva, 2 Airbnb com 0 com preço → todos NaN, corretamente sem cálculo.

## 4. Robustez

| Perfil | Airbnb | Com preço | Cobertura | Viva | Classificação | Motivo |
|---|---|---|---|---|---|
| Studio Centro (0q) | 2 | 0 (0%) | 0 | **insuficiente** | 0 com preço, 0 Viva - nenhuma mediana |
| 1q Centro | 116 | 78 (67%) | 22 | **robusto** | 78 com preço (67% de 116) - robusto para Airbnb, mas Viva 22 (<50) - pequeno para compra |
| Compactos Centro (0q+1q) | 118 | 78 (66%) | 22 | **pequeno (Viva <30)** | 78 com preço de 118 (66%, idêntico a 1q), Viva 22 (<50) - pequeno para escala 10-20 (45-90% do estoque) |
| 2q Centro | 183 | 65 (36%) | 89 | **robusto** | 65 com preço (36% de 183) - moderado, Viva 89 (<100) - moderado |
| 2q Meia Praia | 723 | 187 (26%) | 244 | **robusto** | 187 com preço (26% de 723), 244 Viva - robusto |
| 3q Meia Praia | 1451 | 327 (23%) | 1704 | **robusto** | 327 com preço (23% de 1451), 1704 Viva - robusto |
| 2q Morretes | 229 | 51 (22%) | 1044 | **robusto** | 51 com preço (22% de 229), 1044 Viva - moderado |
| 4q Meia Praia | 286 | 60 (21%) | 1327 | **robusto** | 60 com preço (21% de 286) - pequeno (60) |
| 3q Centro | 211 | 45 (21%) | 438 | **moderado** |  |

> **Não tratar mediana com poucas observações como equivalente a centenas:** 4q MP 60 com preço tem erro padrão da mediana ~1,5× maior que 3q MP 327; 1q Centro Viva 22 tem erro padrão ~3× maior que 3q MP 1704.

## 5. Comparação (onde compactos têm vantagem e onde não)

| Comparação | Compactos Centro | Concorrente | Vantagem compactos? | Números |
|---|---|---|---|---|
| Compactos vs 2q Centro | Retorno 10.92% vs 10.89% (Sim) | Preço R$ 890,000 vs 1,150,000 (Sim (menor capital)) | Volume Viva 22 vs 89 (Não) | Diária 450 vs 580 |
| Compactos vs 2q Meia Praia | Retorno 10.92% vs 9.24% (Sim) | Preço R$ 890,000 vs 1,075,000 (Sim (menor capital)) | Volume Viva 22 vs 244 (Não) | Diária 450 vs 460 |
| Compactos vs 3q Meia Praia | Retorno 10.92% vs 8.02% (Sim) | Preço R$ 890,000 vs 1,884,860 (Sim (menor capital)) | Volume Viva 22 vs 1704 (Não) | Diária 450 vs 700 |
| Compactos vs 2q Morretes | Retorno 10.92% vs 13.62% (Não) | Preço R$ 890,000 vs 790,000 (Não) | Volume Viva 22 vs 1044 (Não) | Diária 450 vs 498 |

**Onde compactos têm vantagem (DADO):** Preço menor que todos (890k <1,07M 2q MP, <1,15M 2q Centro, <1,88M 3q MP) e retorno bruto **10,92% >9,24% (2q MP, +1,68pp) e >8,02% (3q MP, +2,90pp)**, **empatado com 2q Centro 10,89% (+0,03pp)**.

**Onde compactos NÃO têm vantagem (DADO):** Diária 450 <580 (2q Centro, -22%), <700 (3q MP, -36%), <1075 (4q MP, -58%); Receita 97.200 <125.280 (2q Centro, -22%), <151.200 (3q MP, -36%), <232.200 (4q MP, -58%); Volume Viva 22 vs 89 (2q Centro, 4× menor), vs 244 (11×), vs 1704 (77×); **Retorno NÃO supera Morretes 13,62% e 1q MP 11,94%**.

**Evidências que contrariam tese (não tentei confirmar):**
- **Studio 0q: 0 com preço, 0 Viva - sem evidência, contradiz 'studio/1q' como conjunto** (tese inclui studio, mas studio não tem dados).
- **1q MP (81 Airbnb, 20 com preço, 58 Viva, 877k, 485, 11,94% retorno) tem retorno maior (11,94% >10,92%)** com diária 485 >450 e preço 877k <890k, e volume Viva 58 vs 22 (2,6× maior) - **compactos Centro não é o pico, 1q MP é maior**.
- **2q Morretes 13,62% (498, 790k, 229/1044) >10,92%** com volume Viva 1044 vs 22 (47×) - **compactos não é o mais eficiente geral**.
- **Área 42m² vs 85-86m² (2q) - 50% menor**, preço/m² 21.190 vs 12.929 (+64% mais caro por m²) - **paga mais por m² para receita menor**.
- **Alta 31 (26,7%) vs 2q MP 151 (20,9%) - alta similar, não superior**; guest fav 33 vs 173 (2q MP) vs 298 (3q MP) - **não domina demanda**.

## 6. Conclusão independente

**Classificação (escolha 1 de 3):**

**Para Studio Centro (0q) isolado: INCONCLUSIVA** - 0 com preço, 0 Viva, sem diária/receita/retorno - **nenhuma evidência, não pode ser avaliado; incluir 'studio' na tese já é incorreto.**

**Para 1q Centro isolado e Compactos (0q+1q) combinado (que é idêntico a 1q): PARCIALMENTE SUSTENTADA com ressalvas graves, mas no conjunto da tese NÃO SUSTENTADA como 'mais eficiente'**

**Escolho: NÃO SUSTENTADA como 'mais eficiente' isolado (e INCONCLUSIVA para studio).**

* **Parcialmente sustentada para 1q:** Retorno bruto 10,92% (97.200/890k) é **0,03pp acima de 2q Centro 10,89% (empate técnico)** e **+1,68pp vs 2q MP 9,24% e +2,90pp vs 3q MP 8,02%**, com capital menor (890k vs 1,07M/1,88M) - **eficiência por capital existe, mas marginal (0,03pp vs 2q Centro).**
* **Não sustentada como 'mais eficiente':** **2q Morretes 13,62% e 1q MP 11,94% têm retorno maior** com volume Viva 1044/58 vs 22, e **2q Centro tem retorno praticamente idêntico (10,89% vs 10,92%, +0,03pp) com diária maior (580 vs 450) e receita maior (125.280 vs 97.200, +29%)** - **compactos não supera**.
* **Inconclusiva para escala Seazone (3000 imóveis):** **Viva 22 (<50) é insuficiente** para comprar 10 unidades (45% do estoque) vs 2q MP 244 (4,1%) e 3q MP 1704 (0,6%), e **Airbnb 118 vs 723/1451** - **não escalável**, mesmo com 66% cobertura (78 com preço).

**Números que justificam:**
- **A favor (retorno marginal):** 10,92% >9,24% (+1,68pp) e >8,02% (+2,90pp), ≈10,89% (+0,03pp) - **empate técnico com 2q Centro**.
- **Contra (volume):** Viva 22 vs 89 (4×), vs 244 (11×), vs 1704 (77×) - **insuficiente**.
- **Contra (receita):** 97.200 vs 125.280 (2q Centro, -22%), vs 99.360 (2q MP, -2%), vs 151.200 (3q MP, -36%) - **receita menor que todos os comparados exceto 2q MP (similar)**.
- **Contra (amplitude):** 1q MP 11,94% >10,92% e Morretes 13,62% >10,92% - **não é pico**.
- **Contra (studio):** 0 dados - **inconclusivo**.

**Frase final obrigatória:**

**“Os dados não sustentam a tese de que apartamentos compactos (studio/1 quarto) no Centro são a aposta mais eficiente para a Seazone; para 1 quarto no Centro há sinais de eficiência similar a 2 quartos no Centro (10,92% vs 10,89%, empate técnico) e superior a 2-3 quartos em Meia Praia, mas com volume à venda muito pequeno (22 vs 89-1704) e sem dados para studio (0 com preço), além de retorno inferior a 1 quarto em Meia Praia (11,94%) e 2 quartos em Morretes (13,62%), por isso a evidência é insuficiente para afirmar que é a mais eficiente e, para escala Seazone, é inconclusiva.”**

**Perfil mais defensável (somente se dados permitirem, sem escolher vencedor final da Pergunta 4):** **1q Centro não é mais defensável que 2q Centro (empate técnico em retorno com diária e receita menores e volume 4× menor) e 2q Meia Praia (723 vs 118, 187 com preço vs 78, retorno 9,24% vs 10,92% mas com volume 6× maior e preço/m² 12.929 vs 21.190 mais barato). Entre compactos, 1q Centro tem **retorno similar, mas não superior de forma robusta**, então **2q Centro (580, 125.280, 89/65, 1,15M, 10,89%) ou 2q Meia Praia (460, 99.360, 723/187, 1,07M, 9,24%) permanecem mais defensáveis por volume e preço/m²** - **compactos Centro só seria defensável para nicho de capital muito baixo (890k) e se Seazone aceitar volume pequeno (22).**
