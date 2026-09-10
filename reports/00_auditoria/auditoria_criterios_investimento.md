# Auditoria - Critérios para Decisão de Investimento (Pergunta 4, sem tese studio/1q Centro)

> **Status: [APROVADO COM RESSALVAS - PESOS ARBITRÁRIOS, VENCEDOR NÃO ROBUSTO]**
> **Arquivos auditados:** `analysis/analisar_decisao_criterios.py:1`, `analysis/relatorio_criterios_investimento.md:73`, `analysis/candidatos_investimento.csv:7` (5+1 perfis), `analysis/base_analitica_itapema.csv:4441` (3710 apto), `data/VivaReal_Itapema.csv:8329` (7529 apto), `analysis/localizacao_receita.csv:46`, `analysis/roi_perfil.csv:15`
> **Método auditado:** Score ponderado `0-100` por critério (retorno 30, capital 25, receita 10, volume 20, robustez 15) com `volume = Airbnb + Viva` somados.

---

## 1. Pesos 30/25/20/15/10 são justificados ou arbitrários?

**Verificação:** Pesos foram definidos em `analisar_decisao_criterios.py: Pesos justificados:` com texto "Eficiência do capital é central..." mas **sem nenhum cálculo data-driven** (ex: sem AHP, sem regressão, sem otimização). São **escolhas do analista**, não derivadas dos dados.

**Evidência:**
* Soma pesos =100, mas distribuição 30/25/20/15/10 não tem ancoragem em `base` ou `Viva` (ex: não há correlação entre retorno e volume que justifique 30 vs 20).
* Texto "Volume e robustez devem ter peso maior que retorno isolado para Seazone, porque retorno alto com n=65 não escala" é **interpretação plausível** para Seazone (3000 imóveis, precisa escalar), mas **não é dado** - é **premissa estratégica** da Seazone, não evidência empírica.
* Pesos não foram validados com sensibilidade no relatório original (só apresentados como definitivos).

**Veredito:** **Arbitrários, mas com justificativa estratégica plausível para Seazone.** Não são errados, mas são **escolhas**, não **descoberta**. Deveriam ser apresentados como **"cenário de pesos para Seazone focada em escala"**, com sensibilidade, não como "pesos corretos".

---

## 2. Teste de sensibilidade - Vencedor continua?

**Refeito com `normalize()` 0-100 entre os 5 perfis:**

| Cenário de pesos | Vencedor | Score | 2º lugar | Diferença |
|---|---|---|---|---|
| **Original 30/25/10/20/15** (retorno 30, capital 25, receita 10, volume 20, robustez 15) | **3q MP 62,48** | 2q Centro 61,40 | **+1,08 (1,7%) - empate técnico** |
| **Teste 1: foco eficiência 40/35/5/10/10** (retorno 40, capital 35, receita 5, volume 10, robustez 10) | **2q Centro 75,65** | 2q MP 67,58 | 3q MP cai para 3º (59,87) - **vencedor muda** |
| **Teste 2: sem dupla contagem receita 50/30/0/10/10** (retorno 50, capital 30, receita 0) | **2q Centro 79,82** | 2q MP 68,87 | 3q MP 58,06 - **vencedor muda** |
| **Teste 3: pesos iguais 20/20/20/20/20** | **3q MP 68,46** | 2q MP 47,46 | 2q Centro 44,73 - **3q MP volta a vencer, mas com outra ordem** |

**Conclusão:** **3q Meia Praia NÃO é robusto a mudanças de pesos.** Com foco em **eficiência (retorno+capital 75%)**, **2q Centro vence folgado** (75,6 vs 59,8, +26%). Com **pesos iguais**, 3q MP vence, mas 2q Centro cai para 3º. **Diferença original 62,48 vs 61,40 é apenas 1,08 ponto (1,7%) - empate técnico**, não vitória clara. **O vencedor depende dos pesos, que são arbitrários.**

**Impacto:** **Alto** - O ranking apresentado como definitivo (1. 3q MP, 2. 2q Centro) **não é estável**. Para hackathon, deve ser apresentado como **"2q Centro e 3q MP empatados tecnicamente, com 3q MP ligeiramente à frente no cenário pró-volume"**, não como vencedor isolado.

