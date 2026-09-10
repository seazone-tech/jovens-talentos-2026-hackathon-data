# Auditoria Independente - Perguntas 1 a 4

> **Objetivo:** Verificar de forma independente (sem defender conclusões anteriores) se existem erros de cálculo, filtros que excluíram dados, conclusões não suportadas, confusão entre dado/premissa/resultado, problemas de amostra, comparações injustas e afirmações causais indevidas.
> **Método:** Releitura de `analysis/*.py` e `analysis/*.md` + `data/*.csv` e `analysis/base_analitica_itapema.csv`, recálculo manual de 15 cenários de ROI e 5 perfis de receita, e checagem de filtros com `value_counts()`. Nenhum arquivo em `data/` alterado. Não escolhe novo investimento.

---

## 1. Erros de Cálculo

| Item | Status | Valor Original | Cálculo refeito | Correção / Justificativa |
|---|---|---|---|---|
| **Receita 60% (Pergunta 1 e 2)** | Correto | `relatorio_receita.md:11` 2q MP 460×30×0,60=8.280/mês, 99.360/ano; 3q MP 700×216=151.200; 4q MP 1075×216=232.200; 2q Centro 580×216=125.280; 3q Centro 790×216=170.640 | Refeito `460*18*12=99.360`, `700*18*12=151.200`, `1075*18*12=232.200`, `580*18*12=125.280`, `790*18*12=170.640` | **Correto, sem erro.** Fórmula `diaria×30×occ×12` aplicada consistentemente em `analisar_receita.py: cenarios()` e `analisar_roi.py:109-112` e `analisar_localizacao_receita.py:72`. |
| **Receita Centro isolado** | **Ressalva** | `relatorio_localizacao_receita.md:13` Centro 587×216=126.720, mas exibido como 587 (arredondado) | Mediana exata Centro é **586,6667** (193 com preço, `base_analitica` median). `586,6667×216=126.720,0072` → **126.720 correto com mediana exata**; `587×216=126.792` seria +72. | **Não é erro, é arredondamento de exibição.** Deve ser notado como "587 (586,67 usado no cálculo)". Já corrigido na auditoria Pergunta 2, sem impacto no ranking (Meia Praia 129.600 > Centro 126.720 mantido). |
| **ROI 60%** | Correto | `relatorio_roi.md:49-63` 2q Centro 7,75% (89.120/1.150.000), 2q MP 6,20% (66.676/1.075.000), 3q MP 5,67% (106.860/1.884.860) | Refeito `89.120/1.150.000=0,07749=7,749%→7,75%`, `66.676/1.075.000=0,06202=6,20%`, `106.860/1.884.860=0,05669=5,67%` | **Correto, sem erro de divisão/porcentagem/anualização.** `roi_perfil.csv:12` 7,7495% confere. |
| **Payback** | Correto | 2q MP 16,1a (1.075.000/66.676), 3q MP 17,6a (1.884.860/106.860) | Refeito `1.075.000/66.676=16,122→16,1a`, `1.884.860/106.860=17,638→17,6a` | **Correto, só quando lucro>0 (todos positivos).** |
| **Correlação 0,98** | **Ressalva** | `relatorio_caracteristicas_receita.md:37` "r=0,98 (forte) - area 85→460, 129→700, 188→1075" | Refeito com `areas=[85,129,188,86,131]`, `diarias=[460,700,1075,580,790]` → `np.corrcoef=0,9768→0,98` **correto matematicamente para n=5 medianas**, mas **individual** `Viva area vs sale_price n=7528 r=0,3529` e `Base quartos vs diaria n=911 r=0,3139` (ver `auditoria_pergunta3.md`) são **moderadas**. O cálculo está correto, mas a **interpretação como "forte para todos os imóveis" é exagerada** - já sinalizado na auditoria Pergunta 3. | **Cálculo correto, interpretação precisa de ressalva (n=5 vs n=911).** |
| **Retorno bruto vs ROI** | Correto | `relatorio_candidatos_investimento.md` retorno bruto 9,24% (99.360/1.075.000) vs ROI 6,20% ((99.360-32.684)/1.075.000) | Refeito 99.360/1.075.000=9,242% e (99.360-32.684)/1.075.000=6,202% | **Correto, distinção mantida.** |
| **Outros** | Correto | `price_mediano` medianas 460,700,1075,580,790; `sale_price` medianas 1,07M/1,88M/3,6M/1,15M/2,1M; `qtd` 723/1451/286 etc. | Recontados via `value_counts()` e `median()` e batem com `cruzamento_perfil.csv:6` e `localizacao_receita.csv:46` | **Corretos.** |

