# Auditoria ROI - Pergunta 1

> **Status: [APROVADO COM RESSALVAS]**  
> **Arquivos auditados:** `analysis/analisar_roi.py:1`, `analysis/relatorio_roi.md:1`, `analysis/roi_perfil.csv:16`, `analysis/relatorio_cruzamento_compra_aluguel.md:1`, `analysis/cruzamento_perfil.csv:6`, `analysis/relatorio_receita.md:48`, `data/VivaReal_Itapema.csv:8329`, `analysis/base_analitica_itapema.csv:4441`  
> **Conclusão auditoria:** Nenhum erro matemático encontrado. Metodologia é defensável para hackathon com premissas explícitas, mas possui ressalvas de amostra e premissas que devem ser declaradas no vídeo. Pode ser usado como base da Pergunta 1 com distinção entre ROI estimado e fato.

---

## 1. Verificar preço de compra

**Método em `analisar_roi.py:54-56`:** `compra_valid = sub_v[sub_v["sale_price"]>0]` + `median()` por perfil filtrado `listing_type_norm=="apartamento" & bedrooms==q & suburb_norm==b_norm` com `suburb_norm = strip().lower()`.

**Verificação refeita (reproduzindo):**
| Perfil | Qtd Viva | Filtrados | Mediana sale_price auditada | Mediana em roi_perfil.csv | Confere? |
|---|---|---|---|---|---|
| 2q Meia Praia | 244 | `apartamento & 2 & meia praia` | **1.075.000** | 1.075.000 | Sim |
| 3q Meia Praia | 1704 | 3 & meia praia | **1.884.860** | 1.884.860 | Sim |
| 4q Meia Praia | 1327 | 4 & meia praia | **3.600.000** | 3.600.000 | Sim |
| 2q Centro | 89 | 2 & centro | **1.150.000** | 1.150.000 | Sim |
| 3q Centro | 438 | 3 & centro | **2.100.000** | 2.100.000 | Sim |

*Imóveis com preço inválido:* `sale_price>0` exclui 0/NaN - em VivaReal 0 inválidos (100% válidos, `relatorio_vivareal.md:44`), então nenhum excluído nos 5 perfis (todos >0). Correto.

*Mediana adequada?* Sim, é a principal referência definida no cruzamento (`relatorio_cruzamento:10`). Distribuição tem outliers (P99 6,4M para 3q MP, max 11,3M) - mediana é robusta vs média (2,10M para 3q MP). **Defensável.** Não há problema evidente de outlier puxando mediana.

**Parecer:** **Aprovado.** Filtros corretos, normalização correta, mediana adequada.

---

## 2. Verificar diária

**Método `analisar_roi.py:70`:** `diaria_med = sub_b["price_mediano"].median()` onde `sub_b` filtrado `apartamento & number_of_bedrooms==q & suburb_norm==b_norm`, `price_mediano` já é `median(price)` por anúncio em `price_por_anuncio.csv` (118.839 observações -> 1005 medianas).

**price_mediano representa diária histórica por anúncio:** Sim, é `price_mediano` de `price_por_anuncio.csv:1` (colunas `price_min/max/medio/mediano` por `airbnb_listing_id`), convertido `pd.to_numeric`. **Não confundido com receita** - relatório separa e fórmula usa `diaria * dias`.

*Mediana das medianas:* Sim, `median()` das 60-327 medianas por perfil (robusta ao outlier R$29.000 `31397917` com `price_max 29000` mas `price_mediano 250` - não distorce).

**Cobertura por perfil (recalculada):**

| Perfil | Airbnb total | Com preço | % | Sem preço | Avaliação cobertura |
|---|---|---|---|---|---|
| 2q Meia Praia | 723 | 187 | **25,9%** | 536 | Suficiente (187) |
| 3q Meia Praia | 1451 | 327 | 22,5% | 1124 | Suficiente (327) |
| 4q Meia Praia | 286 | 60 | **21,0%** | 226 | **Pequena (60) - ressalva** |
| 2q Centro | 183 | 65 | 35,5% | 118 | Suficiente (65) |
| 3q Centro | 211 | 45 | **21,3%** | 166 | **Pequena (45) - ressalva** |

Destaque: **4q Meia Praia (60) e 3q Centro (45)** têm amostra <30% e <50 observações, mediana menos estável. **2q Meia Praia (187) e 3q Meia Praia (327) têm cobertura adequada.** O relatório já sinaliza isso em `relatorio_roi.md:113-115` e é correto.