---

## 3. Volume = Airbnb + Viva - Pode somar?

**Método atual `analisar_decisao_criterios.py: volume = qtd_airbnb + qtd_viva` e depois `normalize(volume)`.**

* **O que cada base representa (DADO OBSERVADO):**
  * `qtd_airbnb` (Base, 723 para 2q MP, 1451 para 3q MP): **estoque de anúncios de aluguel por temporada ativos** (oferta de temporada, proxy de demanda e concorrência).
  * `qtd_viva` (Viva, 244, 1704): **estoque de imóveis à venda ativos** (oferta de compra, liquidez para aquisição).

* **São coisas diferentes:** Uma mede **concorrência no aluguel**, outra **oportunidade de compra**. Somá-las (723+244=967 para 2q MP vs 183+89=272 para 2q Centro) **mistura oferta de dois mercados distintos com unidades diferentes** (um é anúncio, outro é imóvel). Metodologicamente, **não é adequado somar** - é como somar maçãs e laranjas para dizer "volume de mercado".

* **Teste com volume separado:** Recalculado com `score_volume = (normalize(qtd_airbnb) + normalize(qtd_viva))/2` (média) em vez de soma, com pesos originais 30/25/10/20/15:
  * 3q MP 66,49 (100 volume) vs 2q Centro 57,27 (0 volume) - **ranking idêntico a original (3q MP vence por 9 pontos)**, então **neste caso a distorção não mudou o vencedor**, mas o método continua conceitualmente incorreto.

* **Forma melhor (recomendação):** **Manter 2 critérios separados:** `Volume Airbnb` (20% → 10% + 10%) e `Volume Viva` (10% +10%) ou usar **mínimo** (`min(qtd_airbnb, qtd_viva)`) para capturar gargalo (não adianta ter 1704 à venda se só há 183 para alugar). Outra forma defensável: **usar apenas `qtd_airbnb` com preço (com_preco) para robustez**, e `qtd_viva` apenas como contexto, não no score.

**Veredito:** **Metodologicamente inadequado somar**, mas com **baixo impacto prático** neste caso (vencedor não muda com média). **Deve ser corrigido para apresentação:** separar em dois subcritérios ou usar `qtd_airbnb` como volume principal e `qtd_viva` como contexto.

---

## 4. "Permite escalar 10-20 aquisições sem esgotar o mercado" - Temos dados?

**Dado observado:** `3q MP: 1704 à venda (Viva, estoque snapshot) + 1451 Airbnb (estoque)` - são **estoques em um momento**, não **fluxo de transações** (quantos realmente vendem por mês).

**Afirmação no relatório:** `relatorio_criterios_investimento.md:63` "permite comprar 10-20 unidades sem esgotar mercado, com receita 151k/ano por unidade e alta 242".

**Análise:** 10-20 / 1704 = **0,6-1,2% do estoque à venda**. Parece plausível como **ordem de grandeza**, mas **não temos dados de liquidez** (tempo médio de venda, absorção mensal, taxa de conversão de anúncio para venda). Um estoque de 1704 pode ter **baixa rotatividade** (ex: 5% vende por mês = 85/mês, então 20 é 23% do fluxo mensal - já relevante). Sem dado de **vazão**, afirmar "sem esgotar" é **extrapolação além dos dados**.

**Correto seria:** "Com **estoque de 1704 à venda** (vs 89 em 2q Centro, 19× maior), **há mais opções para prospectar** 10-20 unidades, mas **não temos dado de liquidez** (quantos vendem por mês), então **escala é potencial, não garantida**."

**Veredito:** **Extrapolação, não dado.** Deve ser **rebaixado de afirmação para hipótese** com ressalva de estoque vs fluxo.

---

## 5. Comparação sem assumir vencedor - 5 perfis lado a lado

**Recalculado sem pesos, apenas dados observados e resultados:**

