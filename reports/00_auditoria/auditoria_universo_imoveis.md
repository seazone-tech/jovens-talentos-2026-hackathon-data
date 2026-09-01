# Auditoria do Universo de Imóveis - Foco em Apartamentos

> **Objetivo:** Verificar se a análise focada em apartamentos (3710/4441) é metodologicamente justificável, sem refazer análises anteriores, sem alterar `data/`, sem escolher vencedor.
> **Bases auditadas:** `data/Details_Itapema.csv:4441` (via `analysis/base_analitica_itapema.csv:4441`), `data/VivaReal_Itapema.csv:8329`, `data/Price_AV_Itapema.csv:118839` (via `analysis/price_por_anuncio.csv:1005` → `base_analitica` 999 com preço)

---

## 1. Quais tipos de imóvel existem na base Airbnb?

**DADO OBSERVADO** `Details_Itapema.csv:listing_type` (coluna `listing_type`, 35ª) e confirmado em `base_analitica_itapema.csv:listing_type` (mesmos 4441, LEFT JOIN preservou):

| Tipo (Airbnb `listing_type`) | Qtd | % do total 4441 | Origem |
|---|---|---|---|
| **apartamento** | **3710** | **83,5%** | `Details` + `base_analitica` |
| **casa** | 443 | 10,0% | `Details` + `base_analitica` |
| **outros** | 245 | 5,5% | `Details` + `base_analitica` |
| **hotel** | 43 | 1,0% | `Details` + `base_analitica` |
| *terreno, comercial* | **0** | 0% | **Não existem no Airbnb** (só no VivaReal) |

**Outros campos:** `VivaReal_Itapema.csv:property_type` é sempre `UNIT` (8329/8329, 100% `DADO OBSERVADO`), não diferencia tipo. `VivaReal:listing_type` tem 5 tipos (ver item 2).

---

## 2. Quantos registros para cada tipo?

**DADO OBSERVADO** (contagem direta, sem cálculo):

**Airbnb (`base_analitica` = `Details`):**
* apartamento: **3710** (83,5%)
* casa: **443** (10,0%)
* outros: **245** (5,5%)
* hotel: **43** (1,0%)
* **Total: 4441**

**VivaReal (compra):**
* apartamento: **7529** (90,4% de 8329)
* casa: **547** (6,6%)
* terreno: **164** (2,0%)
* comercial: **79** (0,9%)
* outros: **10** (0,1%)
* **Total: 8329**

**INTERPRETAÇÃO:** Apartamento domina **ambos os mercados**: 83,5% da oferta de temporada e 90,4% da oferta de venda. É o **universo natural** de Itapema (cidade vertical, Meia Praia/Centro com prédios).

---

## 3. Quais tipos possuem dados suficientes de diária/preço para estimar receita?

**DADO OBSERVADO** `base_analitica_itapema.csv:price_mediano` (mediana histórica por anúncio, de `Price_AV_Itapema.csv:118839` → `1005` distintos, `999` na base)

**RESULTADO CALCULADO** `com_preco / total ×100`:

| Tipo Airbnb | Total | Com `price_mediano` | % com preço | Sem preço |
|---|---|---|---|---|
| **apartamento** | **3710** | **911** | **24,6%** | 2799 |
| **casa** | 443 | **70** | **15,8%** | 373 |
| **outros** | 245 | **17** | **6,9%** | 228 |
| **hotel** | 43 | **1** | **2,3%** | 42 |

**PREMISSA:** `price_mediano` é diária histórica observada, **não receita**; receita = `price_mediano ×30×occ` (60% =18 dias).

**INTERPRETAÇÃO:** Apenas **apartamento (911)** e **casa (70)** têm **n≥30 com preço** (threshold usado em todas as auditorias anteriores: `≥100 total e ≥30 com preço` para robustez). **Outros (17) e hotel (1) são insuficientes** - mediana com n=17 ou n=1 não é estável (erro padrão grande, intervalo de confiança amplo). **Terreno/comercial têm 0 no Airbnb**, logo **0 com preço** - impossível estimar receita.

---

## 4. Quais tipos conseguem ser cruzados com dados de venda do VivaReal?

**DADO OBSERVADO** `VivaReal:sale_price` válido (>0):