**Parecer:** **Aprovado com ressalva** - método correto, mas 4q e 3q Centro têm amostra pequena e devem ser apresentados como "dados insuficientes/nicho" (o relatório faz).

---

## 3. Verificar receita

**Fórmulas `analisar_roi.py:109-112`:**
```python
diarias_mes = 30 * occ  # occ 0.40/0.60/0.80
receita_mensal = diaria * diarias_mes
receita_anual = receita_mensal * 12
```
Matematicamente correto.

**Verificação cenários:**
* 40% = 12,0 dias/mês (30*0.40) | 60% = 18,0 dias | 80% = 24,0 dias - correto.
* 60% como BASE: **razoável como hipótese central** (entre 40 e 80), mas o relatório corretamente o descreve como **PREMISSA** (`relatorio_roi.md:29`), não dado real. Não afirma ser ocupação real de Itapema (o que seria falso). **Defensável.**

Teste: 2q MP diária 460 *18 = 8.280/mes *12 = 99.360/ano - confere com `roi_perfil.csv:3` 8.280/99.360.

**Parecer:** **Aprovado.** Matemática correta, premissa explicitada.

---

## 4. Auditar comissão 15%

**Em `analisar_roi.py:98,117`:** `COMISSAO_PCT=0.15` + `comissao_anual = receita_anual * 0.15`

*Claramente identificada como PREMISSA?* Sim, em `relatorio_roi.md:30` "Comissão plataforma: 15% da receita bruta - **PREMISSA** (não existe na base, hipótese Airbnb/Seazone)" e `analisar_roi.py:98` comentário `PREMISSA plataforma`.

*Aplicada sobre receita bruta?* Sim, `receita_anual *0.15` - correto (não sobre lucro).

*Matematicamente correta?* Sim. Ex: 2q MP 60% receita 99.360*0.15=14.904 confere com `roi_perfil.csv:3` 14.904.

*Fonte?* **Não existe fonte nos arquivos** - `VivaReal` e `base_analitica` não têm coluna de comissão. Portanto a frase correta é: **"15% é uma premissa de modelagem, não um dado observado."** O relatório já diz isso, não inventa fonte.

**Avaliação das alternativas:**
* **A) Manter 15% como cenário-base:** Defensável se explicitado e com sensibilidade.
* **B) Retirar comissão do principal:** Esconderia custo real de plataforma, subestimaria e seria menos realista.
* **C) Só sensibilidade:** Sem base, não haveria número principal para comparar.

**Escolha mais defensável: A + C - manter 15% como base mas apresentar sensibilidade (10%/15%/20%) e ROI antes de comissão em apêndice.** O relatório atual faz A (mantém 15% explícito) mas **não apresenta sensibilidade de comissão** - é a principal lacuna. Recomendação: adicionar tabela `ROI com 0%,10%,15%,20%` para mostrar que ranking (2q Centro >2q MP >3q Centro) se mantém estável. Como não é erro matemático, é **ressalva metodológica**, não reprovação.

**Parecer:** **Aprovado com ressalva** - 15% está correto como premissa explícita, mas falta sensibilidade. Não é erro, é melhoria.

---

## 5. Auditar cleaning fee

*Origem:* `base_analitica_itapema.csv:cleaning_fee` (de `Details_Itapema.csv:cleaning_fee`), DADO OBSERVADO, cobertura 100% (0 nulos, `relatorio_auditoria:86` 939 zeros mas zeros são valor 0 válido).

*Mediana por perfil (recalculada):* 2q MP 250, 3q MP 300, 4q MP 350, 2q Centro 240, 3q Centro 280 - confere com `cost_check.py` (250/300/350/240/280) e com `analisar_roi.py:75` `median()`.

*Fórmula:* `cleaning_anual = cleaning_fee * (diarias_ano /5)` onde `diarias_ano = 30*occ*12`, `5 = AVG_STAY` - `analisar_roi.py:97,115-116` correto.

*5 dias é PREMISSA?* Sim, `AVG_STAY=5` comentado como PREMISSA e relatório `relatorio_roi.md:31` explicita `avg_stay=5`. Correto.

*Risco dupla contagem?* Não - `cleaning_fee` é custo por estadia (per reservation), `receita` é por diária, então `diarias_ano/5 = nº estadias/ano`. Ex: 2q MP 60% diarias_ano 216/5=43.2 estadias *250=10.800 - confere com `roi_perfil.csv` 10.800. Não há dupla contagem com diária (diária não inclui cleaning). **Matematicamente correto.**