| Perfil | Retorno bruto 60% (RESULTADO) | Preço (DADO) | Receita 60% ano (RESULTADO) | Airbnb | Com preço | Viva | Alta |
|---|---|---|---|---|---|---|---|
| **2q Morretes** | **13,62%** (498×216/790k) | 790k | 107.568 | 229 | 51 (22%) | 1044 | 30 (13%) |
| 2q Centro | 10,89% | 1,15M | 125.280 | 183 | 65 (36%) | 89 | 34 (19%) |
| 2q MP | 9,24% | 1,075M | 99.360 | 723 | 187 (26%) | 244 | 151 (21%) |
| 3q Centro | 8,13% | 2,1M | 170.640 | 211 | 45 (21%) | 438 | 22 (10%) |
| 3q MP | 8,02% | 1,88M | 151.200 | 1451 | 327 (23%) | 1704 | 242 (17%) |
| 4q MP | 6,45% | 3,6M | 232.200 | 286 | 60 (21%) | 1327 | 33 (12%) |

**Sem pesos, por critério isolado:**
* **Maior retorno:** 2q Morretes 13,62% >2q Centro 10,89% >2q MP 9,24%
* **Menor capital:** 2q Morretes 790k <2q MP 1,075M
* **Maior receita:** 4q MP 232k >3q Centro 170k >3q MP 151k
* **Maior volume Airbnb:** 3q MP 1451 >2q MP 723 >4q MP 286
* **Maior robustez (com preço):** 3q MP 327 >2q MP 187 >2q Centro 65

**Conclusão sem assumir vencedor:** **Nenhum perfil domina todos os critérios.** 2q Morretes domina **retorno** e **capital**, mas é **Morretes** (fora do eixo premium Meia Praia/Centro, com diária 498 <460? Na verdade 498 >460, mas é Morretes, com preço/m² diferente). 4q MP domina **receita** mas perde em **capital e robustez**. **3q MP é o único no top 2 em volume (1º), robustez (1º) e receita (3º), com retorno mediano (4º) - por isso aparece como equilíbrio, mas não vence em nenhum critério isolado.**

**O relatório original ao escolher 3q MP como vencedor estava correto em buscar equilíbrio, mas deveria ter incluído Morretes na comparação principal para não parecer que escondeu um concorrente com retorno maior.**

---

## 6. Incluir 2q Morretes - Exclusão justificada?

**Dados 2q Morretes (DADO OBSERVADO):** 1044 à venda, 790k median, 229 Airbnb, 51 com preço (22,3%), diária 498, receita 107.568, retorno **13,62%** (maior que todos os 5), alta 30 (13,1%), área 69m².

**Por que foi excluído dos 5 principais?** `analisar_candidatos_investimento.py` filtrou `qtd_airbnb>=50 e qtd_viva>=50 e com_preco>=20` e achou Morretes, mas `relatorio_criterios_investimento.md` manteve **5 principais = 2q/3q/4q MP +2q/3q Centro** (decisão prévia de focar Meia Praia/Centro) e colocou Morretes como "extra" com nota "Não é Meia Praia/Centro, mas é candidato a observar."

**Justificativa real baseada em dados vs decisão prévia:**
* **Justificativa real:** Morretes tem **retorno bruto maior (13,62% vs 10,89% 2q Centro)**, **preço menor (790k vs 1,07M)**, **volume Viva 1044 vs 244 (4× maior que 2q MP)** e **volume Airbnb 229 vs 183 (similar a 2q Centro)** - **objetivamente, deveria estar entre os 3 primeiros por retorno+capital+volume**.
* **Justificativa do relatório:** "Não é Meia Praia/Centro, mas é candidato a observar" - **decisão prévia de focar eixo premium, não dado**. Morretes tem **diária 498 >460 (2q MP) e preço/m² ~11.449 (790k/69m²) vs 12.929 (2q MP)**, então **não é inferior em qualidade**, apenas **fora do foco estratégico** (Seazone pode preferir Meia Praia/Centro por liquidez turística vs Morretes mais residencial).