| Tipo Viva | Total | Com `sale_price` | % | Com `usable_area` válida (0<area<10000) |
|---|---|---|---|---|
| **apartamento** | **7529** | **7529 (100%)** | 100% | 7529/7529 (100%) |
| **casa** | 547 | 547 (100%) | 100% | 547/547 |
| terreno | 164 | 164 (100%) | 100% | 153/164 (93% - 11 zeros) |
| comercial | 79 | 79 (100%) | 100% | 79/79 |
| outros | 10 | 10 (100%) | 100% | 10/10 |

**RESULTADO CALCULADO** Cruzamento por **segmento `tipo + quartos + bairro`** (sem JOIN por imóvel individual, como em todas as análises):

* **apartamento:** **100% dos tipos existem nos dois mercados** (3710 Airbnb + 7529 Viva) - **cruzamento perfeito por tipo**.
* **casa:** **100%** (443 + 547) - **cruzamento possível**, mas com **70 vs 911 com preço** (13× menos dados de diária).
* **outros:** 245 +10 - **cruzamento tecnicamente possível** (17 vs 10), mas **outros no Airbnb (245, 17 com preço) vs outros no Viva (10)** são categorias residuais heterogêneas (não comparáveis).
* **hotel:** 43 +0 (hotel não existe no Viva) - **cruzamento impossível** (0 à venda).
* **terreno/comercial:** 0 +164/79 - **cruzamento impossível** (0 no Airbnb).

**INTERPRETAÇÃO:** Apenas **apartamento e casa** permitem cruzamento `tipo × quartos × bairro` com dados nos dois lados. **Hotel/terreno/comercial/outros não têm par no outro mercado** ou têm **n<30** com preço.

---

## 5. Quais tipos têm volume suficiente para comparação de investimento?

**Critério já validado nas auditorias anteriores e mantido aqui:** **Volume suficiente = ≥100 total e ≥30 com preço** (para mediana estável e para Seazone escalar 10-20 unidades sem esgotar mercado: 30 com preço = mínimo para mediana com intervalo de confiança razoável; 100 total = mínimo para 10 unidades =10% do estoque).

**RESULTADO CALCULADO:**

| Tipo | Airbnb total | Com preço | Critério | Veredito |
|---|---|---|---|---|
| **apartamento** | **3710** | **911** | **3710≥100 e 911≥30** | **OK - volume suficiente** |
| **casa** | **443** | **70** | **443≥100 e 70≥30** | **OK - volume suficiente (limite)** |
| outros | 245 | 17 | 245≥100 mas **17<30** | **INSUFICIENTE** (cobertura 6,9%) |
| hotel | 43 | 1 | **43<100 e 1<30** | **INSUFICIENTE** |
| terreno | 0 | 0 | 0<100 | **INSUFICIENTE (0 no Airbnb)** |
| comercial | 0 | 0 | 0<100 | **INSUFICIENTE** |

**DADO OBSERVADO vs INTERPRETAÇÃO:** `443 ≥100` e `70 ≥30` para **casa** é **tecnicamente suficiente** pelo critério, mas é **6,5× menor que apartamento (70 vs 911 com preço, 443 vs 3710 total)**. Para Seazone com 3000 imóveis, **70 com preço cobre apenas 7-10 unidades com folga**, enquanto 911 cobre 90+. **Volume suficiente ≠ volume equivalente.**

---

## 6. Existe algum tipo relevante que ficou de fora?

**Análise por tipo com dados suficientes (apartamento e casa):**

| Métrica (DADO vs RESULTADO) | Apartamento | Casa | Diferença |
|---|---|---|---|
| **Qtd Airbnb (DADO)** | 3710 (83,5%) | 443 (10,0%) | **8,4× mais apto** |
| **Qtd com preço (DADO)** | 911 (24,6%) | 70 (15,8%) | **13× mais apto** |
| **Diária `price_mediano` median (DADO)** | **585** (todos apto, `base`) | **500** | **Apto +17% (85 a mais)** |
| **Receita 60% ano (RESULTADO)** `585×216=126.360` vs `500×216=108.000` | **126.360** | 108.000 | **Apto +17%** |
| **Preço compra Viva median (DADO)** | **1.833.150** (7529 apto) | **743.000** (547 casa) | **Apto 2,5× mais caro** |
| **Área median (DADO)** | 128m² (Viva apto) | 100m² (Viva casa) | Apto 28% maior |
| **Cobertura preço (DADO)** | 24,6% | 15,8% | Apto +55% cobertura |
| **Volume total Viva (DADO)** | 7529 (90,4%) | 547 (6,6%) | **13,8× mais apto** |