**Parecer:** **Aprovado.** Origem, cobertura e fórmula corretas, premissa explicitada.

---

## 6. Auditar condomínio e IPTU

*Como obtidos:* `VivaReal_Itapema.csv:monthly_condo_fee` e `yearly_iptu` filtrados por perfil `apartamento & bedrooms & suburb_norm`, `pd.to_numeric(errors='coerce')`.

*Valores zero excluídos:* Sim, `analisar_roi.py:60-66` `condo_pos = condo_series[condo_series>0].dropna()` e `iptu_pos = iptu_series[iptu_series>0]` - correto, zeros são missing codificado, não condomínio grátis para apartamento. Relatório explicita `median >0, excluindo zeros/missing`.

*Cobertura por perfil (recalculada, >0):*
* 2q MP: condo 134/244 **55% pos** (180/244 74% total), iptu 115/244 47% pos
* 3q MP: 820/1704 **48% pos** (1210/1704 71% total), iptu 670/1704 39%
* 4q MP: 546/1327 **41% pos** (901/1327 68% total), iptu 436/1327 33%
* 2q Centro: 55/89 **62% pos** (73/89 82% total), iptu 50/89 56%
* 3q Centro: 179/438 **41% pos** (319/438 73% total), iptu 154/438 35%

Cobertura 41-62% pos (68-82% total) - **suficiente para mediana, mas 30-40% NA deve ser declarado**. Relatório faz (`relatorio_roi.md:12`).

*Mediana >0 defensável?* Sim, para apartamento, condo 0 é implausível (seria dado faltante). Usar mediana de >0 evita distorção. Para **3q Centro, mediana geral 1** (incluindo 140 zeros) vs **mediana >0 = 617** - o código corretamente usa 617 (`cost_check.py` 617), e relatório `relatorio_roi.md:15` explica: "Para 3q Centro, mediana geral 1 inclui zeros, por isso usamos mediana >0 (617)". **Problema já foi tratado, não distorce.**

**Parecer:** **Aprovado.** Tratamento correto e defensável, com ressalva de cobertura 40-60% que já é explicitada.

---

## 7. Auditar custos

*Reconstrução `analisar_roi.py:118` `custos_anuais = condo_anual + iptu_anual + cleaning_anual + comissao_anual`*

Exemplo 2q MP 60%: condo 500*12=6.000 + iptu 980 + cleaning 300*43.2=10.800? Wait 2q MP cleaning 250*43.2=10.800 (para 2q MP) + comissão 99.360*0.15=14.904 = 32.684 - confere com `roi_perfil.csv:3` 32.684.

Cada parcela confirmada separadamente acima. Nenhum custo sem dados foi acrescentado sem ser premissa (comissão e limpeza/5 são premissas explicitadas). Não há custos escondidos.

*Lista DADOS OBSERVADOS:* `sale_price` median, `price_mediano` median, `condo` median >0, `iptu` median >0, `cleaning_fee` median (todos com cobertura).

*Lista PREMISSAS:* `ocupacao 40/60/80`, `comissao 15%`, `avg_stay 5` para cleaning, `capital = sale_price` sem reforma/ITBI.

**Parecer:** **Aprovado.** Custos reconstruídos corretamente.

---

## 8. Auditar lucro

`lucro = receita_anual - custos_anuais` `analisar_roi.py:119` - correto.

Verificado 5 perfis ×3 cenários =15 linhas em `roi_perfil.csv`: todos lucros positivos (ex: 4q MP 40% lucro 107.190, menor ROI mas ainda positivo). Nenhum negativo, então payback é válido.

Exemplo 3q MP 60%: receita 151.200 - custos 44.340 (7.200+1.500+12.960+22.680) = 106.860 - confere.

**Parecer:** **Aprovado.**

---

## 9. Auditar ROI

`roi = lucro / preco_compra *100` `analisar_roi.py:120` - correto (anual simples, sem anualização extra pois lucro já é anual).

Sem erro de multiplicação/divisão/porcentagem: Ex 2q MP 60% lucro 66.676 /1.075.000*100=6.202% - `roi_perfil.csv:3` 6.202418... correto.

Preço usado corretamente: `preco_compra` mediano por perfil, não geral.