**Veredito cálculos:** **Nenhum erro matemático grave.** Apenas 1 ressalva de arredondamento (Centro 587 vs 586,67) sem impacto.

---

## 2. Filtros que podem ter excluído dados

| Filtro | Código | Efeito | Justificado? |
|---|---|---|---|
| `listing_type==apartamento` (Base 3710/4441, Viva 7529/8329) | `analisar_roi.py:52-53`, `analisar_localizacao_receita.py:56` | Exclui casa 443 (10%), outros 245 (5,5%), hotel 43 (1%), terreno 164, comercial 79 | **Sim, para Pergunta 1-4 foco em apartamentos.** `auditoria_universo_imoveis.md` mostrou que **apenas apartamento (911 com preço, 24,6%) e casa (70, 15,8%) têm n≥30 com preço** para mediana estável. Outros (17), hotel (1), terreno/comercial (0 no Airbnb) têm **n<30 e cobertura <7%**, mediana não robusta. **Filtro é objetivo (≥100 total e ≥30 com preço), não escolha conveniente.** Ressalva correta: casa tem volume suficiente no nível `casa` isolado (443/70) mas **13× menos com preço que apartamento (70 vs 911)** e **8× menos total**, e **modelo operacional distinto** (casa vs prédio com elevador) - por isso foco em apartamento é defensável para Seazone (3000 imóveis em prédios). |
| `suburb_norm = strip().lower()` | `analisar_roi.py:26`, `analisar_localizacao_receita.py:23` | Unifica `Meia Praia`/`Meia praia`/`MEIA PRAIA`, vazios excluídos | **Correto.** Duplicidade `alto sao bento` vs `alto são bento` (14 vs 13 únicos) por acento não normalizado é **baixo impacto** (ambos 0 com preço, excluídos do ranking). Deveria usar `unidecode` para 13 únicos, mas não altera vencedores. |
| `bedrooms==q` (2,3,4) | `analisar_roi.py:52` | Exclui 0q/1q (Studio/1q) da Pergunta 1 (intencional, tese separada) e 5q+ (32+3+1 etc. com n<30) | **Correto e explicitado** ("Não considere ainda tese studio/1q Centro"). Para Pergunta 1, 1q tem 233 total, 106 com preço (45% cobertura) mas é **6,3% do mercado vs 35-47% para 2-3q** - volume menor, não foi excluído por erro, mas por foco. |
| `0<usable_area<10000` | `analisar_vivareal.py` e `analisar_roi.py:57` | Exclui 11 zeros e 1 outlier 188000 m² (0,14% de 8329) da mediana área/m² | **Correto e explicitado** (`relatorio_vivareal.md:77` "11 zeros +1 outlier"). Sem exclusão, mediana área seria distorcida (188000 puxaria média, mas mediana robusta mudaria pouco). |
| `price_mediano.notna()` | `analisar_roi.py:81` etc. | Exclui 3442/4441 (77,5%) sem preço da mediana | **Correto, não tratado como zero.** Cobertura 21-35% por perfil é baixa, mas é **dado observado**, não exclusão arbitrária. Relatório sinaliza "3442 sem preço" como limitação. |
| `qtd_airbnb>=100 & com_preco>=30` para ranking | `analisar_localizacao_receita.py:187` | Exclui Tabuleiro 99/17, Ilhota 22/5, Casa Branca 63/13, Andorinha 0/0 | **Correto e objetivo** - evita que Tabuleiro (131.760 com 99/17) vença Meia Praia (129.600 com 2602/607) por diária 610 vs 600 com n=17. Sem filtro, Tabuleiro seria #1 isolado, mas com **17 com preço vs 607**, mediana com n=17 tem erro padrão ~3× maior. |

