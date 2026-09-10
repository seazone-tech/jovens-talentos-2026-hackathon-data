# Relatorio Caracteristicas que Explicam as Melhores Receitas - Pergunta 3

> **Sem causalidade, apenas associacao** | **DADO OBSERVADO vs RESULTADO CALCULADO vs PREMISSA** separados | Reaproveita `base_analitica`, `VivaReal`, `roi`, `cruzamento`, `localizacao` sem recalcular ROI | `data/` intacto

## A. Quartos x receita (2q/3q/4q Meia Praia e Centro)

| Perfil | Qtd Airbnb | Com preco | Diaria med | Receita 60% ano | Preco compra med | Area med | Volume/demanda | Receita vs preco |
|---|---|---|---|---|---|---|---|---|
| 2q Meia Praia | 723 | 187 (26%) | R$ 460 | R$ 99,360 | R$ 1,075,000 | 85m2 | alta 723 total, 187 com preco |
| 3q Meia Praia | 1451 | 327 (23%) | R$ 700 | R$ 151,200 | R$ 1,884,860 | 129m2 | alta 1451 total, 327 com preco |
| 4q Meia Praia | 286 | 60 (21%) | R$ 1075 | R$ 232,200 | R$ 3,600,000 | 188m2 | alta 286 total, 60 com preco |
| 2q Centro | 183 | 65 (36%) | R$ 580 | R$ 125,280 | R$ 1,150,000 | 86m2 | alta 183 total, 65 com preco |
| 3q Centro | 211 | 45 (21%) | R$ 790 | R$ 170,640 | R$ 2,100,000 | 131m2 | alta 211 total, 45 com preco |

> **Quartos → receita:** 2q 99k/125k < 3q 151k/170k < 4q 232k (RESULTADO). Mais quartos está **associado** a maior receita (forte), mas preco compra sobe +75% (2q→3q) e +91% (3q→4q) mais que diaria (+52%,+53%), então **mais quartos não é proporcionalmente melhor economicamente** (sem ROI, apenas receita).

## B. Localizacao x receita

| Bairro | Qtd Airbnb | Com preco | Diaria med | Receita 60% ano | Qtd venda apto | Preco compra med | Combinacao |
|---|---|---|---|---|---|---|---|
| Meia Praia | 2602 | 607 | R$ 600 | R$ 129,600 | 3414 | R$ 2,306,900 | 2602 vs 3414 |
| Centro | 548 | 193 | R$ 587 | R$ 126,720 | 985 | R$ 2,600,000 | 548 vs 985 |
| Morretes | 318 | 68 | R$ 500 | R$ 108,000 | 1307 | R$ 797,000 | 318 vs 1307 |

> **Localizacao:** Meia Praia 129,6k (600, 2602) > Centro 126,7k (587, 548) > Morretes 108k (500, 318). **Associação moderada:** Meia Praia combina **volume 4,7× Centro** com diaria similar, mas diferença receita bairro isolado é só 2,3% (2.880/ano) - empate técnico com leve vantagem. Bairros <30 com preco (Tabuleiro 17, Casa Branca 13) excluídos.

## C. Area util x diaria/receita

| Faixa area | Qtd Viva apto | Area med | Preco med | Preco/m2 med | Diaria proxy (quartos) | Receita proxy 60% ano |
|---|---|---|---|---|---|---|
| 0-70m² | 1684 | 68 | R$ 790,000 | R$ 11,873 | 1q 434 (studio) |  |
| 70-100m² | 600 | 89 | R$ 1,150,000 | R$ 12,524 | 2q 460-580 | 99k |
| 100-130m² | 1707 | 120 | R$ 1,700,000 | R$ 14,569 | 3q 700-790 | 151k |
| 130-180m² | 1892 | 150 | R$ 2,400,000 | R$ 15,789 | 3q-4q 700-1075 | 151k |
| >180m² | 1645 | 212 | R$ 4,052,000 | R$ 18,341 | 4q 1075+ | 232k |