**Parecer:** **Aprovado.** Nenhum erro.

---

## 10. Auditar payback

`payback = preco_compra / lucro` `analisar_roi.py:121` com `if lucro>0 else nan` - correto, não apresenta payback positivo para lucro negativo (não há caso).

Ex 2q MP 60%: 1.075.000/66.676=16.122 - `roi_perfil.csv` 16.1227 correto.

**Parecer:** **Aprovado.**

---

## 11. Teste manual (60% BASE)

**2q Meia Praia (60%):**
* Preço: 1.075.000 (DADO Viva 244 apto 2q MP median)
* Diária: 460 (DADO base 723 apto 2q MP, 187 com preço, median price_mediano)
* Dias ocupados: 30*0.60=18/mês, 216/ano
* Receita: 460*18=8.280/mês, 8.280*12=99.360/ano
* Custos: condo 500*12=6.000 (OBS 55% pos) + IPTU 980 (OBS 47%) + cleaning 250*(216/5=43.2)=10.800 (OBS fee 250 + PREMISSA stay 5) + comissão 99.360*0.15=14.904 (PREMISSA 15%) = 32.684
* Lucro: 99.360-32.684=66.676
* ROI: 66.676/1.075.000*100=**6,20%**
* Payback: 1.075.000/66.676=**16,1a** - confere com `roi_perfil.csv:3`

**2q Centro (60%):**
* Preço: 1.150.000 | Diária: 580 (65 com preço de 183, 35,5% cov)
* Dias: 18 | Receita: 580*18=10.440/mês, 125.280/ano
* Custos: 500*12=6.000 +1.000 +240*43.2=10.368 +18.792=36.160
* Lucro: 125.280-36.160=89.120 | ROI 89.120/1.150.000=**7,75%** | Payback 12,9a - confere

**3q Meia Praia (60%):**
* Preço: 1.884.860 | Diária: 700 (327 com preço de 1451, 22,5%)
* Dias: 18 | Receita: 700*18=12.600/mês, 151.200/ano
* Custos: 600*12=7.200+1.500+300*43.2=12.960+22.680=44.340
* Lucro: 151.200-44.340=106.860 | ROI 106.860/1.884.860=**5,67%** | Payback 17,6a - confere

**Parecer:** **Aprovado.** Três testes manuais batem exatamente com `roi_perfil.csv`.

---

## 12. Teste de sensibilidade

*Ocupação:* Ranking se mantém? 40%: 2q Centro 4,96% >2q MP 3,92% >3q Centro 3,81% | 60%: 2q Centro 7,75% >2q MP 6,20% | 80%: 2q Centro 10,54% >2q MP 8,49% - **vencedor estável** (2q Centro) e **2q MP e 3q MP permanecem competitivos** (>3,6% mesmo em 40%). 4q MP cai de 6,35% (80%) para 2,98% (40%) - mais sensível por capital alto.

*Comissão:* Se 0% (sem comissão), lucros aumentam ~15% da receita: 2q MP 60% lucro iria de 66.676 para 81.580 (66.676+14.904) ROI 7,59% vs 6,20% (+1,39pp). Ranking **não muda** (2q Centro ainda lidera). Se 20%, ROI cai ~0,9pp, ranking mantém.

*Limpeza:* Se `avg_stay` 4 (mais limpezas: 216/4=54 vs 43,2) cleaning 250*54=13.500 vs 10.800 (+2.700) ROI 2q MP cairia de 6,20% para 5,95% (-0,25pp). Se 6 noites (36 limpezas) cleaning 9.000 ROI sobe para 6,37% (+0,17pp). **Impacto pequeno (<0,3pp), não muda vencedor.**

**Conclusão sensibilidade:** Pequenas mudanças (±5% comissão, ±1 dia stay, ±20% ocupação) **não alteram vencedor** (2q Centro >2q MP >3q Centro). O ranking é robusto.

---

## 13. Definir o que pode ser afirmado

**PODEMOS AFIRMAR COM SEGURANÇA (dado observado):**
* Preços medianos de compra por perfil são 1,07M (2q MP), 1,88M (3q MP), 3,6M (4q MP), 1,15M (2q Centro), 2,1M (3q Centro) com 100% cobertura Viva.
* Diárias medianas históricas são 460, 700, 1075, 580, 790 com cobertura 21-35% (60-327 anúncios).
* 2q Centro tem **maior ROI estimado no modelo** em todos os cenários (4,96%/7,75%/10,54%).
* 4q Meia Praia tem **maior lucro absoluto** (167.940 base) mas menor ROI % e amostra pequena.

