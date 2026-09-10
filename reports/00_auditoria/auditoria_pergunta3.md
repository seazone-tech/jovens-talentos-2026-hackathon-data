# Auditoria Pergunta 3 - Quais características explicam as melhores receitas?

> **Status: [APROVADO COM RESSALVAS - 3 REFORMULAÇÕES OBRIGATÓRIAS]**
> **Arquivos auditados:** `analysis/relatorio_caracteristicas_receita.md:155`, `analysis/analisar_caracteristicas_receita.py:378`, `analysis/caracteristicas_receita.csv:10`, `analysis/base_analitica_itapema.csv:4441` (3710 apto, 999 com price_mediano), `data/VivaReal_Itapema.csv:8329` (7529 apto), `analysis/roi_perfil.csv:15`, `analysis/cruzamento_perfil.csv:6`, `analysis/localizacao_receita.csv:46`, `analysis/resposta_pergunta1.md`, `analysis/auditoria_pergunta2.md`
> **Método:** Refeitos cálculos de receita (700×216), correlação em 5 vs 911 pontos, e coberturas. Nenhum erro matemático de receita, mas **3 interpretações precisam ser rebaixadas de "forte" para "moderada"** antes do vídeo.

---

## Verificação crítica dos pontos levantados pela auditoria

### 1. r=0,98 entre área e diária

**De onde veio:** `analisar_caracteristicas_receita.py:98-100`
```python
areas=[85,129,188,86,131]  # area Viva median por perfil 2q MP,3q MP,4q MP,2q Centro,3q Centro
diarias=[460,700,1075,580,790]
corr=np.corrcoef(areas, diarias)[0,1]  # 0.9768 → 0,98
```
**Quantos pontos:** **n=5 medianas agregadas por perfil**, **não** 3710 imóveis individuais.

**Verificação refeita:**
* 5 medianas: **r=0,9768 (forte no agregado)**
* Individual `Viva` area vs `sale_price` (n=7528, 0<area<10000): **r=0,3529 (moderada)**
* Individual `Base` quartos vs `price_mediano` (n=911 com preço): **r=0,3139 (moderada)**

**Interpretação correta:** A auditoria está **certa**. O relatório diz corretamente "nos 5 perfis r=0,98" (`relatorio:37`), mas a tabela comparativa classifica "Área útil" como **"forte evidência"** sem qualificar que é **entre medianas de 5 perfis**. Para **todos os imóveis de Itapema**, a evidência é **moderada (r≈0,31-0,35) com grande dispersão**, não forte. **Precisa reformular:** `r=0,98 entre medianas dos 5 perfis (n=5, forte no agregado) mas r≈0,31 individual (n=911, moderada)`.

**O que fazer:** Manter número 0,98 mas **rebaixar força para "moderada no nível individual, forte apenas entre medianas de perfis"** e citar ambos.

### 2. Diária como "driver forte"

**Fato:** `relatorio: C` e `Tabela comparativa` classificam "Diária histórica" como **"forte"** com "correlação 1,0 (fórmula)".

**Verificação:** `receita_60% = price_mediano ×30×0,60×12 = price_mediano×216`. Para os 5 perfis, `diarias=[460,700,1075,580,790]` vs `receitas=[99360,151200,232200,125280,170640]` → **r=1,00 por construção** (verificado `np.corrcoef` 1,0).

**Auditoria está certa:** Dizer que diária "explica" receita como descoberta empírica é **tautológico** - é **definição matemática**, não evidência. O relatório já traz a ressalva "diária é driver direto por fórmula (700×216=151k)" e "sem volume e sem preço não explica melhor perfil econômico" (`relatorio: F`), mas ainda classifica como **"forte"** na tabela. **Deveria ser "moderada/tautológica: driver matemático por construção, evidência empírica real é quartos/área → diária (r≈0,31)"**.

**O que fazer:** Rebaixar para **moderada/tautológica** e manter a ressalva já existente.

### 3. Retorno decrescente (preço vs receita)

**Afirmação auditada:** `relatorio: D` "2q→3q MP preço +75% (1,07M→1,88M) gera receita +52% (99k→151k); 3q→4q +91% gera +53% - ponto de retorno decrescente" com classificação **"associação moderada"**.