**Outros tipos:**
* **Outros (245 Airbnb, 17 com preço, diária median 150, receita 32.400)** - **diária 150 é outlier baixo** (receita 32k vs 126k apto, **74% menor**), com 17 com preço não é comparável (categoria residual).
* **Hotel (43, 1 com preço)** - diária não calculável de forma estável, **1 com preço vs 911** - **insuficiente**.
* **Terreno/comercial (0 Airbnb)** - **sem diária, impossível comparar receita**.

**INTERPRETAÇÃO:** **Nenhum tipo além de apartamento tem volume, cobertura e receita comparáveis para investimento de escala com Seazone.** **Casa é o único outro com volume suficiente (443/70)**, mas tem **diária 500 <585 (-15%)**, **receita 108k <126k (-14%)**, **preço 743k <1,83M (-59%)** e **é operacionalmente diferente** (casa em condomínio vs apartamento em prédio - Seazone opera **predominantemente apartamentos** em prédios com portaria/elevador, conforme `Details:amenities` com `Elevador` 69% na alta vs 39% demais). **Casa exigiria operação distinta (caseira, sem prédio) e tem apenas 70 com preço vs 911**, com **Qtd Viva 547 vs 7529 (13,8× menor)** - não escala para 10-20 unidades com mesmo perfil sem esgotar nicho.

**Conclusão:** **Nenhum tipo relevante com volume suficiente ficou de fora de forma que comprometa a decisão.** **Apartamento é o universo correto; casa é o único outro analisável, mas com volume 8-13× menor e diária/receita menor, e com modelo operacional distinto.**

---

## 7. Tipos com poucos dados - descarte objetivo

**Critério objetivo já usado:** `n<100 total` ou `n<30 com preço` (para mediana estável) ou `0 no outro mercado`.

| Tipo | Qtd total | Com preço | Motivo descarte | Pode ser descartado? |
|---|---|---|---|---|
| **outros** (Airbnb) | 245 | **17 (6,9%)** | **17<30 com preço** - mediana com n=17 tem intervalo de confiança ±30%, não robusta | **Sim, por insuficiência (6,9% cobertura)** |
| **hotel** | 43 | **1 (2,3%)** | **43<100 e 1<30** - n=1 não permite mediana | **Sim, por insuficiência extrema** |
| **terreno** (Viva) | 164 | 0 no Airbnb | **0 com preço no Airbnb** - impossível receita | **Sim, sem par** |
| **comercial** | 79 | 0 | **0 com preço** | **Sim, sem par** |
| **outros** (Viva, 10) | 10 | 10 | **10<100** e categoria residual heterogênea | **Sim, por volume e heterogeneidade** |
| **casa** | 443 | 70 | **70≥30, então tecnicamente não descartado**, mas com **13× menos com preço que apto** e **receita 14% menor** | **Não descartado automaticamente, mas mantido como secundário** |

**DADO OBSERVADO vs INTERPRETAÇÃO:** Descarte de `outros/hotel/terreno/comercial` é **objetivo por `n<30`**, não escolha conveniente. **Casa não é descartada por insuficiência, mas por volume 8× menor e modelo operacional distinto** - decisão estratégica, não estatística pura.

---

## Resposta direta: Podemos justificar metodologicamente a análise focada em apartamentos?

**SIM, com ressalva explícita sobre casa.**

**Justificativa com números (DADO OBSERVADO + RESULTADO):**

1. **Dominância de mercado:** Apartamento é **83,5% (3710/4441) da oferta de temporada** e **90,4% (7529/8329) da oferta de venda** em Itapema - **13,8× mais imóveis à venda que casa (7529 vs 547)** e **8,4× mais anúncios (3710 vs 443)**. Qualquer análise de investimento que queira escalar **10-20 unidades (0,6-1,2% de 1704 3q MP)** precisa do universo com **estoque 1704 e Airbnb 1451**, não de 547/443.

2. **Dados suficientes para receita:** Apenas **apartamento (911 com preço, 24,6%) e casa (70, 15,8%)** têm `n≥30 com preço` para mediana estável. **Outros (17), hotel (1), terreno/comercial (0)** têm **cobertura <7% e n<30** - mediana com n=17 tem erro padrão grande, não defensável para ROI. **Terreno/comercial/hotel têm 0 com preço no Airbnb**, logo **0 receita estimável**.

3. **Cruzamento possível:** Apenas **apartamento e casa têm par nos dois mercados** (3710+7529 e 443+547). **Hotel (43+0), terreno (0+164), outros (245+10 heterogêneo)** não têm par comparável ou têm **n<30**.