**PODEMOS AFIRMAR COMO ESTIMATIVA (modelo com premissas):**
* 2q Centro possui **ROI estimado de 7,75% no cenário-base 60% (payback 12,9a)** - estimativa, não fato.
* 2q Meia Praia tem **ROI estimado 6,20% base** e permanece competitivo no conservador (3,92%).
* 3q Meia Praia tem **lucro estimado 106.860 base** com ROI 5,67% - forte potencial equilibrado como estimativa.

**NÃO PODEMOS AFIRMAR (sem dados):**
* "2q Centro é o melhor investimento garantido" - é **estimativa**, depende de ocupação real desconhecida, custos completos e amostra limitada.
* "Ocupação real em Itapema é 60%" - 60% é **hipótese**, não dado.
* "ROI será exatamente 6,20%" - é **projetado**, sensível a premissas, sem ITBI/reforma.
* Correspondência entre imóvel Viva específico e anúncio Airbnb específico.

---

## 14. Definir o vencedor

**Vencedor por ROI percentual (cenário BASE 60%):** **2q Centro - ROI 7,75%** (conservador 4,96%, otimista 10,54%, payback 12,9a, preço 1,15M, diária 580, lucro 89.120)

**Vencedor por menor capital:** **2q Meia Praia - R$1.075.000** (vs 1,15M 2q Centro, 1,88M 3q MP)

**Vencedor por equilíbrio (ROI + capital + volume + demanda + cobertura + lucro):** **2q Meia Praia** como **melhor oportunidade equilibrada** (ROI 6,20% base, capital menor 1,07M, volume 723 Airbnb/244 compra, alta 151 20,9%, 187 com preço) e **3q Meia Praia** como **forte alternativa com lucro absoluto maior** (ROI 5,67% base, lucro 106.860 vs 66.676, volume 1451/1704, alta 242). A distinção é intencional e correta no relatório.

*Não houve escolha antecipada - ranking calculado mostra 2q Centro lidera em ROI % em todos os cenários, mas tem volume 89 compra vs 244 (2q MP) e 1704 (3q MP), por isso o equilíbrio favorece Meia Praia.*

---

## 15. Revisar conclusão da Pergunta 1

**Versão revisada (curta, para relatório, sem prometer garantia):**

> **Considerando preço de aquisição (DADO), diária histórica (DADO) e cenários de ocupação/custos (PREMISSAS), o maior ROI estimado no modelo é 2q Centro (4,96%/7,75%/10,54% para 40/60/80%, payback 12,9a base, preço R$1.150.000, diária R$580, lucro R$89.120 base). A recomendação mais defensável pelo equilíbrio é 2q Meia Praia (ROI estimado 3,92%/6,20%/8,49%, preço R$1.075.000, diária R$460, lucro R$66.676 base, payback 16,1a) - menor capital, volume 723, alta 20,9% - com 3q Meia Praia (ROI 5,67% base, lucro R$106.860, volume 1451) como alternativa de lucro absoluto maior. 4q Meia Praia tem diária 1075 mas ROI 2,98-6,35% por capital 3,6M e amostra pequena (60 com preço). Estimativas, cenários hipotéticos, potencial projetado - não garantido, sem reforma/ITBI.**

Esta versão corrige a anterior que citava "ROI Centro 2q 6,14% base supera MP 2q" (valor desatualizado 6,14% vs atual 7,75%) e já está refletida no `relatorio_roi.md` atual após correções.

---

## 16. Relatório e correções

* **Nenhum erro matemático real encontrado** - todas as fórmulas refeitas batem com `roi_perfil.csv`.
* **Nenhum erro metodológico grave** - filtros, normalização, medianas >0, premissas explicitadas estão corretos.
* **Apenas ressalvas de premissas e amostra** (15% comissão, avg_stay 5, 60% ocupação, cobertura 21-35%, 4q amostra 60) - já explicitadas, não requerem `analisar_roi_v2.py` ou `roi_perfil_v2.csv`. **Não criar v2** é a decisão correta (instrução: só criar v2 se erro real).
* **Ranking não mudou** após auditoria (2q Centro >2q MP >3q Centro >3q MP >4q MP em todos os cenários) - estável.
* **Correções já aplicadas:** 3q Centro condo 617 (não 1) e lat/lon 0 consolidados - auditoria confirma que já foram tratadas.