> **Area → diaria/receita:** Correlação área-diaria nos 5 perfis **r=0.98 (forte)** - area 85m²→460, 129→700, 188→1075. Imóveis maiores têm diária e receita maiores. Faixas até 70m² (studio/1q) têm preço 650k, 70-100 (2q) 1,07M, 100-130 (3q) 1,69M, 130-180 (3q) 2,1M, >180 (4q) 3,6M. Area explica receita, mas preço/m² também sobe (10,7k→18,5k).

## D. Preco compra x receita

| Perfil | Preco compra med | Preco/m2 | Diaria med | Receita 60% ano | Receita vs preco |
|---|---|---|---|---|---|
| 2q Meia Praia | R$ 1,075,000 | R$ 12,929 | R$ 460 | R$ 99,360 | 9.24% receita/preço |
| 3q Meia Praia | R$ 1,884,860 | R$ 14,957 | R$ 700 | R$ 151,200 | 8.02% receita/preço |
| 4q Meia Praia | R$ 3,600,000 | R$ 18,519 | R$ 1075 | R$ 232,200 | 6.45% receita/preço |
| 2q Centro | R$ 1,150,000 | R$ 13,068 | R$ 580 | R$ 125,280 | 10.89% receita/preço |
| 3q Centro | R$ 2,100,000 | R$ 15,789 | R$ 790 | R$ 170,640 | 8.13% receita/preço |

> **Preço compra → receita:** Correlação positiva, mas **não proporcional**. Ponto de retorno decrescente: 2q→3q MP preço +75% (1,07M→1,88M) gera receita +52% (99k→151k); 3q→4q preço +91% (1,88M→3,6M) gera receita +53% (151k→232k). **Preço/m² mais alto (18,5k 4q vs 12,9k 2q) não garante melhor perfil econômico**, apenas maior receita bruta.

## E. Demanda/reviews x receita

| Grupo | Qtd | Com preco | Diaria med | Receita 60% ano | Quartos med | Bairro top | Preco compra med |
|---|---|---|---|---|---|---|---|
| Alta (≥15) | 625 | 504 | R$ 550 | R$ 118,800 | 3q | Meia Praia | 1,88M (3q MP) |
| Demais | 3085 | 407 | R$ 600 | R$ 129,600 | 3q | Meia Praia | 1,07M (2q MP) |
| Todos | 3710 | 911 | R$ 585 | R$ 126,360 | 3q | Meia Praia | 1,07M (2q MP) |

> **Demanda (reviews) → receita:** Alta (≥15, 625, 80,6% com preço) tem **diária mediana 550 vs demais 600 (alta cobra 50 a menos)** e **receita 60% 118.800 vs demais 129.600 (alta menor)** - **reviews alta não está associada a maior diária/receita**, mas a **maior probabilidade de ter histórico (80,6% vs 13,2%) e a características como Guest Favorite 67,7% vs 10,7%**. **Não tratar reviews como ocupação.**

## F. Caracteristicas combinadas (mais importante)

| Perfil | Local | Quartos | Area | Diaria | Preco compra | Preco/m2 | Qtd Airbnb | Receita 60% ano | Alta |
|---|---|---|---|---|---|---|---|---|---|
| 4q Meia Praia | Meia Praia | 4q | 188m2 | R$ 1075 | R$ 3,600,000 | R$ 18,519 | 286 (60) | R$ 232,200 | 286 total |
| 3q Centro | Centro | 3q | 131m2 | R$ 790 | R$ 2,100,000 | R$ 15,789 | 211 (45) | R$ 170,640 | 211 total |
| 3q Meia Praia | Meia Praia | 3q | 129m2 | R$ 700 | R$ 1,884,860 | R$ 14,957 | 1451 (327) | R$ 151,200 | 1451 total |
| 2q Centro | Centro | 2q | 86m2 | R$ 580 | R$ 1,150,000 | R$ 13,068 | 183 (65) | R$ 125,280 | 183 total |
| 2q Meia Praia | Meia Praia | 2q | 85m2 | R$ 460 | R$ 1,075,000 | R$ 12,929 | 723 (187) | R$ 99,360 | 723 total |