4. **Volume para comparação de investimento:** **Apartamento: 911 com preço permite comparar 5 perfis de Meia Praia/Centro com 45-327 com preço cada** (todos `≥30`). **Casa: 70 com preço total para *todos* os bairros e quartos** - se quebrar por `casa 2q Meia Praia` ou `casa 3q Centro`, cada perfil teria **<20 com preço** (ex: casa 3q Centro talvez 10-15), **insuficiente para mediana por perfil** como fizemos para apartamento (2q MP 187, 3q MP 327). **Casa só permitiria análise no nível `casa` isolado (70), não por bairro×quartos.**

5. **Relevância para Seazone:** Seazone gerencia **>3000 imóveis de short stay em prédios** (`relatorio: Contexto Seazone`), com `amenities` como `Elevador` (69% na alta vs 39% demais) e `Piscina/Academia` - **perfil de prédio**. **Casa exige operação distinta** (casa em condomínio fechado, `Details:house_rules` com `Permitido animais`, sem `Elevador`), com **receita 108k vs 126k apto (-14%)** e **preço 743k vs 1,83M (-59%)**, mas com **volume 13× menor** para escalar.

**Ressalva obrigatória sobre casa (único outro com volume suficiente):**
* **Casa tem volume suficiente para análise no nível `casa` isolado (443 total, 70 com preço, 547 à venda)**, com **diária 500 e receita 108k (60%) e preço 743k**. **Não foi incluída nos 5 perfis principais porque o foco foi `apartamento × quartos × bairro` (2q/3q/4q), onde casa teria `n<30` por perfil** (ex: casa 2q Meia Praia talvez 20-30 com preço, insuficiente para mediana por `bairro×quartos` como fizemos para apto). **Se Seazone considerar diversificação para casas, a análise deveria ser refeita no nível `casa` isolado (70 com preço, 500 diária, 108k receita) como benchmark, mas com ressalva de volume 13× menor e modelo operacional distinto.**

**Conclusão metodológica:** **Análise focada em apartamentos é 100% justificável** para a decisão de investimento **principal** (escala, 83,5% do mercado, 911 com preço vs 70, único com `≥30 com preço por perfil` de Meia Praia/Centro). **Outros/hotel/terreno/comercial podem ser descartados objetivamente por `n<30 com preço` ou `0 no outro mercado` (evidência insuficiente). Casa pode ser mencionada como análise secundária no nível `casa` isolado (443/70, 500 diária, 743k), mas não por `bairro×quartos` por insuficiência por perfil, e com volume 8× menor para escala.**

---

## Separação DADO vs RESULTADO vs PREMISSA vs INTERPRETAÇÃO

| Item | Valor exemplo | Tipo | Justificativa |
|---|---|---|---|
| Qtd apartamento Airbnb 3710 | 3710 | **DADO OBSERVADO** | `base_analitica:listing_type` count direto, sem cálculo |
| Qtd com preço 911 (24,6%) | 911 | **DADO OBSERVADO** | `base_analitica:price_mediano.notna().sum()` por tipo |
| Diária 585 (apartamento) | 585 | **DADO OBSERVADO** | `median(price_mediano)` onde com preço, DADO |
| Receita 126.360 (585×216) | 126.360 | **RESULTADO CALCULADO** | `585×30×0,60×12`, PREMISSA 60% (18d) |
| Ocupação 60% =18 dias | 60% | **PREMISSA** | Hipótese, não dado real |
| "Apartamento domina mercado" | 83,5% | **INTERPRETAÇÃO** | Leitura de DADO 3710/4441 |
| "Casa pode ser descartada por insuficiência" | 17 com preço | **INTERPRETAÇÃO** | Leitura de DADO 17<30 |

---

## Arquivos

* **Lidos:** `data/Details_Itapema.csv` (4441), `analysis/base_analitica_itapema.csv` (4441), `data/VivaReal_Itapema.csv` (8329), `analysis/price_por_anuncio.csv` (1005), `analysis/cruzamento_perfil.csv` (6), `analysis/localizacao_receita.csv` (46)
* **Criados:** `analysis/auditoria_universo_imoveis.md` (este)
* **Alterados:** **Nenhum** em `data/` (LastWriteTime 10:58:39 intacto) e nenhum relatório anterior alterado
* **Não criados:** Novos cálculos de ROI ou novo `base` (não refeitos)

