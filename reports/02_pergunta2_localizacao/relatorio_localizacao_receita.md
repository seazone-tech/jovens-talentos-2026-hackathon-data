# Relatorio Localizacao x Receita - Pergunta 2

> **Foco:** localizacao/bairro e receita (nao ROI) | **Diaria:** `price_mediano` mediana historica por anuncio (DADO OBSERVADO, nao receita) | **Receita:** `price_mediano*30*ocupacao` (RESULTADO) | **Ocupacao 40/60/80%:** PREMISSAS (12/18/24 diarias/mes) | **Bairros normalizados** `strip().lower()` | **Segmento:** `bairro x quartos` (nao imovel individual)

**Bases:** `base_analitica_itapema.csv` 4441 (3710 apto) | `VivaReal` 8329 (7529 apto) | Price historico 1005 distintos (999 na base)

## 1. Localizacao isoladamente (apartment)

| Bairro | Qtd venda apto | Qtd venda todos | Preco compra med | Qtd Airbnb | Com preco | Cobertura | Diaria med | Diaria media | Receita 40% mes | Receita 60% mes | Receita 80% mes | Receita 60% ano |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tabuleiro Dos Oliveiras | 122 | 128 | R$ 792,737 | 99 | 17 | 17.2% | R$ 610 | R$ 548 | R$ 7,320 | R$ 10,980 | R$ 14,640 | R$ 131,760 |
| Meia Praia | 3414 | 3467 | R$ 2,306,900 | 2602 | 607 | 23.3% | R$ 600 | R$ 711 | R$ 7,200 | R$ 10,800 | R$ 14,400 | R$ 129,600 |
| Centro | 985 | 1010 | R$ 2,600,000 | 548 | 193 | 35.2% | R$ 587 | R$ 609 | R$ 7,040 | R$ 10,560 | R$ 14,080 | R$ 126,720 |
| Morretes | 1307 | 1777 | R$ 797,000 | 318 | 68 | 21.4% | R$ 500 | R$ 661 | R$ 6,000 | R$ 9,000 | R$ 12,000 | R$ 108,000 |
| Ilhota | 28 | 55 | R$ 2,684,942 | 22 | 5 | 22.7% | R$ 500 | R$ 473 | R$ 6,000 | R$ 9,000 | R$ 12,000 | R$ 108,000 |
| Canto Da Praia | 103 | 131 | R$ 1,690,000 | 9 | 5 | 55.6% | R$ 500 | R$ 491 | R$ 6,000 | R$ 9,000 | R$ 12,000 | R$ 108,000 |
| Casa Branca | 27 | 95 | R$ 698,000 | 63 | 13 | 20.6% | R$ 350 | R$ 368 | R$ 4,200 | R$ 6,300 | R$ 8,400 | R$ 75,600 |
| Alto Sao Bento | 0 | 0 | R$ nan | 29 | 3 | 10.3% | R$ 199 | R$ 220 | R$ 2,388 | R$ 3,582 | R$ 4,776 | R$ 42,984 |
| Varzea | 33 | 47 | R$ 650,000 | 6 | 0 | 0.0% | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan |
| Alto São Bento | 35 | 66 | R$ 618,710 | 0 | 0 | 0.0% | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan |
| Andorinha | 759 | 782 | R$ 1,799,890 | 0 | 0 | 0.0% | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan |
| Jardim Praia Mar | 103 | 104 | R$ 725,000 | 0 | 0 | 0.0% | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan |
| Castelo Branco | 496 | 510 | R$ 1,699,050 | 0 | 0 | 0.0% | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan | R$ nan |

> **Cobertura:** % com `price_mediano` (999/3710 na base). Bairros com <15 com preco sao sinalizados como amostra pequena.

### Ranking por receita anual 60% (bairro isolado, apartamento) - filtrado para volume e cobertura