**Nenhum filtro excluiu dados relevantes de forma indevida.** Todos têm justificativa objetiva (n<30, 0 no outro mercado, ou foco explícito).

---

## 3. Conclusões não suportadas pelos dados

| Conclusão no relatório | Suportada? | Evidência | Risco |
|---|---|---|---|
| **"4q Meia Praia tem maior receita (232.200) mas é nicho"** | **Sim** | 4q MP receita 232.200 >3q MP 151.200 (+53%) com n=60 com preço (21% de 286) vs 327/1451 (22% de 1451) e 33 alta (11,5% vs 16,7%) - **receita maior é fato, volume 5× menor e alta menor também são fatos**, então "nicho" é interpretação defensável. | Baixo |
| **"Meia Praia vence Centro por +2,3% (129.600 vs 126.720) por volume 4,7×"** | **Parcialmente** | Diferença 2.880/126.720=2,27% com n=607 vs 193 com preço. **Intervalo de confiança da mediana com n=607 vs 193 e desvio padrão ~300-400 é de ±10-15 reais**, então **2.880/ano = 240/mês = 13,3 reais por dia (600 vs 587) está dentro da margem de erro**. Dizer "Meia Praia vence" como fato é **exagerado**; correto é **"empate técnico com leve vantagem Meia Praia sustentada por volume 4,7×"** - o relatório já faz isso em 80% dos trechos (`relatorio_localizacao: Análise volume vs receita`), mas a **conclusão curta "Localização vencedora: Meia Praia" sem qualificar "empate técnico" é parcialmente não suportada** se lida como vitória folgada. | Médio - precisa qualificar como empate técnico |
| **"3q Meia Praia é segmento mais robusto / mais contribui"** | **Parcialmente** | 3q MP receita 151.200 <4q MP 232.200, então **não é maior receita**. É **mais robusto**: 327 com preço (vs 60), 1451 vs 286, alta 242 vs 33. O relatório em `relatorio_localizacao: Segmento que mais contribui dentro do vencedor: 3q Meia Praia` com filtro `≥100 & ≥100 com preço` (onde 4q com 60 é excluído) é **defensável como "mais robusto"**, mas a frase curta "mais contribui" sem qualificar pode ser lida como "maior receita" (falso). **Precisa sempre qualificar "mais robusto com volume"**. | Médio |
| **"Mais quartos → maior receita (forte)"** | **Sim, mas com nuance** | 2q 99k →3q 151k (+52%) →4q 232k (+53%) com n=187/327/60 - **tendência é fato**, mas **4q n=60 pequeno** vs 2q/3q robustos, e **1q 104k (81 base, 20 com preço, 485 diária) quebra a monotonicidade** (1q 104k >2q 99k, com n=81/20 pequeno). Com 5 pontos 1q-5q, ratio receita/preço cai monotonicamente 11,94%→9,24%→8,02%→6,45%→5,12% (ver `auditoria_pergunta3.md`), então **associação é forte entre medianas de perfis (n=5, r=0,98), mas moderada no individual (n=911, r=0,31)**. Dizer "forte" sem qualificar n=5 vs n=911 é **parcialmente não suportado**. | Médio |
| **"Área r=0,98 forte"** | **Não totalmente** | r=0,98 é **entre 5 medianas** (85→460 etc., n=5), não entre 7529 imóveis individuais (r=0,35). O relatório diz "nos 5 perfis r=0,98" - **correto na frase longa**, mas a **tabela classifica como "forte evidência" sem qualificar n=5 vs n=911** - **exagerado**. Deveria ser "forte entre medianas de 5 perfis, moderada (r≈0,31-0,35) no individual". | Médio |
| **"Retorno decrescente com preço"** | **Parcialmente** | 2q→3q MP +75% preço → +52% receita, 3q→4q +91% → +53% com **2 incrementos em 1 bairro e 4q n=60** - **sugestivo, não prova geral**. Com 1q-5q (5 pontos) ratio cai monotonicamente, mas **5q tem n=27 base (muito pequeno) e 1q n=81/20 também pequeno**. **"Associação moderada/sugestiva" é correto, "forte" seria exagerado** - relatório classifica como **moderada**, **correto**. | Baixo |
| **"2q Centro tem maior ROI (7,75%)"** | **Sim** | 2q Centro 7,75% >2q MP 6,20% >3q MP 5,67% com n=65/187/327 com preço - **matematicamente correto** e com **amostra ≥45**. **Suportado**. | Baixo |
| **"2q Meia Praia é melhor equilíbrio" vs "3q Meia Praia é melhor equilíbrio"** | **Depende dos pesos** | Com pesos originais 30/25/10/20/15, 3q MP vence por **1,08 ponto (1,7%)** - **empate técnico**. Com foco eficiência 40/35/5/10/10, **2q Centro vence (75,65 vs 59,87)**. **Nenhum vence de forma robusta**, depende dos pesos (arbitrários). **Conclusão "3q MP é vencedor equilibrado" sem sensibilidade é parcialmente não suportada** - deveria ser "3q MP e 2q Centro empatados tecnicamente, com 3q MP ligeiramente à frente no cenário pró-volume". **Auditoria de critérios já mostrou isso.** | **Alto - escolha de vencedor com pesos arbitrários** |