**Veredito:** **Exclusão de Morretes é arbitrária, não data-driven.** Se o critério é **retorno+capital+volume**, Morretes **deveria ter entrado no top 3**, superando 3q Centro e 4q MP. A justificativa correta seria: **"2q Morretes tem maior retorno bruto (13,62%) e menor capital (790k) com volume 229/1044, mas foi mantido como 5º candidato extra porque Seazone historicamente foca Meia Praia/Centro (maior liquidez turística e ticket), não por ser inferior nos números."** O relatório deveria ter sido transparente sobre isso, em vez de dizer "Nenhum extra supera os 5 principais em equilíbrio" (falso para Morretes).

---

## 7. Receita com 10% de peso - Dupla contagem?

**Receita = diária ×30×occ×12** - **diária já está em retorno** (`retorno = receita/preço = diária×216/preço`), então **receita e retorno compartilham diária e ocupação**. Dar 10% para receita **além** de 30% para retorno é **contar diária duas vezes** (uma via retorno, outra direta).

**Teste sem receita (pesos 50/30/0/10/10):**
* Original 30/25/**10**/20/15 → 3q MP 62,48 >2q Centro 57,27
* Sem receita 50/30/**0**/10/10 → 2q Centro 79,82 >2q MP 68,87 >3q MP 58,06 - **vencedor muda de 3q MP para 2q Centro**

**Impacto:** **Alto** - 10% de receita parece pouco, mas é suficiente para fazer 3q MP (receita 151k, 3º maior) superar 2q Centro (125k, 4º) quando somado a volume. Sem receita, 2q Centro vence.

**Forma melhor:** **Remover receita como critério separado** e manter apenas **retorno (que já contém receita) e volume**. Ou, se manter receita, **explicitar que é redundante e com peso baixo justamente por isso**, e mostrar sensibilidade sem ela.

**Veredito:** **Metodologicamente inadequado dar peso a receita quando retorno já a contém.** Deveria ser **0% ou explicitado como duplo, com sensibilidade**.

---

## 8. Não confundir maior retorno, maior receita, maior volume e maior robustez

**No relatório original:**
* Maior **retorno**: 2q Morretes 13,62% (ou 2q Centro 10,89% entre os 5) - **correto**
* Maior **receita**: 4q MP 232.200 - **correto**
* Maior **volume**: 3q MP 1451 Airbnb / 1704 venda - **correto**
* Maior **robustez**: 3q MP 327 com preço (23%) - **correto**

**O relatório não confunde** - em `relatorio_criterios_investimento.md: Comparação` separa cada coluna. **Porém** a frase "3q MP tem 100 em volume" pode ser lida como "volume = receita", mas o relatório separa. **Parcialmente correto, mas poderia reforçar:** 4q MP tem **maior receita mas menor volume e menor robustez**, 2q Centro tem **maior retorno mas menor volume** - são coisas diferentes, e o score tenta equilibrar, mas com pesos arbitrários.

---

## Parecer direto

### Quais partes são sólidas
* **Dados observados:** Preços, diárias, qtds, com_preco, alta - todos recalculados e corretos, sem erro matemático, com normalização `strip().lower()` adequada.
* **Filtros e cobertura:** Exclusão de Tabuleiro 99/17 etc. com critério objetivo ≥30 com preço, sinalização de amostra pequena (60,45) - **sólido**.
* **Cálculos de receita/retorno:** `diaria×216/preço` corretos, sem confundir venda vs aluguel por imóvel (segmento).
* **Identificação de trade-offs:** 4q maior receita mas capital 3,3×, 2q Centro maior retorno mas volume 89 - **sólido**.

### Quais partes são arbitrárias ou precisam ajuste
* **Pesos 30/25/20/15/10: arbitrários**, não derivados dos dados; diferença vencedor 62,48 vs 61,40 é **1,08 ponto (1,7%) dentro da margem de arredondamento** - **não é vitória robusta**.
* **Volume = Airbnb+Viva somados: metodologicamente inadequado** (mistura oferta de dois mercados) - corrigir para média ou dois critérios separados.
* **Escala 10-20 unidades sem esgotar: extrapolação** (estoque vs fluxo) - rebaixar para hipótese.
* **Exclusão Morretes: arbitrária** (decisão prévia Meia Praia/Centro, não dado) - Morretes tem retorno 13,62% > todos os 5 e deveria estar no top 3.
* **Receita com 10%: dupla contagem** com retorno (receita já em retorno) - remover ou zerar e mostrar sensibilidade.
* **Correlação e diária como "forte" em outros relatórios**: já auditado, mas aqui também afeta.