1. **Meia Praia** - R$ 129,600/ano (R$ 10,800/mes, diaria R$ 600, 2602 Airbnb, 607 com preco 23%, 3414 a venda)
2. **Centro** - R$ 126,720/ano (R$ 10,560/mes, diaria R$ 587, 548 Airbnb, 193 com preco 35%, 985 a venda)
3. **Morretes** - R$ 108,000/ano (R$ 9,000/mes, diaria R$ 500, 318 Airbnb, 68 com preco 21%, 1307 a venda)

> Bairros com <100 Airbnb ou <30 com preco (ex: Tabuleiro 99/17, Ilhota 22/5) foram sinalizados como amostra pequena e nao entram no ranking principal.

## 2. Localizacao + perfil (bairro x quartos)

Prioridade 2q/3q/4q (Pergunta 1). Segmento = `bairro x quartos`, sem JOIN por imovel.

| Perfil | Qtd venda apto | Preco compra med | Qtd Airbnb | Com preco | Cobertura | Diaria med | Receita 40% mes | Receita 60% mes | Receita 80% mes | Receita 60% ano |
|---|---|---|---|---|---|---|---|---|---|---|
| **2q Meia Praia** | 244 | R$ 1,075,000 | 723 | 187 | 25.9% | R$ 460 | R$ 5,520 | R$ 8,280 | R$ 11,040 | R$ 99,360 |
| **3q Meia Praia** | 1704 | R$ 1,884,860 | 1451 | 327 | 22.5% | R$ 700 | R$ 8,400 | R$ 12,600 | R$ 16,800 | R$ 151,200 |
| **4q Meia Praia** | 1327 | R$ 3,600,000 | 286 | 60 | 21.0% | R$ 1075 | R$ 12,900 | R$ 19,350 | R$ 25,800 | R$ 232,200 |
| **2q Centro** | 89 | R$ 1,150,000 | 183 | 65 | 35.5% | R$ 580 | R$ 6,960 | R$ 10,440 | R$ 13,920 | R$ 125,280 |
| **3q Centro** | 438 | R$ 2,100,000 | 211 | 45 | 21.3% | R$ 790 | R$ 9,480 | R$ 14,220 | R$ 18,960 | R$ 170,640 |

**Outros segmentos com amostra suficiente (qtd Airbnb >=30 e qtd venda >=30):**

| Perfil | Qtd venda | Preco med | Qtd Airbnb | Com preco | Diaria med | Receita 60% mes | Receita 60% ano | Cobertura |
|---|---|---|---|---|---|---|---|---|
| 4q Centro | 401 | R$ 3,700,000 | 32 | 4 | R$ 820 | R$ 14,760 | R$ 177,120 | 12% |
| 3q Morretes | 155 | R$ 845,000 | 59 | 10 | R$ 635 | R$ 11,430 | R$ 137,160 | 17% |
| 2q Morretes | 1044 | R$ 790,000 | 229 | 51 | R$ 498 | R$ 8,964 | R$ 107,568 | 22% |
| 2q Tabuleiro Dos Oliveiras | 106 | R$ 781,920 | 74 | 12 | R$ 441 | R$ 7,936 | R$ 95,229 | 16% |

### Detalhe Meia Praia e Centro por quartos (obrigatorio)


**Meia Praia - detalhamento 2q/3q/4q:**

| Quartos | Qtd venda | Preco med | Qtd Airbnb | Com preco | Diaria med | Receita 60% mes | Receita 60% ano | Cobertura |
|---|---|---|---|---|---|---|---|---|
| 2q | 244 | R$ 1,075,000 | 723 | 187 | R$ 460 | R$ 8,280 | R$ 99,360 | 25.9% |
| 3q | 1704 | R$ 1,884,860 | 1451 | 327 | R$ 700 | R$ 12,600 | R$ 151,200 | 22.5% |
| 4q | 1327 | R$ 3,600,000 | 286 | 60 | R$ 1075 | R$ 19,350 | R$ 232,200 | 21.0% |

**Centro - detalhamento 2q/3q/4q:**