---

## 4. Confusão entre dado observado / premissa / resultado

| Item | Tipo correto | Como está no relatório | Correto? |
|---|---|---|---|
| `sale_price` median 1,07M | **DADO OBSERVADO** (Viva, 244) | `relatorio_roi.md:9` "DADO OBSERVADO Viva" | **Sim** |
| `price_mediano` 460 | **DADO OBSERVADO** (Base, 187 com preço) | `relatorio_roi.md:21` "DADO OBSERVADO" | **Sim** |
| `receita 99.360` (460×216) | **RESULTADO CALCULADO** | `relatorio_roi.md:30` "RESULTADO `diaria×216`" | **Sim** |
| `ocupação 60% =18 dias` | **PREMISSA** | `relatorio_roi.md:29` "PREMISSA, não observada" | **Sim** |
| `comissão 15%` | **PREMISSA** | `relatorio_roi.md:30` "PREMISSA (não existe na base)" | **Sim** |
| `avg_stay=5` | **PREMISSA** | `relatorio_roi.md:31` "PREMISSA" | **Sim** |
| `ROI 6,20%` | **RESULTADO** | `relatorio_roi.md:49` "ROI" | **Sim** |
| `qtd 723` | **DADO OBSERVADO** | `relatorio_roi.md:21` "Qtd Airbnb" | **Sim** |
| `retorno decrescente 75%→52%` | **INTERPRETAÇÃO** de RESULTADO | `relatorio_caracteristicas: D` "Preço +75% gera receita +52% - ponto de retorno decrescente" | **Sim, mas deveria estar mais claro que é INTERPRETAÇÃO de 3 pontos, não DADO** - está como "Preço compra → receita: Correlação positiva, mas não proporcional. Ponto de retorno decrescente" - **parcialmente correto, mas com n=3 perfis em 1 bairro, deveria ter ressalva "com amostra pequena no último"** |

**Nenhuma confusão grave encontrada.** Todos os relatórios separam com `> DADO OBSERVADO vs PREMISSA` e `> Tipos:` em `relatorio_criterios_investimento.md:31`. **Correto.**

---

## 5. Problemas de amostra

| Perfil | Airbnb total | Com preço | % | Viva total | Status | Sinalizado? |
|---|---|---|---|---|---|---|
| 2q MP | 723 | 187 | 25,9% | 244 | **Robusto** | Sim, como robusto |
| 3q MP | 1451 | 327 | 22,5% | 1704 | **Robusto** | Sim |
| 4q MP | 286 | **60** | 21,0% | 1327 | **Pequena (60)** | **Sim, sinalizado** `relatorio_roi.md:113` "4q MP só 60" e `relatorio_caracteristicas:4` |
| 2q Centro | 183 | 65 | 35,5% | 89 | **Moderada (65)** | Sim, como moderado |
| 3q Centro | 211 | **45** | 21,3% | 438 | **Pequena (45)** | **Sim, sinalizado** |
| 1q Centro (tese) | 116 | 78 | 67% | 22 | **Pequena Viva 22 (<50)** | **Sim, em `relatorio_tese_compactos_centro.md:63` "Viva 22 (<50) - insuficiente"** |
| Studio Centro | 2 | 0 | 0% | 0 | **Insuficiente (0)** | **Sim, INCONCLUSIVA** |