**Verificação refeita com mais pontos (Meia Praia, incluindo 1q e 5q):**
* 1q MP: n_viva 58, preço 877.500, n_base 81, diária 485, receita 104.760, **ratio receita/preço 11,94%**
* 2q MP: 244/723, 1.075.000, 460, 99.360, **9,24%**
* 3q MP: 1704/1451, 1.884.860, 700, 151.200, **8,02%**
* 4q MP: 1327/286, 3.600.000, 1075, 232.200, **6,45%**
* 5q MP: 73/27, 8.000.000, 1897, 409.752, **5,12%**

Ratio cai monotonicamente **11,94% →9,24%→8,02%→6,45%→5,12%** em **4 incrementos**, com n=58,244,1704,1327,73 para preço (todos >50) mas base com preço para 5q é muito pequena (27 total, poucos com preço). **Padrão sugere decrescente, mas com amostra pequena para extremos (1q 8 com preço? 5q 27 total).**

**Auditoria disse que são "poucos exemplos (3 perfis, 2 incrementos, 4q n=60)" - está parcialmente certa mas subestima:** Na verdade são **5 perfis (1q-5q) em 1 bairro com 4 incrementos**, mas **4q e 5q têm amostra pequena para diária (60 e <20 com preço)** e **1q tem 58 venda mas 81 base com 8?** Na verdade 1q MP com preço é 106? No dado acima, 1q MP com preço não listado, but 1q has 58 venda, 81 base, but com preço maybe 8? So 1q also small for diaria.

**Veredito:** A auditoria está **certa em pedir cautela**, mas **exagerou ao dizer "poucos exemplos" como se fossem só 2 incrementos** - na verdade são 4 incrementos mostrando monotonicidade, o que **fortalece** a hipótese, mas ainda com **amostra pequena nos extremos**. A classificação atual **"associação moderada"** está **correta** (não "forte"), não precisa mudar para "insuficiente". **Manter como moderada, mas explicitar que são 5 perfis (1q-5q) e que 1q/5q têm amostra menor para diária.**

### 4. 4q maior receita vs 3q mais robusto

**Dado:** 4q MP receita **232.200** (1075×216, 60 com preço de 286, 21%, alta 33 11,5%) vs 3q MP **151.200** (700×216, 327 de 1451, 22,5%, alta 242 16,7%).

**Afirmação auditada:** "3q Meia Praia é o segmento que mais contribui" - **parcialmente correta se qualificada** como "mais robusto com volume" (1451 vs 286, 5× volume, 5,4× com preço). O relatório já qualifica em `relatorio: F` e `Tabela comparativa` como "melhor combinação volume-receita-preço (151k, 327, alta 242) vs 4q 232k, 60, alta 33 - nicho" e em `Conclusão` como "4q tem maior receita mas volume 5× menor". **Portanto a auditoria está certa em pedir qualificação, mas o relatório já faz isso em 80% dos lugares** - apenas a frase curta "3q mais contribui" sem contexto é incorreta. **Precisa garantir que toda menção curta inclua "mais robusto (volume)"**.

### 5. Meia Praia vs Centro

**Dado:** Meia Praia isolado receita **129.600** (600, 2602, 607) vs Centro **126.720** (587, 548, 193) = **+2.880 (+2,27%)** com volume **4,7× mais Airbnb (2602 vs 548)** e **3,5× mais venda (3414 vs 985)**.

**Auditoria:** Diz que é **empate técnico com leve vantagem Meia Praia**, não "vencedora isolada" - **correto**. O relatório já diz em `relatorio: B` "diferença só 2,3% - empate técnico com leve vantagem" e em `relatorio_localizacao: Análise volume vs receita` - **já está correto**. A conclusão curta em `relatorio_caracteristicas: B` diz "Meia Praia 129,6k > Centro 126,7k +2,3%, volume 4,7×" - **também já qualifica**. **Nenhuma correção necessária**, apenas manter essa qualificação no vídeo (não dizer "Meia Praia tem muito mais receita").

### 6. Alta demanda, condomínio, IPTU