---

## Caminho percorrido na auditoria

1. **Arquivos auditados:** `analisar_roi.py`, `relatorio_roi.md`, `roi_perfil.csv`, `relatorio_cruzamento_compra_aluguel.md`, `cruzamento_perfil.csv`, `relatorio_receita.md`, `VivaReal_Itapema.csv` (8329), `base_analitica_itapema.csv` (4441).
2. **Fórmulas verificadas:** `preco_compra=median(sale_price)`, `diaria=median(price_mediano)`, `receita_mensal=diaria*30*occ`, `receita_anual*12`, `custos=condo*12+iptu+cleaning_fee*(diarias_ano/5)+receita*0.15`, `lucro=receita-custos`, `ROI=lucro/preco*100`, `payback=preco/lucro`.
3. **Dados observados:** `sale_price` median, `price_mediano` median, `condo/iptu` median >0, `cleaning_fee` median, `qtd` contagens (com cobertura).
4. **Premissas:** `ocupacao 40/60/80`, `comissao 15%`, `avg_stay 5`, `capital=sale_price` sem ITBI/reforma.
5. **Cálculos refeitos:** 15 cenários (5 perfis×3 occ) recalculados manualmente para 2q MP, 2q Centro, 3q MP e comparados com `roi_perfil.csv` - 100% match.
6. **Problemas encontrados:** Nenhum erro matemático; apenas premissas discutíveis (15% e 5 dias) e amostras pequenas (4q MP 60, 3q Centro 45 com preço) já sinalizadas.
7. **Problemas não encontrados:** Preço/diária filtros corretos, mediana adequada, receita correta, custos corretos, lucro/ROI/payback sem erro de anualização ou divisão.
8. **Correção:** Nenhuma correção de cálculo necessária; apenas atualização de texto de 6,14% para 7,75% já feita - não requer v2.
9. **Ranking mudou?** Não, permanece 2q Centro >2q MP >3q Centro >3q MP >4q MP em todos os cenários.
10. **Conclusão defensável:** **2q Centro maior ROI estimado (7,75% base)**, **2q Meia Praia melhor equilíbrio (6,20% base, capital 1,07M, volume 723, alta 20,9%)**, **3q Meia Praia forte alternativa (5,67% base, lucro 106k, volume 1451)** - pode ser defendida com ressalvas.

---

## Resposta final no terminal

```
AUDITORIA ROI
Status: [APROVADO COM RESSALVAS]
```
* **Houve erro matemático?** Não. 15 cenários recalculados manualmente batem com `roi_perfil.csv` (ex: 2q MP 60% 460*18*12=99.360, custos 32.684, lucro 66.676, ROI 6,20%).
* **Houve erro metodológico?** Não grave. Filtros, normalização `strip().lower()`, medianas >0, premissas explicitadas estão defensáveis. Apenas ressalva: `cruzamento_perfil.csv` ainda tem `condo 1` para 3q Centro (antigo), mas `ROI` já corrige para 617.
* **Alguma premissa precisa ser alterada?** Não alterar, mas **adicionar sensibilidade** para 15% (0%/10%/20%) e `avg_stay` 4/6 dias no apêndice - ranking se mantém, então manter 15% e 5 dias como base é defensável com ressalva.
* **Ranking mudou?** Não. 2q Centro >2q MP >3q Centro >3q MP >4q MP em 40/60/80%.
* **Quem possui maior ROI?** **2q Centro: 4,96% (40%), 7,75% (60% BASE), 10,54% (80%)**, payback 20,1/12,9/9,5a.
* **Quem é recomendação equilibrada?** **2q Meia Praia (6,20% base, 1,07M, 723, alta 20,9%)** e **3q Meia Praia (5,67% base, 1,88M, 1451, alta 242)** como forte alternativa de lucro absoluto.
* **Podemos usar na Pergunta 1?** **Sim, com ressalvas** - como **ROI estimado em cenário-base 60%**, com premissas 15%/5 dias/40-80% e limitações de amostra (4q MP 60 com preço, 3q Centro 45) declaradas. Não como fato garantido.
* **Arquivos gerados:** `analysis/auditoria_roi.md` (este), `analysis/relatorio_roi.md` mantido, `analysis/roi_perfil.csv` validado, `data/` não alterado (timestamps 10:58:39).