### Ranking permanece depois dos testes?
**Não de forma robusta.**
* **Original (30/25/10/20/15):** 3q MP 62,48 >2q Centro 61,40 (empate técnico, +1,7%)
* **Foco eficiência (40/35/5/10/10):** **2q Centro 75,65 >2q MP 67,58 >3q MP 59,87** - **vencedor muda para 2q Centro**
* **Sem receita (50/30/0/10/10):** **2q Centro 79,82 >2q MP 68,87 >3q MP 58,06** - **vencedor muda**
* **Pesos iguais (20 cada):** **3q MP 68,46 >2q MP 47,46 >2q Centro 44,73** - **3q MP volta, mas ordem muda**

**Conclusão: Ranking é sensível a pesos. 3q MP só vence no cenário pró-volume (original e pesos iguais). Com foco em eficiência (retorno+capital), 2q Centro vence.**

### 3q Meia Praia continua defensável?
**Sim, como *uma* escolha defensável entre empates técnicos, não como vencedora isolada.** 
* **Defensável como:** "3q MP é o **único no top 2 em volume (1º, 1451), robustez (1º, 327) e receita (3º, 151k) com retorno mediano (4º, 8,02%) e capital médio (1,88M)** - equilíbrio, com n=327 robusto e 1704 à venda para escalar 10-20 unidades (0,6-1,2% do estoque, hipótese)."
* **Não defensável como:** "3q MP tem maior retorno" (tem 8,02% vs 10,89% 2q Centro e 13,62% Morretes) ou "3q MP tem maior receita" (4q MP 232k >151k).

**Com os pesos originais, 3q MP vence por 1,08 ponto (1,7%) - dentro do erro de arredondamento - então a escolha mais honesta é declarar **empate técnico entre 3q MP e 2q Centro**, com 3q MP ligeiramente à frente no cenário pró-volume/escala e 2q Centro à frente no cenário pró-eficiência.**

### Qual critério/método seria mais adequado?
* **Método mais defensável:** **Não usar score ponderado com pesos arbitrários como decisão final**, mas **apresentar fronteira de Pareto**: plotar `retorno vs volume` e `retorno vs capital` e mostrar que **2q Centro, 2q MP e 3q MP estão na fronteira eficiente** (nenhum domina os outros em todos os critérios), enquanto 4q MP é dominado (maior receita mas pior em 3 de 4 critérios) e 3q Centro é dominado. Depois, **deixar Seazone escolher conforme estratégia**: se quer **eficiência** → 2q Centro/Morretes; se quer **escala** → 3q MP; se quer **menor capital** → 2q MP/Morretes.
* **Se precisar de um ranking único, usar pesos iguais (20 cada) ou pesos derivados de AHP com stakeholders da Seazone**, e **sempre com sensibilidade** (mostrar top 3 em 2-3 cenários de pesos) em vez de um vencedor único.
* **Volume:** separar em `Volume Airbnb` e `Volume Viva` (10% cada) em vez de somar.

---

## Arquivos

* **Lidos:** `analisar_decisao_criterios.py`, `relatorio_criterios_investimento.md`, `candidatos_investimento.csv` (7 perfis), `base_analitica_itapema.csv` (4441), `VivaReal` (8329), `localizacao_receita.csv` (45), `roi_perfil.csv` (15)
* **Criados:** `analysis/auditoria_criterios_investimento.md` (este)
* **Alterados:** **Nenhum** em `data/` (verificado `LastWriteTime` 10:58:39) e **nenhum** relatório anterior alterado nesta auditoria (apenas leitura)
* **Não criados:** `analisar_roi_v2.py` (não necessário)