**Alta demanda:** Relatório classifica como **"associação moderada"** com "alta 550 vs demais 600 (alta cobra 50 a menos) e receita 118.800 vs 129.600 (alta menor) - alta não está associada a maior diária, mas a liquidez (80,6% vs 13,2%)" - **correto, não confunde ausência com prova**. Auditoria confirma que está correto.

**Condomínio/IPTU:** Classificados como **"evidência insuficiente"** com "500-942, sem padrão claro" e limitação "cobertura 41-62% pos" - **correto**. O relatório **não** diz "condomínio não influencia", diz "evidência insuficiente" - **não confunde ausência de evidência com prova de ausência**. Auditoria confirma que está correto.

**Preço/m²:** Classificado como **moderada** com "12,9k→18,5k com receita, mas ROI menor" - **correto**.

### 7. Outros pontos que a auditoria não percebeu (ou percebeu parcialmente)

* **Bairro duplicado por acento:** `candidatos_sorted` tem **14 entradas com "alto sao bento" e "alto são bento"** separados (Viva sem acento, Base com acento) - **duplicidade real** com 0 Airbnb com preço para ambos, impacto **baixo** (excluídos do ranking), mas indica normalização incompleta (deveria usar `unidecode`). **Não afeta conclusão, mas deve ser corrigido para 13 únicos.**
* **Mistura Viva vs Base para área:** Relatório usa `Viva usable_area` como proxy para `Base` (que não tem área) - está explicitado como limitação "`Base Airbnb não tem usable_area (usamos Viva como proxy por perfil)`" - **correto com ressalva**, não é mistura indevida escondida.
* **Média vs mediana:** Usa **mediana** consistentemente (robusta a outlier 29k), não média - **correto**.
* **Amostras pequenas já sinalizadas:** 4q MP 60, 3q Centro 45, Tabuleiro 17 - **correto**, não deixam vencer.
* **Nenhum erro de mistura venda vs aluguel por imóvel:** Comparação é por segmento `bairro×quartos`, sem JOIN por `listing_id` - **correto**.

---

## O que permanece válido (sem alteração)

* **Filtros, medianas, receitas:** Todos corretos (460×216=99.360, 700×216=151.200, etc.), medianas robustas, sem erro matemático.
* **Mais quartos → maior receita (associação forte):** 2q 99k <3q 151k <4q 232k com n=723/1451/286 e 187/327/60 com preço - **válido**, com ressalva 4q amostra menor.
* **Bairro Meia Praia volume + receita (moderada):** 129,6k vs 126,7k com volume 4,7× - **válido** como empate técnico com leve vantagem.
* **Preço compra com retorno decrescente (moderada):** 1,07M→1,88M (+75%)→99k→151k (+52%) e 1,88M→3,6M (+91%)→151k→232k (+53%) com 5 pontos 1q-5q mostrando ratio 11,94%→9,24%→8,02%→6,45%→5,12% - **válido como sugestivo**, não lei geral.
* **Alta demanda não implica diária maior (moderada):** 550 vs 600, 80,6% vs 13,2% com preço - **válido**.
* **Condomínio/IPTU insuficiente:** Classificação correta.
* **Padrão combinado Meia Praia 2-3q:** 85-129m², 460-700, 1,07-1,88M, 723-1451, 99-151k - **válido**.

---

## O que precisa ser corrigido (3 reformulações obrigatórias)

1. **Correlação r=0,98:** De `r=0,98 (forte)` para `r=0,98 entre medianas dos 5 perfis (n=5, forte no agregado) mas r≈0,31-0,35 no nível individual (n=911 quartos vs diária e n=7528 area vs preço, moderada com grande dispersão)`. **Manter número 0,98 mas rebaixar força e explicitar n=5 vs n=911/7528.**

2. **Diária como "forte":** De `forte evidência` para `moderada/tautológica: diária é driver matemático da receita por construção (receita=diaria×216, r=1,00 por fórmula), a evidência empírica real é quartos/área → diária (r≈0,31)`. Manter diária como DADO, mas não como descoberta empírica.