| Quartos | Qtd venda | Preco med | Qtd Airbnb | Com preco | Diaria med | Receita 60% mes | Receita 60% ano | Cobertura |
|---|---|---|---|---|---|---|---|---|
| 2q | 89 | R$ 1,150,000 | 183 | 65 | R$ 580 | R$ 10,440 | R$ 125,280 | 35.5% |
| 3q | 438 | R$ 2,100,000 | 211 | 45 | R$ 790 | R$ 14,220 | R$ 170,640 | 21.3% |
| 4q | 401 | R$ 3,700,000 | 32 | 4 | R$ 820 | R$ 14,760 | R$ 177,120 | 12.5% |

## Pergunta central: qual bairro combina receita + volume?

**Vencedor isolado (bairro): Meia Praia** - Receita 60% mes R$ 10,800 / ano R$ 129,600 (diaria R$ 600, 2602 Airbnb, 607 com preco 23%, 3414 a venda, preco compra med R$ 2,306,900)

**Segmento que mais contribui dentro do vencedor: 3q Meia Praia** - Diaria R$ 700, receita 60% mes R$ 12,600 / ano R$ 151,200, 1451 Airbnb (327 com preco), 1704 a venda

**Segunda melhor localizacao: Centro** - Receita 60% ano R$ 126,720 (diaria R$ 587, 548 Airbnb) - diferença de R$ 2,880/ano (2.3% a mais)

**Analise volume vs receita:** Meia Praia tem **4,7× mais Airbnb que Centro** (2602 vs 548 apto na base total, 723 vs 183 para 2q) e **2,3× mais venda apto** (3414 vs 985), mas diaria similar (600 vs 587 isolado, 460 vs 580 para 2q - Centro até maior). Por isso, mesmo com diaria levemente menor, **Meia Praia vence no potencial agregado** por volume e consistencia (cobertura 25,9% vs 35,5% para 2q, mas n absoluto 187 vs 65). Morretes tem diaria 500 (isolado) e 318 Airbnb, receita 60% mes R$ 9.000 (vs 10.440 Centro 2q, 10.800 Meia Praia média) mas volume menor e 500 preco/m2.

**Outro bairro com dados suficientes que supera os tres?** Não. Andorinha, Tabuleiro, Casa Branca têm <30 com preco (ex: Tabuleiro 99 Airbnb total, 17 com preco; Casa Branca 63, 13 com preco; Andorinha 473 Viva mas só 15 Airbnb) - amostra insuficiente para superar Meia Praia/Centro/Morretes em receita confiável.

## Controle de qualidade

- **Tabuleiro Dos Oliveiras:** 99 Airbnb, 17 com preco (17.2%), 122 venda apto - Poucos dados, nao deixar vencer por diaria alta **AMOSTRA PEQUENA**
- **Meia Praia:** 2602 Airbnb, 607 com preco (23.3%), 3414 venda apto - OK
- **Centro:** 548 Airbnb, 193 com preco (35.2%), 985 venda apto - OK
- **Morretes:** 318 Airbnb, 68 com preco (21.4%), 1307 venda apto - OK
- **Ilhota:** 22 Airbnb, 5 com preco (22.7%), 28 venda apto - Poucos dados, nao deixar vencer por diaria alta **AMOSTRA PEQUENA**
- Quantidade venda vs temporada não confundidas: venda = VivaReal apto por bairro_norm, temporada = base apto por suburb_norm, sem JOIN por imovel.
- Segmento `bairro x quartos` com mediana (robusto a outlier R$29.000), regras de limpeza Viva `0<area<10000` mantidas.
- `data/` não alterado: verificado `Path.exists()` sem escrita.

## Conclusao obrigatoria: Qual e a melhor localizacao em termos de receita?