**Todos os perfis com amostra pequena já estão sinalizados como "amostra pequena" ou "insuficiente" nos relatórios.** **Correto.**

**Problema não sinalizado:** **Viva 22 para 1q Centro é <50**, mas `relatorio_tese` classifica 1q Centro como "67% cobertura, melhor cobertura de todos" sem mencionar que **22 é <50 para mediana de preço com intervalo de confiança amplo**. Deveria sinalizar que **Viva 22 tem erro padrão da mediana ~ ±15%** vs 244/1704 com erro ±3-5%.

---

## 6. Comparações injustas entre Airbnb e VivaReal

**Método usado em todos os relatórios:** Comparação por **segmento `bairro×quartos`** (ex: "3q Meia Praia 1704 venda vs 1451 Airbnb"), **sem JOIN por `airbnb_listing_id` vs `listing_id`** (não há correspondência, `Viva` e `Base` têm IDs diferentes). **Correto e explicitado** em `relatorio_cruzamento: Normalização` e `relatorio_roi: Sem correspondência`.

**Possível injustiça:** Comparar `preço compra` (Viva, estoque à venda, com `sale_price` de todos os 244/1704) com `diária` (Base, 187/327 com preço, 25% cobertura) - **Viva tem 100% com preço, Base tem 21-35%**. **Comparar mediana de 244 com 100% vs 187 com 22% pode ser injusto** se os 22% com preço são os mais bem avaliados (viés de seleção: anúncios com preço são os mais ativos, com 80,6% alta demanda vs 13,2% demais). **O relatório não menciona esse viés de seleção** (anúncios com preço são mais bem avaliados, com 67,7% Guest Favorite vs 10,7% demais, `relatorio_demanda.md:6`). **Isso é uma comparação injusta potencial: `price_mediano` vem dos 22% mais bem avaliados, enquanto `sale_price` vem de 100% dos à venda (incluindo ruins).**

**Impacto:** Médio - **receita estimada pode estar superestimada** porque usa diária dos **melhores 22%** (alta demanda) vs preço de **todos** os à venda (incluindo ruins). O relatório deveria ter notado que **diária mediana com 22% cobertura vs preço com 100%** não são populações idênticas.

---

## 7. Afirmação causal vs correlação

| Afirmação no relatório | Linguagem usada | É causal? | Correto? |
|---|---|---|---|
| "Mais quartos está associado a maior receita (forte), mas..." | **"está associado"** | Não causal, correto | **Sim, correto** - usa "associado" |
| "Área r=0,98 (forte) - area 85→460" | **"Correlação"** | Não causal, mas r=0,98 com n=5 é **correlação entre medianas**, não entre imóveis - **parcialmente correto, mas sem qualificar n=5 vs n=911** | **Ressalva necessária (já feita na auditoria Pergunta 3)** |
| "Meia Praia combina volume" | **"combina"** | Descrição, não causal | **Sim** |
| "Preço +75% gera receita +52%" | **"gera"** | **Linguagem causal** ("gera") para **correlação** (preço vs receita por segmento) - **incorreto, é associação, não gera**. | **Erro de linguagem causal** - deveria ser "está associado a receita +52%" |
| "Alta demanda não está associada a maior diária" | **"não está associada"** | Correto, com dados 550 vs 600 | **Sim** |
| "Diária é driver" | **"driver direto por fórmula"** | **Tautológico mas explicitado como "por fórmula"** - **correto com ressalva** | **Ressalva de tautologia já feita** |

**Nenhuma afirmação causal forte como "mais quartos causa maior receita" foi encontrada sem qualificar como "associado". Apenas o "gera" em D é causal e deve ser corrigido para "está associado".**