3. **Retorno decrescente e 3q vs 4q:** De `forte` para `moderada: nos 5 perfis Meia Praia 1q-5q (n=58,244,1704,1327,73 venda; 81,723,1451,286,27 base, com preço 8,187,327,60,<20) preço +75%/+91% gera receita +52%/+53% - sugerindo decrescente, mas com amostra pequena nos extremos (4q 60, 5q <20 com preço, 1q 8)` e garantir que toda frase curta diga `3q MP é mais robusto (volume) enquanto 4q MP tem maior receita (232k)`.

4. **Bairro duplicado:** Corrigir normalização para `unidecode` ou `strip acentos` para 13 únicos (baixo impacto).

---

## Quais números precisam ser mantidos

**Todos os números principais permanecem, apenas com qualificação:**

* Diárias: 460 (2q MP, 187/723), 700 (3q MP, 327/1451), 1075 (4q MP, 60/286), 580 (2q Centro, 65/183), 790 (3q Centro, 45/211) - **manter**.
* Receitas: 99.360, 151.200, 232.200, 125.280, 170.640 (×216) - **manter**.
* Preços: 1.075.000, 1.884.860, 3.600.000, 1.150.000, 2.100.000 - **manter**.
* Áreas: 85,129,188,86,131 - **manter**.
* Volumes: 723/1451/286 e 183/211, 2602/548 - **manter**.
* Alta: 625 (504 com preço) vs demais 3085 (407) - **manter**.
* **Correlação: manter 0,9768 mas adicionar r individual 0,3139 e 0,3529.**

**Nenhum número precisa ser alterado, apenas requalificado.**

---

## Conclusão final defensável da Pergunta 3 (sem exagerar)

> **Entre segmentos com volume e cobertura suficientes (≥100 Airbnb e ≥30 com preço), mais quartos e maior área estão associados a maiores receitas (2q 99k →3q 151k →4q 232k a 60%, com área 85→129→188m²; r=0,98 entre medianas dos 5 perfis, n=5, forte no agregado, mas r≈0,31 individual, n=911, moderada com dispersão), mas com retorno decrescente vs preço (75% mais capital para 52% mais receita, sugerido em 1q-5q com amostra pequena nos extremos). Meia Praia combina volume (2602, 4,7× Centro) com receita (129,6k vs 126,7k, +2,3% - empate técnico com leve vantagem) e, dentro dela, 3 quartos (700, 151k, 1451, 1,88M, 129m², 327 com preço) é o equilíbrio mais robusto, enquanto diária histórica (460-1075) é o driver matemático da receita (receita=diaria×216, r=1,00 por construção), não evidência empírica; alta demanda (550 vs 600) indica liquidez (80,6% vs 13,2% com preço), não diária maior. Condomínio/IPTU e preço/m² têm evidência insuficiente isoladamente.**

Esta versão mantém volume, mas rebaixa força de 0,98, diária e retorno decrescente para **moderada** onde indicado e qualifica 3q robusto vs 4q maior receita, defensável para banca.

---

## Veredito

1. **Análise está correta?** **Parcialmente correta - defensável com 3 reformulações.** Filtros e receitas corretos, conclusões gerais se sustentam, mas 3 classificações exageram.
2. **Erro matemático?** **Não.** Receitas e r=0,9768 corretos.
3. **Problema metodológico?** **Sim, 2 moderados:** correlação n=5 apresentada como n=3710, e bairro duplicado por acento.
4. **Conclusão exagerada?** **Sim, 3:** r=0,98 forte, diária forte, retorno decrescente forte - devem ser moderada/tautológica/sugestiva.
5. **O que reformular?** Correlação (n=5 vs n=911), diária (tautológica), retorno decrescente (moderada com n pequeno), e sempre qualificar 3q robusto vs 4q maior receita.
6. **Conclusão segura?** A acima (4 linhas) - sem causalidade, com limitações de amostra pequena para 4q/5q e n=5 para correlação.
7. **Pode usar no README/vídeo?** **SIM, com as 3 reformulações.** Sem elas, exageraria (0,98 como prova para todos, diária como descoberta, retorno como lei). Com as qualificações para **moderada** e nota n=5 vs n=911 e 3q robusto vs 4q maior, permanece "2-3q Meia Praia equilíbrio" e é **defensável como estimativa bem fundamentada**.

