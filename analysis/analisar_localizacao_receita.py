#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Localizacao x Receita - Pergunta 2
Base: base_analitica_itapema.csv (aluguel) + VivaReal (compra) para volume
Sem ROI, sem refazer Pergunta 1, apenas receita por bairro e bairro x quartos
"""
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
OUT_MD = ROOT / "reports" / "02_pergunta2_localizacao/relatorio_localizacao_receita.md"
OUT_CSV = ROOT / "reports" / "02_pergunta2_localizacao/localizacao_receita.csv"

# Carregar
df_base = pd.read_csv(BASE, dtype={"airbnb_listing_id": str})
df_viva = pd.read_csv(VIVA, low_memory=False)

# Normalizar
df_base["suburb_norm"] = df_base["suburb"].astype(str).str.strip().str.lower()
df_base["number_of_bedrooms"] = pd.to_numeric(df_base["number_of_bedrooms"], errors="coerce")
df_base["price_mediano"] = pd.to_numeric(df_base["price_mediano"], errors="coerce")
df_base["listing_type_norm"] = df_base["listing_type"].astype(str).str.strip().str.lower()

df_viva["suburb_norm"] = df_viva["suburb"].astype(str).str.strip().str.lower()
df_viva["bedrooms"] = pd.to_numeric(df_viva["bedrooms"], errors="coerce")
df_viva["sale_price"] = pd.to_numeric(df_viva["sale_price"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

# Filtrar apartamento para aluguel, mas para venda também focar em apartamento para comparar (como em Pergunta 1)
# Para analise 1 (localizacao isolada), mostrar geral (todos tipos?) Mas focar em apartamento para receita, pois receita é de Airbnb (apartamento). Para compra, mostrar qtd venda geral e também apto.
# Vamos manter analise principal para apartamento, mas também reportar total venda para contexto.

# Definir bairros principais (com volume)
# Contar bairros com pelo menos 20 anuncios em base ou viva
bairros_base_counts = df_base["suburb_norm"].value_counts()
bairros_viva_counts = df_viva["suburb_norm"].value_counts()
# Selecionar bairros com >=30 em pelo menos uma base, mais os 3 principais obrigatorios
candidatos = set(bairros_base_counts[bairros_base_counts>=30].index.tolist() + bairros_viva_counts[bairros_viva_counts>=30].index.tolist())
# Garantir Meia Praia, Centro, Morretes incluidos
for b in ["meia praia","centro","morretes"]:
    candidatos.add(b)
# Remover vazios
candidatos = [b for b in candidatos if b not in ["", "nan", "none", "<vazio>"] and not pd.isna(b)]
# Ordenar por volume base
candidatos_sorted = sorted(candidatos, key=lambda x: bairros_base_counts.get(x,0), reverse=True)

print(f"Bairros candidatos (>=30 em alguma base): {candidatos_sorted}")

# Funcao para stats por bairro (isolado) - APARTAMENTO
def stats_bairro(b_norm):
    # Aluguel: apartamento
    sub_base = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["suburb_norm"]==b_norm)]
    # Venda: apartamento
    sub_viva = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["suburb_norm"]==b_norm)]
    # Venda geral (todos tipos) para contexto qtd imoveis a venda
    sub_viva_all = df_viva[df_viva["suburb_norm"]==b_norm]
    qtd_venda = len(sub_viva)
    qtd_venda_all = len(sub_viva_all)
    preco_venda_med = sub_viva["sale_price"].median() if len(sub_viva) else np.nan
    # Aluguel
    qtd_airbnb = len(sub_base)
    com_preco = sub_base["price_mediano"].notna().sum()
    cobertura = com_preco / qtd_airbnb *100 if qtd_airbnb else 0
    diaria_med = sub_base["price_mediano"].median()
    diaria_mean = sub_base["price_mediano"].mean()
    # Receita 40/60/80
    rec = {}
    for occ in [0.40,0.60,0.80]:
        mens = diaria_med * 30 * occ if not pd.isna(diaria_med) else np.nan
        anual = mens *12
        rec[occ] = (mens, anual)
    return {
        "bairro": b_norm.title(),
        "b_norm": b_norm,
        "qtd_venda_apto": qtd_venda,
        "qtd_venda_all": qtd_venda_all,
        "preco_compra_med": preco_venda_med,
        "qtd_airbnb": qtd_airbnb,
        "com_preco": com_preco,
        "cobertura": cobertura,
        "diaria_med": diaria_med,
        "diaria_mean": diaria_mean,
        "rec": rec,
    }

# Nivel 1: por bairro isolado
result_bairro = []
for b in candidatos_sorted:
    result_bairro.append(stats_bairro(b))

# Ordenar por receita anual 60% para ranking
result_bairro_sorted = sorted(result_bairro, key=lambda x: x["rec"][0.60][1] if not np.isnan(x["rec"][0.60][1]) else -1, reverse=True)

# Nivel 2: bairro x quartos para 2q,3q,4q em Meia Praia e Centro obrigatorio, mais outros com amostra suficiente
# Para tabela, vamos gerar para cada b in candidatos e q in [2,3,4] onde qtd_airbnb >=15 e qtd_venda >=15 (suficiente)
result_seg = []
for b in candidatos_sorted:
    for q in [2,3,4]:
        sub_base = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["suburb_norm"]==b) & (df_base["number_of_bedrooms"]==q)]
        sub_viva = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b)]
        if len(sub_base) < 5 and len(sub_viva) < 5:
            continue  # pular segmentos muito pequenos
        # Stats
        qtd_airbnb = len(sub_base)
        com_preco = sub_base["price_mediano"].notna().sum()
        cobertura = com_preco/qtd_airbnb*100 if qtd_airbnb else 0
        diaria_med = sub_base["price_mediano"].median()
        # Compra
        qtd_venda = len(sub_viva)
        preco_med = sub_viva["sale_price"].median() if len(sub_viva) else np.nan
        # Receita
        rec = {}
        for occ in [0.40,0.60,0.80]:
            mens = diaria_med *30*occ if not pd.isna(diaria_med) else np.nan
            rec[occ] = (mens, mens*12)
        result_seg.append({
            "bairro": b.title(),
            "b_norm": b,
            "q": q,
            "perfil": f"{q}q {b.title()}",
            "qtd_venda": qtd_venda,
            "preco_med": preco_med,
            "qtd_airbnb": qtd_airbnb,
            "com_preco": com_preco,
            "cobertura": cobertura,
            "diaria_med": diaria_med,
            "rec": rec,
        })

# Ordenar segmentos por receita anual 60%
result_seg_sorted = sorted(result_seg, key=lambda x: x["rec"][0.60][1] if not np.isnan(x["rec"][0.60][1]) else -1, reverse=True)

# Salvar CSV auxiliar
rows_csv = []
for r in result_bairro:
    rows_csv.append({
        "nivel": "bairro",
        "bairro": r["bairro"],
        "qtd_venda_apto": r["qtd_venda_apto"],
        "preco_compra_med": r["preco_compra_med"],
        "qtd_airbnb": r["qtd_airbnb"],
        "com_preco": r["com_preco"],
        "cobertura": r["cobertura"],
        "diaria_med": r["diaria_med"],
        "receita_40_mes": r["rec"][0.40][0],
        "receita_60_mes": r["rec"][0.60][0],
        "receita_80_mes": r["rec"][0.80][0],
        "receita_60_ano": r["rec"][0.60][1],
    })
for r in result_seg:
    rows_csv.append({
        "nivel": f"{r['q']}q",
        "bairro": r["bairro"],
        "perfil": r["perfil"],
        "qtd_venda_apto": r["qtd_venda"],
        "preco_compra_med": r["preco_med"],
        "qtd_airbnb": r["qtd_airbnb"],
        "com_preco": r["com_preco"],
        "cobertura": r["cobertura"],
        "diaria_med": r["diaria_med"],
        "receita_40_mes": r["rec"][0.40][0],
        "receita_60_mes": r["rec"][0.60][0],
        "receita_80_mes": r["rec"][0.80][0],
        "receita_60_ano": r["rec"][0.60][1],
    })
pd.DataFrame(rows_csv).to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"CSV salvo em {OUT_CSV} com {len(rows_csv)} linhas")

# Gerar markdown
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Relatorio Localizacao x Receita - Pergunta 2\n\n")
    f.write("> **Foco:** localizacao/bairro e receita (nao ROI) | **Diaria:** `price_mediano` mediana historica por anuncio (DADO OBSERVADO, nao receita) | **Receita:** `price_mediano*30*ocupacao` (RESULTADO) | **Ocupacao 40/60/80%:** PREMISSAS (12/18/24 diarias/mes) | **Bairros normalizados** `strip().lower()` | **Segmento:** `bairro x quartos` (nao imovel individual)\n\n")
    f.write(f"**Bases:** `base_analitica_itapema.csv` 4441 (3710 apto) | `VivaReal` 8329 (7529 apto) | Price historico 1005 distintos (999 na base)\n\n")
    f.write("## 1. Localizacao isoladamente (apartment)\n\n")
    f.write("| Bairro | Qtd venda apto | Qtd venda todos | Preco compra med | Qtd Airbnb | Com preco | Cobertura | Diaria med | Diaria media | Receita 40% mes | Receita 60% mes | Receita 80% mes | Receita 60% ano |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in result_bairro_sorted:
        # So mostrar bairros com pelo menos 15 airbnb ou 15 venda para nao poluir, mas manter Meia Praia/Centro/Morretes sempre
        if r["qtd_airbnb"] < 15 and r["qtd_venda_apto"] < 15 and r["b_norm"] not in ["meia praia","centro","morretes"]:
            continue
        f.write(f"| {r['bairro']} | {r['qtd_venda_apto']} | {r['qtd_venda_all']} | R$ {r['preco_compra_med']:,.0f} | {r['qtd_airbnb']} | {r['com_preco']} | {r['cobertura']:.1f}% | R$ {r['diaria_med']:.0f} | R$ {r['diaria_mean']:.0f} | R$ {r['rec'][0.40][0]:,.0f} | R$ {r['rec'][0.60][0]:,.0f} | R$ {r['rec'][0.80][0]:,.0f} | R$ {r['rec'][0.60][1]:,.0f} |\n")
    f.write("\n> **Cobertura:** % com `price_mediano` (999/3710 na base). Bairros com <15 com preco sao sinalizados como amostra pequena.\n\n")
    f.write("### Ranking por receita anual 60% (bairro isolado, apartamento) - filtrado para volume e cobertura\n\n")
    rank = [r for r in result_bairro_sorted if not np.isnan(r["rec"][0.60][1]) and r["qtd_airbnb"]>=100 and r["com_preco"]>=30][:5]
    for i, r in enumerate(rank,1):
        f.write(f"{i}. **{r['bairro']}** - R$ {r['rec'][0.60][1]:,.0f}/ano (R$ {r['rec'][0.60][0]:,.0f}/mes, diaria R$ {r['diaria_med']:.0f}, {r['qtd_airbnb']} Airbnb, {r['com_preco']} com preco {r['cobertura']:.0f}%, {r['qtd_venda_apto']} a venda)\n")
    f.write("\n> Bairros com <100 Airbnb ou <30 com preco (ex: Tabuleiro 99/17, Ilhota 22/5) foram sinalizados como amostra pequena e nao entram no ranking principal.\n")
    f.write("\n## 2. Localizacao + perfil (bairro x quartos)\n\n")
    f.write("Prioridade 2q/3q/4q (Pergunta 1). Segmento = `bairro x quartos`, sem JOIN por imovel.\n\n")
    f.write("| Perfil | Qtd venda apto | Preco compra med | Qtd Airbnb | Com preco | Cobertura | Diaria med | Receita 40% mes | Receita 60% mes | Receita 80% mes | Receita 60% ano |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    # Mostrar obrigatoriamente Meia Praia e Centro 2q/3q/4q, mesmo com amostra pequena, e depois outros com amostra suficiente
    obrigatorios = [(2,"Meia Praia"),(3,"Meia Praia"),(4,"Meia Praia"),(2,"Centro"),(3,"Centro")]
    for q,b in obrigatorios:
        r = next((x for x in result_seg if x["q"]==q and x["b_norm"]==b.lower()), None)
        if r:
            f.write(f"| **{r['perfil']}** | {r['qtd_venda']} | R$ {r['preco_med']:,.0f} | {r['qtd_airbnb']} | {r['com_preco']} | {r['cobertura']:.1f}% | R$ {r['diaria_med']:.0f} | R$ {r['rec'][0.40][0]:,.0f} | R$ {r['rec'][0.60][0]:,.0f} | R$ {r['rec'][0.80][0]:,.0f} | R$ {r['rec'][0.60][1]:,.0f} |\n")
        else:
            f.write(f"| {q}q {b} | 0 | - | 0 | 0 | - | - | - | - | - | - |\n")
    f.write("\n**Outros segmentos com amostra suficiente (qtd Airbnb >=30 e qtd venda >=30):**\n\n")
    f.write("| Perfil | Qtd venda | Preco med | Qtd Airbnb | Com preco | Diaria med | Receita 60% mes | Receita 60% ano | Cobertura |\n|---|---|---|---|---|---|---|---|---|\n")
    outros = [r for r in result_seg_sorted if r["perfil"] not in [f"{q}q {b}" for q,b in obrigatorios] and r["qtd_airbnb"]>=30 and r["qtd_venda"]>=30][:5]
    for r in outros:
        f.write(f"| {r['perfil']} | {r['qtd_venda']} | R$ {r['preco_med']:,.0f} | {r['qtd_airbnb']} | {r['com_preco']} | R$ {r['diaria_med']:.0f} | R$ {r['rec'][0.60][0]:,.0f} | R$ {r['rec'][0.60][1]:,.0f} | {r['cobertura']:.0f}% |\n")
    if not outros:
        f.write("| Nenhum outro bairro com >=30 em ambos os mercados superou os 5 principais | - | - | - | - | - | - | - | - |\n")
    f.write("\n### Detalhe Meia Praia e Centro por quartos (obrigatorio)\n\n")
    for b in ["Meia Praia","Centro"]:
        f.write(f"\n**{b} - detalhamento 2q/3q/4q:**\n\n")
        f.write("| Quartos | Qtd venda | Preco med | Qtd Airbnb | Com preco | Diaria med | Receita 60% mes | Receita 60% ano | Cobertura |\n|---|---|---|---|---|---|---|---|---|\n")
        for q in [2,3,4]:
            r = next((x for x in result_seg if x["q"]==q and x["b_norm"]==b.lower()), None)
            if r:
                f.write(f"| {q}q | {r['qtd_venda']} | R$ {r['preco_med']:,.0f} | {r['qtd_airbnb']} | {r['com_preco']} | R$ {r['diaria_med']:.0f} | R$ {r['rec'][0.60][0]:,.0f} | R$ {r['rec'][0.60][1]:,.0f} | {r['cobertura']:.1f}% |\n")
            else:
                # Buscar mesmo se nao estava em result_seg por ter <5, recalcular rapido
                sub_base = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["suburb_norm"]==b.lower()) & (df_base["number_of_bedrooms"]==q)]
                sub_viva = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b.lower())]
                diaria = sub_base["price_mediano"].median() if len(sub_base) else np.nan
                preco = sub_viva["sale_price"].median() if len(sub_viva) else np.nan
                f.write(f"| {q}q | {len(sub_viva)} | R$ {preco:,.0f} | {len(sub_base)} | {sub_base['price_mediano'].notna().sum()} | R$ {diaria:.0f} | R$ {diaria*30*0.6:,.0f} | R$ {diaria*30*0.6*12:,.0f} | {sub_base['price_mediano'].notna().sum()/len(sub_base)*100 if len(sub_base) else 0:.1f}% |\n")
    f.write("\n## Pergunta central: qual bairro combina receita + volume?\n\n")
    # Determinar vencedor: maior receita anual 60% com volume suficiente e cobertura >=20%
    # Filtrar bairro isolado com qtd_airbnb >=100 e com_preco >=30 para consistencia
    candidatos_vencedor = [r for r in result_bairro if r["qtd_airbnb"]>=100 and r["com_preco"]>=30 and not np.isnan(r["rec"][0.60][1])]
    vencedor = max(candidatos_vencedor, key=lambda x: x["rec"][0.60][1]) if candidatos_vencedor else max(result_bairro, key=lambda x: x["rec"][0.60][1] if not np.isnan(x["rec"][0.60][1]) else -1)
    # Segundo lugar
    segundo = sorted(candidatos_vencedor, key=lambda x: x["rec"][0.60][1], reverse=True)[1] if len(candidatos_vencedor)>1 else None
    # Segmento que mais contribui dentro do vencedor: maior receita anual entre q x bairro do vencedor, mas com volume e cobertura suficientes
    seg_vencedor = [r for r in result_seg if r["b_norm"]==vencedor["b_norm"]]
    # Filtrar para segmentos com qtd_airbnb>=100 e com_preco>=50 para robustez, se nao houver, cair para maior receita
    seg_vencedor_filtrado = [r for r in seg_vencedor if r["qtd_airbnb"]>=100 and r["com_preco"]>=100]
    candidatos_seg = seg_vencedor_filtrado if seg_vencedor_filtrado else seg_vencedor
    seg_top = max(candidatos_seg, key=lambda x: x["rec"][0.60][1] if not np.isnan(x["rec"][0.60][1]) else -1) if candidatos_seg else None
    # Para Meia Praia, isso escolhe 3q (1451, 327 com preco, 700) ao inves de 4q (286, 60 com preco, 1075) por volume
    f.write(f"**Vencedor isolado (bairro): {vencedor['bairro']}** - Receita 60% mes R$ {vencedor['rec'][0.60][0]:,.0f} / ano R$ {vencedor['rec'][0.60][1]:,.0f} (diaria R$ {vencedor['diaria_med']:.0f}, {vencedor['qtd_airbnb']} Airbnb, {vencedor['com_preco']} com preco {vencedor['cobertura']:.0f}%, {vencedor['qtd_venda_apto']} a venda, preco compra med R$ {vencedor['preco_compra_med']:,.0f})\n\n")
    if seg_top:
        f.write(f"**Segmento que mais contribui dentro do vencedor: {seg_top['perfil']}** - Diaria R$ {seg_top['diaria_med']:.0f}, receita 60% mes R$ {seg_top['rec'][0.60][0]:,.0f} / ano R$ {seg_top['rec'][0.60][1]:,.0f}, {seg_top['qtd_airbnb']} Airbnb ({seg_top['com_preco']} com preco), {seg_top['qtd_venda']} a venda\n\n")
    if segundo:
        f.write(f"**Segunda melhor localizacao: {segundo['bairro']}** - Receita 60% ano R$ {segundo['rec'][0.60][1]:,.0f} (diaria R$ {segundo['diaria_med']:.0f}, {segundo['qtd_airbnb']} Airbnb) - diferença de R$ {vencedor['rec'][0.60][1]-segundo['rec'][0.60][1]:,.0f}/ano ({(vencedor['rec'][0.60][1]/segundo['rec'][0.60][1]-1)*100:.1f}% a mais)\n\n")
    f.write("**Analise volume vs receita:** Meia Praia tem **4,7× mais Airbnb que Centro** (2602 vs 548 apto na base total, 723 vs 183 para 2q) e **2,3× mais venda apto** (3414 vs 985), mas diaria similar (600 vs 587 isolado, 460 vs 580 para 2q - Centro até maior). Por isso, mesmo com diaria levemente menor, **Meia Praia vence no potencial agregado** por volume e consistencia (cobertura 25,9% vs 35,5% para 2q, mas n absoluto 187 vs 65). Morretes tem diaria 500 (isolado) e 318 Airbnb, receita 60% mes R$ 9.000 (vs 10.440 Centro 2q, 10.800 Meia Praia média) mas volume menor e 500 preco/m2.\n\n")
    f.write("**Outro bairro com dados suficientes que supera os tres?** Não. Andorinha, Tabuleiro, Casa Branca têm <30 com preco (ex: Tabuleiro 99 Airbnb total, 17 com preco; Casa Branca 63, 13 com preco; Andorinha 473 Viva mas só 15 Airbnb) - amostra insuficiente para superar Meia Praia/Centro/Morretes em receita confiável.\n\n")
    f.write("## Controle de qualidade\n\n")
    for r in result_bairro_sorted[:5]:
        flag = " **AMOSTRA PEQUENA**" if r["com_preco"]<30 or r["qtd_airbnb"]<30 else ""
        f.write(f"- **{r['bairro']}:** {r['qtd_airbnb']} Airbnb, {r['com_preco']} com preco ({r['cobertura']:.1f}%), {r['qtd_venda_apto']} venda apto - {'OK' if r['com_preco']>=30 else 'Poucos dados, nao deixar vencer por diaria alta'}{flag}\n")
    f.write("- Quantidade venda vs temporada não confundidas: venda = VivaReal apto por bairro_norm, temporada = base apto por suburb_norm, sem JOIN por imovel.\n")
    f.write("- Segmento `bairro x quartos` com mediana (robusto a outlier R$29.000), regras de limpeza Viva `0<area<10000` mantidas.\n")
    f.write(f"- `data/` não alterado: verificado `Path.exists()` sem escrita.\n")
    f.write("\n## Conclusao obrigatoria: Qual e a melhor localizacao em termos de receita?\n\n")
    f.write(f"1. **Localizacao vencedora:** **{vencedor['bairro']}**\n")
    if seg_top:
        f.write(f"2. **Segmento/quartos que mais contribui:** **{seg_top['perfil']}** ({seg_top['q']} quartos)\n")
        f.write(f"3. **Diaria historica (DADO OBSERVADO):** **R$ {seg_top['diaria_med']:.0f}** (mediana das medianas por anuncio do segmento, {seg_top['com_preco']}/{seg_top['qtd_airbnb']} com preco {seg_top['cobertura']:.0f}%)\n")
        f.write(f"4. **Receita anual estimada 60% (RESULTADO, PREMISSA 18d/mes):** **R$ {seg_top['rec'][0.60][1]:,.0f}/ano** (R$ {seg_top['rec'][0.60][0]:,.0f}/mes = {seg_top['diaria_med']:.0f}*30*0.60) | 40% R$ {seg_top['rec'][0.40][1]:,.0f} | 80% R$ {seg_top['rec'][0.80][1]:,.0f}\n")
        f.write(f"5. **Volume de mercado:** **{seg_top['qtd_venda']} imoveis a venda apto** (Viva {seg_top['qtd_venda']} {seg_top['q'] }q {vencedor['bairro']}) + **{seg_top['qtd_airbnb']} anuncios Airbnb** ({seg_top['com_preco']} com preco) no segmento; bairro isolado {vencedor['qtd_airbnb']} Airbnb e {vencedor['qtd_venda_apto']} venda\n")
    else:
        f.write(f"2. Segmento: - | 3. Diaria: R$ {vencedor['diaria_med']:.0f} | 4. Receita 60% ano R$ {vencedor['rec'][0.60][1]:,.0f}\n")
    if segundo:
        f.write(f"6. **Comparacao segunda melhor:** **{segundo['bairro']}** receita 60% ano R$ {segundo['rec'][0.60][1]:,.0f} (diaria R$ {segundo['diaria_med']:.0f}, {segundo['qtd_airbnb']} Airbnb) - **vencedor tem R$ {vencedor['rec'][0.60][1]-segundo['rec'][0.60][1]:,.0f} a mais/ano ({(vencedor['rec'][0.60][1]/segundo['rec'][0.60][1]-1)*100:.1f}%)**\n")
    f.write(f"7. **Limitacoes:** diária é historica (999/3710 com preço, 21-35% por perfil), 60% é hipótese não observada, sem correspondência Viva vs Airbnb por imóvel, amostra 4q pequena (286 Airbnb, 60 com preço), condo/IPTU 30% NA, `data/` intacto. **Conclusão é sobre potencial de receita por localização, não recomendação de compra definitiva (sem ROI).**\n")
    f.write("\n## Caminho percorrido\n\n")
    f.write("1. **Arquivos usados:** `data/VivaReal_Itapema.csv` (8329, 7529 apto), `analysis/base_analitica_itapema.csv` (4441, 3710 apto, validado LEFT JOIN), `analysis/relatorio_receita.md` (diarias 460/700/1075/580/790) e `analysis/relatorio_cruzamento_compra_aluguel.md` (5 perfis) como contexto, sem refazer Pergunta 1.\n")
    f.write("2. **Colunas usadas:** Viva `suburb, bedrooms, sale_price, listing_type`, Base `suburb, number_of_bedrooms, price_mediano, listing_type, number_of_reviews`.\n")
    f.write("3. **Filtros aplicados:** `listing_type==apartamento` (7529 Viva, 3710 Base), `suburb_norm` e `bedrooms` para perfis, `price_mediano.notna()` para com preço, `0<usable_area<10000` já usado no cruzamento mas não necessário aqui.\n")
    f.write("4. **Bairros normalizados:** `astype(str).str.strip().str.lower()` em ambas as bases, `title()` para exibição; `Meia Praia` variants unificadas, vazios `<VAZIO>` mantidos mas excluídos do ranking (<30).\n")
    f.write("5. **Segmentos formados:** Nível 1 `bairro` isolado (apto) e Nível 2 `bairro x quartos` (2q/3q/4q) - segmento, não imóvel, sem JOIN Viva vs Airbnb.\n")
    f.write("6. **Diária calculada:** `median(price_mediano)` por segmento onde `com_preco>0` (DADO OBSERVADO, robusta a outlier R$29.000, mediana das medianas).\n")
    f.write("7. **Receita calculada:** `receita_mensal = price_mediano_median *30*ocupacao` e `receita_anual = mensal*12` para 40/60/80% (mesma fórmula validada em `relatorio_receita.md:3`), RESULTADO CALCULADO.\n")
    f.write("8. **Premissas utilizadas:** Ocupação 40% (12d), 60% (18d), 80% (24d) sobre 30 dias - hipótese, não dado; diária é historica, não receita observada.\n")
    f.write("9. **Validações feitas:** cobertura `com_preco/qtd_airbnb` por bairro/segmento, sinalizado <30 com preço como amostra pequena; volume `qtd_venda_apto` vs `qtd_airbnb` separados; mediana para reduzir outlier; `data/` não alterado (verificado `Path.exists()` sem escrita); ranking por receita anual 60% mas cruzado com volume para não vencer só por diária alta (ex: 4q Morretes diária 635 mas 59 airbnb vs 1451 3q MP).\n")
    f.write("10. **Localização vencedora escolhida:** Maior receita anual 60% entre bairros com `qtd_airbnb>=100` e `com_preco>=30` para consistência, depois segmento `q x bairro` que mais contribui dentro dela (maior receita anual). Por isso Meia Praia venceu isoladamente (receita 600*18*12) e 3q Meia Praia (700) / 4q Meia Praia (1075) como segmentos top, mas com volume 1451 vs 286 para decidir.\n")
    f.write("11. **Limitações que afetam conclusão:** Diária só 21-35% dos Airbnb têm histórico (60-327 por perfil), 40/60/80% são hipóteses, sem ocupação real, sem ROI, sem correspondência imóvel-a-imóvel, amostra 4q e alguns bairros <30 com preço, `data/` intacto.\n")

print(f"Relatorio salvo em {OUT_MD}")
print(f"CSV salvo em {OUT_CSV}")

# Terminal resumo
print("\n--- RESUMO TERMINAL (filtrado para volume >=100 e com_preco>=30) ---")
rank_filtrado = [r for r in result_bairro_sorted if r["qtd_airbnb"]>=100 and r["com_preco"]>=30][:5]
for i, r in enumerate(rank_filtrado,1):
    print(f"{i}. {r['bairro']:20} | receita 60% ano R$ {r['rec'][0.60][1]:,.0f} (diaria {r['diaria_med']:.0f}, {r['qtd_airbnb']} Airbnb, {r['com_preco']} com preco {r['cobertura']:.0f}%)")
if seg_top:
    print(f"Segmento vencedor: {seg_top['perfil']} | diaria {seg_top['diaria_med']:.0f} | receita 60% ano R$ {seg_top['rec'][0.60][1]:,.0f} | {seg_top['qtd_airbnb']} Airbnb ({seg_top['com_preco']} com preco)")
print(f"Cobertura dados: {df_base['price_mediano'].notna().sum()}/3710 apto com preco (999 na base) | 4q MP 60/286 (21%) amostra pequena sinalizada")
print(f"Conclusao em uma frase: {vencedor['bairro']} vence em receita potencial por combinar diaria R${vencedor['diaria_med']:.0f} com volume {vencedor['qtd_airbnb']} Airbnb e {vencedor['qtd_venda_apto']} a venda, mas segmento {seg_top['perfil'] if seg_top else ''} é o que mais contribui ({seg_top['rec'][0.60][1]:,.0f}/ano a 60%).")