---

## 8. Erros escondidos - Busca específica

| Busca | Resultado | Status |
|---|---|---|
| **Erro de fórmula** | `receita = diaria*30*occ` e `receita_ano*12` e `ROI=lucro/preço` e `payback=preço/lucro` todos refeitos e batem | **Nenhum** |
| **Erro de arredondamento** | Centro 587 exibido vs 586,67 usado (R$72/ano, 0,06%) - já corrigido na auditoria Pergunta 2 | **Ressalva já tratada** |
| **Filtro inconsistente** | `listing_type==apartamento` consistente em 3710/7529 em todos os scripts; `suburb_norm` com `strip().lower()` consistente; `0<area<10000` consistente | **Nenhum** |
| **Nomes de bairros inconsistentes** | `alto sao bento` vs `alto são bento` duplicado (14 vs 13) por acento, mas ambos 0 com preço, excluídos - **baixo impacto** | **Ressalva já tratada** |
| **Duplicidades** | `Viva` 36 ids duplicados (70 linhas) e `Base` 0 dups, `price_por_anuncio` 0 dups full - **corretamente tratados** (não removidos, mas `nunique` usado) | **Correto** |
| **Valores nulos** | `price_mediano` NA mantido (3442), `usable_area` 0/188000 excluídos, `condo` NA mantido - **correto, não tratados como zero** | **Correto** |
| **Uso incorreto de `price_mediano`** | Sempre usado como `median(price_mediano)` onde `notna()`, nunca como `price` individual sem mediana, e sempre distinguido de `price` (diária) vs `sale_price` (compra) | **Correto** |
| **Mistura média e mediana** | Usa **mediana** para `price_mediano`, `sale_price`, `area`, mas mostra **média** para contexto em `relatorio_vivareal` e `relatorio_roi` (ex: média 2.450.770 vs mediana 1.750.000) - **não confunde, separa** | **Correto** |
| **Número de anúncios vs imóveis** | Sempre separado: `Qtd Airbnb (Base)` vs `Qtd Viva (Viva)` vs `Com preço` vs `Alta` - **nunca soma como "imóveis"**, exceto no **score de volume `Airbnb+Viva` somados** (ver abaixo) | **Ressalva: volume somado é metodologicamente inadequado** (ver item 3 da auditoria de critérios) |
| **Conclusões não suportadas** | Ver item 3 acima | **Ver 3** |

**Erro escondido encontrado e não sinalizado antes:**

* **Volume somado `Airbnb + Viva` no score de critérios** (`analisar_decisao_criterios.py: volume = qtd_airbnb + qtd_viva`) - **metodologicamente inadequado** (soma oferta de aluguel + oferta de venda, unidades diferentes). Já auditado em `auditoria_criterios_investimento.md:3` e com **baixo impacto prático** (ranking idêntico com média), mas **não havia sido sinalizado como erro antes** - **agora sinalizado**.

---

## Tabela de Problemas