> **Padrão repetido:** **Meia Praia + 3q + 129m² + diária 700 + volume 1451/1704 + preço 1,88M** aparece como **melhor combinação volume-receita-preço** (receita 151k, 327 com preço, alta 242). **2q MP (460, 99k, 85m², 1,07M, 723)** é similar com ticket menor. **4q MP (1075, 232k, 188m², 3,6M, 286, 60 com preço)** tem receita maior mas volume 5× menor e alta 33 (11,5%) - nicho.

## Tabela comparativa final

| Característica | Perfil/resultado | Evidência (números) | Tipo | Força |
|---|---|---|---|---|
| Número de quartos | 3q (700, 151k) equilibra; 4q (1075, 232k) maior receita mas volume 286 | DADO OBSERVADO: 2q diaria 460-580 (723/183 airbnb), 3q 700-790 (1451/211), 4q 10... | forte | forte evidência de associação |
| Bairro/localização | Meia Praia 129,6k (600, 2602) > Centro 126,7k (587, 548) +2,3%, volume 4,7× | DADO OBSERVADO: Meia Praia 600 (2602, 607 com preço) vs Centro 587 (548, 193) vs... | associação | associação moderada |
| Área útil | 85m²→460, 129→700, 188→1075, r=0,98 | DADO OBSERVADO Viva: faixas até70 (mediana área 60, preco 650k), 70-100 (85, 1,0... | forte | forte evidência de associação |
| Preço de compra | 1,07M→99k, 1,88M→151k (+75% preço, +52% receita), 3,6M→232k (+91% preço, +53% receita) | DADO OBSERVADO: 2q MP 1,07M (diária 460, receita 99k), 3q MP 1,88M (700, 151k), ... | associação | associação moderada |
| Diária histórica | 460→99k, 700→151k, 1075→232k, correlação 1,0 (fórmula) | DADO OBSERVADO: price_mediano mediana por segmento (460,700,1075,580,790). RESUL... | forte | forte evidência de associação |
| Demanda (reviews ≥15) | Alta 550/118k vs demais 600/129k, alta não tem diária maior | DADO OBSERVADO: alta 625 (16,8% dos aptos) com 504 com preço (80,6%) vs demais 3... | associação | associação moderada |
| Condomínio | 500-942, sem padrão claro com receita | DADO OBSERVADO: 2q MP 500 (55% pos), 3q MP 600 (48%), 4q MP 942 (41%), 2q Centro... | evidência | evidência insuficiente |
| IPTU | 980-3000, sobe com quartos, não explica isolado | DADO OBSERVADO: 2q MP 980 (47% pos), 3q MP 1500 (39%), 4q MP 3000 (33%), 2q Cent... | evidência | evidência insuficiente |
| Preço por m² | 12,9k→14,9k→18,5k com receita, mas ROI menor | RESULTADO CALCULADO: sale_price/usable_area median >0: 2q MP 12.929, 3q MP 14.95... | associação | associação moderada |
| Combinação localização+quartos+área | Meia Praia 3q 129m² 700 1,88M 1451 | Padrão repetido: Meia Praia + 2-3q + 85-129m² + diária 460-700 + volume 723-1451... | forte | forte evidência de associação |

### Classificação por força da evidência


**Forte Evidência De Associação:**
- **Número de quartos:** DADO OBSERVADO: 2q diaria 460-580 (723/183 airbnb), 3q 700-790 (1451/211), 4q 1075 (286, 60 com preço). RESULTADO: recei... *Limitação: 4q amostra pequena (60 com preço, 21% de 286) vs 3q robusto (327/1451). Quartos *
- **Área útil:** DADO OBSERVADO Viva: faixas até70 (mediana área 60, preco 650k), 70-100 (85, 1,07M), 100-130 (118, 1,69M), 130-180 (145,... *Limitação: Base Airbnb não tem usable_area (usamos Viva como proxy por perfil); faixas até7*
- **Diária histórica:** DADO OBSERVADO: price_mediano mediana por segmento (460,700,1075,580,790). RESULTADO: receita 60% = diária×216 (ex: 700×... *Limitação: Diária é histórica por anúncio (999/3710 com preço, 21-35% cobertura), não garan*
- **Combinação localização+quartos+área:** Padrão repetido: Meia Praia + 2-3q + 85-129m² + diária 460-700 + volume 723-1451 + preço 1,07-1,88M aparece como mais eq... *Limitação: Análise por segmento, não por imóvel; sem causalidade, apenas associação.*

**Associação Moderada:**
- **Bairro/localização:** DADO OBSERVADO: Meia Praia 600 (2602, 607 com preço) vs Centro 587 (548, 193) vs Morretes 500 (318, 68). RESULTADO: rece... *Limitação: Bairros com <30 com preço (Tabuleiro 17, Casa Branca 13) excluídos corretamente;*
- **Preço de compra:** DADO OBSERVADO: 2q MP 1,07M (diária 460, receita 99k), 3q MP 1,88M (700, 151k), 4q MP 3,6M (1075, 232k). RESULTADO: preç... *Limitação: Viva e Base são por segmento, não por imóvel (sem correspondência individual).*
- **Demanda (reviews ≥15):** DADO OBSERVADO: alta 625 (16,8% dos aptos) com 504 com preço (80,6%) vs demais 3085 com 407 (13,2%). Alta tem diária med... *Limitação: reviews é proxy acumulado, não ocupação; depende de tempo de anúncio; 40% dos de*
- **Preço por m²:** RESULTADO CALCULADO: sale_price/usable_area median >0: 2q MP 12.929, 3q MP 14.957 (+15%), 4q MP 18.519 (+24% vs 3q), 2q ... *Limitação: Calculado apenas onde 0<area<10000 (exclui 11 zeros e 188000), cobertura 70% are*

**Evidência Insuficiente:**
- **Condomínio:** DADO OBSERVADO: 2q MP 500 (55% pos), 3q MP 600 (48%), 4q MP 942 (41%), 2q Centro 500 (62%), 3q Centro 617 (41% pos, 73% ... *Limitação: Cobertura 41-62% pos, 30% NA total, 3q Centro median geral 1 inclui zeros (corri*
- **IPTU:** DADO OBSERVADO: 2q MP 980 (47% pos), 3q MP 1500 (39%), 4q MP 3000 (33%), 2q Centro 1000 (56%), 3q Centro 1300 (35%). IPT... *Limitação: Cobertura 33-56% pos, muitos NA, valores baixos vs preço compra.*

## Hipótese: maior receita vs melhor perfil econômico

**Maior receita (RESULTADO):** 4q Meia Praia **R$232.200/ano a 60%** (1075×216) é a maior receita bruta estimada entre os 5 perfis, mas exige **R$3,6M (+91% vs 3q)** e tem **286 Airbnb (60 com preço, 21%)** vs 1451 de 3q MP.

**Melhor perfil econômico (sem ROI, apenas receita+preço+volume):** **3q Meia Praia (R$151.200, 1,88M, 129m², 1451, 327 com preço, alta 242)** e **2q Meia Praia (R$99.360, 1,07M, 85m², 723, 187)** têm **melhor equilíbrio**: diária alta sem exigir preço tão alto (preço/m² 14,9k vs 18,5k do 4q), volume 5-7× maior, receita 65-87% da maior com 52-29% do capital. **O objetivo da Pergunta 3 é explicar o que está por trás das melhores receitas, não escolher vencedor da Pergunta 1 (ROI).** Por isso, 4q tem maior receita, mas 3q/2q têm melhor perfil econômico em termos de receita por capital e volume.

## Controle de qualidade

1. Números conferidos com `relatorio_receita.md:11`, `cruzamento_perfil.csv:6`, `localizacao_receita.csv:46` - medianas recalculadas batem (460,700,1075,580,790).
2. Medianas calculadas com `median()` (robusta a outlier R$29.000), não média.
3. Valores nulos: `price_mediano` NA mantido (3442 sem preço na base, 21-35% por perfil), `usable_area` 0 e 188000 excluídos de área/m2, `monthly_condo_fee` NA mantido.
4. Amostras pequenas sinalizadas: 4q MP 60 com preço (21% de 286), 3q Centro 45 (21% de 211), Tabuleiro 17, Casa Branca 13 - não deixam vencer por diária alta.
5. Preço compra (Viva) não confundido com receita (Airbnb) - tabelas separadas, sem JOIN por imóvel.
6. Diária (DADO OBSERVADO) não confundida com receita (RESULTADO `*30*occ`)
7. Ocupação 60% é PREMISSA (18 dias), não dado observado - explicitado.
8. Reviews como proxy, não ocupação - alta 550 vs demais 600 mostra que alta não tem diária maior.
9. Sem correspondência Viva vs Airbnb por imóvel, apenas por segmento `bairro×quartos`.
10. `data/` não alterado (verificado).

## Conclusão - Quais características explicam as melhores receitas? (3-5 principais, ordenadas)

**1. Número de quartos (FORTE):** O que os dados mostram: 2q 460→99k, 3q 700→151k (+52% receita), 4q 1075→232k (+53%). Números: 2q 723/244 venda, 3q 1451/1704, 4q 286/1327. Tipo: DADO OBSERVADO (quartos) + RESULTADO (receita). Limitação: 4q amostra pequena (60 com preço), mais quartos = mais área e preço (1,07M→3,6M).

**2. Área útil (FORTE):** O que mostram: faixas até70 650k/60m² → 70-100 1,07M/85m² → 100-130 1,69M/118m² →130-180 2,1M/145m² → >180 3,6M/210m²; diária 460→700→1075 com área 85→129→188 (r=0,98). Tipo: DADO OBSERVADO (Viva area) + RESULTADO. Limitação: Base Airbnb não tem area, usamos Viva como proxy por perfil.

**3. Diária histórica (FORTE):** O que mostram: diária é driver direto da receita por fórmula (700×216=151k). Números: 460→99k, 580→125k, 700→151k, 790→170k, 1075→232k. Tipo: DADO OBSERVADO (price_mediano) + RESULTADO. Limitação: diária é histórica (999/3710), não garantia, e depende de volume.

**4. Localização Meia Praia + volume (MODERADA):** O que mostram: Meia Praia 129,6k/ano (600, 2602) vs Centro 126,7k (587, 548) - diferença pequena 2,3% mas volume 4,7× maior; 3q MP 151k com volume 1451 vs 3q Centro 170k com 211. Tipo: DADO OBSERVADO. Limitação: bairros <30 com preço excluídos, Centro até tem diária maior para 2q (580>460).

**5. Preço de compra com retorno decrescente (MODERADA):** O que mostram: preço 1,07M→1,88M (+75%) gera receita +52%, 1,88M→3,6M (+91%) gera +53%; preço/m² 12,9k→14,9k→18,5k sobe mais rápido que receita. Tipo: DADO OBSERVADO + RESULTADO. Limitação: sem correspondência imóvel-a-imóvel, segmento apenas.

**Conclusão executiva curta (pronta para README/vídeo, sem recomendação final de investimento):**

* **Mais quartos e maior área estão fortemente associados a maiores receitas** (2q 99k → 3q 151k → 4q 232k a 60%, com área 85→129→188m², r≈0,98), mas com **retorno decrescente vs preço** (75% mais capital para 52% mais receita).
* **Meia Praia combina volume (2602) com diária (600) e receita (129,6k)** ligeiramente acima de Centro (126,7k), mas a diferença é pequena (2,3%) - **3q Meia Praia (700, 151k, 1451, 1,88M) é o equilíbrio mais robusto**, 4q tem maior receita (232k) mas volume 5× menor e alta 11,5%.
* **Diária é o driver direto da receita** (700×216=151k), mas **alta demanda (reviews≥15) não significa diária maior** (alta 550 vs demais 600) - demanda indica liquidez (80,6% com preço vs 13,2%), não preço.
* **Condomínio/IPTU e preço/m² têm evidência insuficiente isoladamente** para explicar receita; preço/m² alto (18,5k 4q vs 12,9k 2q) acompanha receita maior, mas não garante melhor perfil econômico.

## Caminho percorrido

1. **Arquivos usados:** `base_analitica_itapema.csv` (4441), `VivaReal_Itapema.csv` (8329), `roi_perfil.csv` (15), `cruzamento_perfil.csv` (5), `localizacao_receita.csv` (45), `resposta_pergunta1.md`, `auditoria_pergunta2.md`, `relatorio_demanda.md` (625 alta), `relatorio_receita.md` (460/700/1075), `relatorio_cruzamento_compra_aluguel.md` (1704 3q MP), `relatorio_roi.md` (custos, sem recalcular ROI).
2. **Colunas usadas:** Base `number_of_bedrooms, suburb, price_mediano/min/max, number_of_reviews, listing_type`, Viva `bedrooms, suburb, sale_price, usable_area, monthly_condo_fee, yearly_iptu, listing_type`.
3. **Filtros aplicados:** `apartamento` (3710 Base, 7529 Viva), `bedrooms==q` (2/3/4), `suburb_norm` (lower), `price_mediano.notna()` para com preço, `0<usable_area<10000` para área, `reviews>=15` para alta, `qtd>=15` para segmentos.
4. **Cálculos feitos:** `median(price_mediano)` por perfil/bairro/faixa, `receita=price_mediano*30*0.60*12` (60% PREMISSA), `count`, `median(sale_price)`, `median(area)`, `sale_price/area` median, `quantile` para faixas, `corr(area,diaria)` nos 5 perfis.
5. **Comparações realizadas:** A: quartos (2/3/4) em Meia Praia/Centro, B: bairros (Meia Praia/Centro/Morretes), C: faixas area 0-70/70-100/100-130/130-180/>180, D: preço compra vs receita e preço/m2, E: alta vs demais (550 vs 600), F: combinadas `3q Meia Praia 129m² 700 1,88M 1451` vs `4q 188m² 1075 3,6M 286`.
6. **Hipóteses testadas:** mais quartos→maior receita? (sim, forte), Meia Praia volume+diaria? (sim, moderada), área→diaria? (sim, r=0,98), preço maior→receita proporcional? (não, decrescente), alta demanda→diaria maior? (não), 4q maior receita vs melhor econômico? (receita maior sim, econômico não por capital).
7. **Padrões encontrados:** Forte: quartos, área (r=0,98), diária; Moderada: Meia Praia volume, preço compra com decrescente, preço/m²; Insuficiente: condo/IPTU. Perfil repetido: **3q Meia Praia 129m² 700 1,88M 1451** e **2q Meia Praia 85m² 460 1,07M 723**.
8. **Limitações:** 4q MP 60 com preço (21% de 286) vs 3q 327/1451, bairros <30 com preço excluídos, Base sem area (proxy Viva), reviews proxy não ocupação, 999/3710 com preço, preco/m2 só onde area válida, `data/` intacto.
9. **Conclusão Pergunta 3:** Ordenada por força: 1) quartos, 2) área, 3) diária, 4) Meia Praia volume, 5) preço com decrescente - sem causalidade, apenas associação, sem recomendação final.