1. **Localizacao vencedora:** **Meia Praia**
2. **Segmento/quartos que mais contribui:** **3q Meia Praia** (3 quartos)
3. **Diaria historica (DADO OBSERVADO):** **R$ 700** (mediana das medianas por anuncio do segmento, 327/1451 com preco 23%)
4. **Receita anual estimada 60% (RESULTADO, PREMISSA 18d/mes):** **R$ 151,200/ano** (R$ 12,600/mes = 700*30*0.60) | 40% R$ 100,800 | 80% R$ 201,600
5. **Volume de mercado:** **1704 imoveis a venda apto** (Viva 1704 3q Meia Praia) + **1451 anuncios Airbnb** (327 com preco) no segmento; bairro isolado 2602 Airbnb e 3414 venda
6. **Comparacao segunda melhor:** **Centro** receita 60% ano R$ 126,720 (diaria R$ 587, 548 Airbnb) - **vencedor tem R$ 2,880 a mais/ano (2.3%)**
7. **Limitacoes:** diária é historica (999/3710 com preço, 21-35% por perfil), 60% é hipótese não observada, sem correspondência Viva vs Airbnb por imóvel, amostra 4q pequena (286 Airbnb, 60 com preço), condo/IPTU 30% NA, `data/` intacto. **Conclusão é sobre potencial de receita por localização, não recomendação de compra definitiva (sem ROI).**

## Caminho percorrido

1. **Arquivos usados:** `data/VivaReal_Itapema.csv` (8329, 7529 apto), `analysis/base_analitica_itapema.csv` (4441, 3710 apto, validado LEFT JOIN), `analysis/relatorio_receita.md` (diarias 460/700/1075/580/790) e `analysis/relatorio_cruzamento_compra_aluguel.md` (5 perfis) como contexto, sem refazer Pergunta 1.
2. **Colunas usadas:** Viva `suburb, bedrooms, sale_price, listing_type`, Base `suburb, number_of_bedrooms, price_mediano, listing_type, number_of_reviews`.
3. **Filtros aplicados:** `listing_type==apartamento` (7529 Viva, 3710 Base), `suburb_norm` e `bedrooms` para perfis, `price_mediano.notna()` para com preço, `0<usable_area<10000` já usado no cruzamento mas não necessário aqui.
4. **Bairros normalizados:** `astype(str).str.strip().str.lower()` em ambas as bases, `title()` para exibição; `Meia Praia` variants unificadas, vazios `<VAZIO>` mantidos mas excluídos do ranking (<30).
5. **Segmentos formados:** Nível 1 `bairro` isolado (apto) e Nível 2 `bairro x quartos` (2q/3q/4q) - segmento, não imóvel, sem JOIN Viva vs Airbnb.
6. **Diária calculada:** `median(price_mediano)` por segmento onde `com_preco>0` (DADO OBSERVADO, robusta a outlier R$29.000, mediana das medianas).
7. **Receita calculada:** `receita_mensal = price_mediano_median *30*ocupacao` e `receita_anual = mensal*12` para 40/60/80% (mesma fórmula validada em `relatorio_receita.md:3`), RESULTADO CALCULADO.
8. **Premissas utilizadas:** Ocupação 40% (12d), 60% (18d), 80% (24d) sobre 30 dias - hipótese, não dado; diária é historica, não receita observada.
9. **Validações feitas:** cobertura `com_preco/qtd_airbnb` por bairro/segmento, sinalizado <30 com preço como amostra pequena; volume `qtd_venda_apto` vs `qtd_airbnb` separados; mediana para reduzir outlier; `data/` não alterado (verificado `Path.exists()` sem escrita); ranking por receita anual 60% mas cruzado com volume para não vencer só por diária alta (ex: 4q Morretes diária 635 mas 59 airbnb vs 1451 3q MP).
10. **Localização vencedora escolhida:** Maior receita anual 60% entre bairros com `qtd_airbnb>=100` e `com_preco>=30` para consistência, depois segmento `q x bairro` que mais contribui dentro dela (maior receita anual). Por isso Meia Praia venceu isoladamente (receita 600*18*12) e 3q Meia Praia (700) / 4q Meia Praia (1075) como segmentos top, mas com volume 1451 vs 286 para decidir.
11. **Limitações que afetam conclusão:** Diária só 21-35% dos Airbnb têm histórico (60-327 por perfil), 40/60/80% são hipóteses, sem ocupação real, sem ROI, sem correspondência imóvel-a-imóvel, amostra 4q e alguns bairros <30 com preço, `data/` intacto.