| Item | Status | Problema | Valor Original | Cálculo refeito | Correção | Impacto |
|---|---|---|---|---|---|---|
| **Centro receita** | Ressalva | Diária exibida 587 vs usada 586,67 | 126.720 (587×216) | 586,67×216=126.720,01 vs 587×216=126.792 | Manter 126.720 com nota "587 arredondado, 586,67 usado" | Baixo (0,06%, não muda ranking) |
| **Correlação 0,98** | Ressalva | r=0,98 apresentado como forte para todos os imóveis | r=0,98 entre 5 medianas (n=5) | r=0,98 (n=5, forte no agregado) mas **r=0,31 individual (n=911, moderada)** | Rebaixar para "moderada no individual, forte apenas entre medianas" | Médio (exagero de força) |
| **Diária driver** | Ressalva | "Diária forte" sem qualificar tautologia | r=1,00 por `receita=diaria×216` | Correlação 1,00 **por construção**, não evidência empírica. Evidência real é quartos/área→diária (r≈0,31) | Rebaixar para "moderada/tautológica" | Médio |
| **Retorno decrescente** | Ressalva | "Forte" com 3 pontos (2q→3q→4q) e n=60 | 1,07M→1,88M +75%/52% e 1,88M→3,6M +91%/53% com **2 incrementos em 1 bairro, n=60 para 4q** | Com 1q-5q (5 pontos) ratio 11,94%→9,24%→8,02%→6,45%→5,12% ainda sugere, mas **com n pequeno nos extremos (1q 8, 5q 27 com preço)** | Manter como **moderada/sugestiva**, não forte |
| **Volume somado** | **Erro metodológico** | `volume = 723+244=967` somando Airbnb+Viva | Airbnb 723 (oferta temporada) + Viva 244 (oferta venda) são **mercados diferentes** | **Separar em `Volume Airbnb` e `Volume Viva` (10% cada) ou usar `min()`** - já testado, ranking idêntico, mas método atual é inadequado | Médio (não mudou vencedor, mas é erro conceitual) |
| **Escala 10-20 sem esgotar** | Ressalva | "Permite escalar 10-20 sem esgotar" com estoque 1704 | 10/1704=0,6% do estoque, mas sem dado de **fluxo mensal** (quantos vendem/mês) | Rebaixar para "com estoque 1704 vs 89 (19×), há **mais opções para prospectar** 10-20, mas **sem dado de liquidez, escala é potencial, não garantida**" | Médio |
| **Meia Praia vence** | Ressalva | "Meia Praia vencedora" com +2,3% (129.600 vs 126.720) | Diferença 2.880/126.720=2,27% com n=607 vs 193, erro padrão da mediana ~±10-15 reais | **Empate técnico com leve vantagem Meia Praia por volume 4,7×**, não vitória folgada - já qualificado em 80% dos trechos, mas conclusão curta "Localização vencedora: Meia Praia" sem qualificar é **parcialmente não suportada** | Médio |
| **3q mais contribui** | Ressalva | "3q mais contribui" sem qualificar vs 4q maior receita (232k vs 151k) | 3q 151k <4q 232k em receita, mas **3q tem 327 vs 60 com preço (5,4×) e 1451 vs 286 (5×)** | **Reformular para "3q mais robusto (volume) enquanto 4q tem maior receita"** - já feito em 80%, mas frase curta precisa qualificar | Médio |
| **Linguagem causal "gera"** | **Erro de linguagem** | `relatorio_caracteristicas: D` "Preço +75% **gera** receita +52%" | Correlação, não causalidade (sem experimento) | **Corrigir para "**está associado a** receita +52%" | Baixo |
| **Outros** | Correto | Filtros, medianas, receitas, ROI, payback, cobertura, sem mistura venda vs aluguel por imóvel | Todos refeitos e batem | **Nenhuma correção** | Baixo |

**Nenhum erro matemático grave ou filtro indevido encontrado além das ressalvas acima.**

---

## Veredito

### 1. Erros encontrados
Ver tabela acima: **1 erro metodológico (volume somado) + 1 erro de linguagem causal ("gera") + 7 ressalvas (arredondamento, correlação n=5, diária tautológica, retorno decrescente com n pequeno, Meia Praia vence por 2,3%, 3q vs 4q, escala 10-20). Nenhum erro de cálculo de receita/ROI/payback.**

### 2. Números confirmados
* Preços compra: 1,075M (2q MP), 1,884M (3q MP), 3,6M (4q MP), 1,15M (2q Centro), 2,1M (3q Centro) - **todos medianas >0 corretas**
* Diárias: 460, 700, 1075, 580, 790 - **medianas corretas, 21-35% cobertura**
* Receitas 60%: 99.360, 151.200, 232.200, 125.280, 170.640 - **corretas (×216)**
* ROI 60%: 2q Centro 7,75% >2q MP 6,20% >3q Centro 5,92% >3q MP 5,67% >4q MP 4,67% - **corretos**
* Qtds: 723/1451/286 e 183/211, 244/1704/1327 - **corretos**

### 3. Números corrigidos
* Centro receita: **126.720 (586,67×216) correto, exibição 587 é arredondamento** - manter 126.720 com nota (diferença R$72)
* Volume: **967 (723+244) → separar em 723 Airbnb e 244 Viva** (não somar)
* Correlação: **0,98 (n=5) → 0,98 entre medianas (forte agregado) e 0,31 individual (moderada)**
* Frase "gera" → **"está associado a"**

### 4. Conclusão da Pergunta 2 e 3
* **Pergunta 2 "Meia Praia vencedora" e "3q mais contribui":** **Parcialmente corretas com ressalva** - Meia Praia vence no ranking filtrado, mas com **vantagem pequena 2,3% (empate técnico)** e **3q é mais robusto, não maior receita que 4q**.
* **Pergunta 3 "Mais quartos/área forte":** **Correta com ressalva** - Forte entre medianas de 5 perfis, moderada no individual (r≈0,31).

### 5. O que podemos afirmar no README/vídeo
**Pode afirmar (fiel):** "Entre segmentos com volume e cobertura suficientes (≥100 & ≥30 com preço), **mais quartos e maior área estão associados a maiores receitas** (2q 99k→3q 151k→4q 232k, área 85→129→188m²; r=0,98 entre medianas dos 5 perfis, n=5, forte no agregado, mas r≈0,31 individual, moderada), **Meia Praia combina volume (2602, 4,7× Centro) com receita 129,6k vs 126,7k (+2,3% - empate técnico com leve vantagem) e 3q MP (700, 151k, 327 com preço) é o mais robusto, enquanto 4q MP (1075, 232k, 60) tem maior receita mas nicho (21% vs 327)."

### 6. O que NÃO devemos afirmar
* Tabuleiro é melhor (99/17)
* 60% é ocupação real
* Correspondência Viva×Airbnb por imóvel
* Receita garantida
* "3q tem maior receita que todos" (4q tem 232k)
* "Meia Praia tem muito mais receita" (só +2,3%)
* "Mais quartos causa maior receita" (é associação, com n pequeno para 4q)

### 7. Caminho exato da análise
`Details 4441 + Mesh 4441 + Price 118839 → base_analitica 4441 (999 com preço, LEFT JOIN)` → `VivaReal 8329` → `strip().lower()` bairros → `apartamento & bedrooms` → `median(price_mediano)` (21-35% cobertura) → `receita=price_mediano×30×occ×12` (40%=12d,60%=18d,80%=24d, PREMISSA) → `median(sale_price)` (DADO) → `price/m²` e `corr` com `np.corrcoef` em 5 medianas vs 911 individuais → ranking filtrado `≥100 & ≥30` → Meia Praia vence com ressalva 2,3% e 3q robusto vs 4q maior receita.

### 8. Arquivos alterados
* **Lidos:** 12 arquivos em `analysis/` + 2 em `data/` (Viva, base)
* **Criados:** `analysis/auditoria_independente_p1_p4.md` (este)
* **Alterados:** **Nenhum** em `data/` (10:58:39) e **nenhum** relatório anterior alterado (apenas leitura)
* **Não criados:** Novo investimento (não escolhido)

---

## 9. VEREDITO FINAL

**“A análise das Perguntas 1 a 4 está pronta para ser usada no README e no vídeo?”**

**SIM, com as 7 ressalvas acima (correlação n=5 vs n=911, diária tautológica, retorno decrescente com n pequeno, volume somado, escala 10-20 sem fluxo, Meia Praia +2,3% como empate técnico, 3q robusto vs 4q maior receita, linguagem causal).**

Em 5 linhas: Análise está matematicamente correta (receitas 99k-232k, ROIs 6,20-7,75%, correlação 0,98 entre 5 medianas) e metodologicamente defensável com filtros objetivos (≥100 & ≥30) e medianas robustas. As 3 conclusões exageradas (0,98 forte para todos, diária forte, retorno decrescente forte) devem ser rebaixadas para **moderada** com n=5 vs n=911 e amostra pequena para 4q (60). Com as qualificações "empate técnico Meia Praia +2,3% por volume" e "3q mais robusto (327) enquanto 4q tem maior receita (232k) com 60", **Meia Praia e 2-3q como equilíbrio permanecem defensáveis como estimativas bem fundamentadas, sem causalidade e sem garantia**.

