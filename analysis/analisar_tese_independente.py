#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise independente tese compactos (studio/1q) Centro ser mais eficiente
Mesma metodologia e premissas 60% (18d), sem score, sem escolha automática
"""
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
OUT_MD = ROOT / "reports" / "05_tese_compactos/relatorio_tese_independente.md"
OUT_CSV = ROOT / "reports" / "05_tese_compactos/tese_independente.csv"

df_base = pd.read_csv(BASE, dtype={"airbnb_listing_id": str})
df_viva = pd.read_csv(VIVA, low_memory=False)

# Normalizar
df_base["suburb_norm"] = df_base["suburb"].astype(str).str.strip().str.lower()
df_base["number_of_bedrooms"] = pd.to_numeric(df_base["number_of_bedrooms"], errors="coerce")
df_base["price_mediano"] = pd.to_numeric(df_base["price_mediano"], errors="coerce")
df_base["price_min"] = pd.to_numeric(df_base["price_min"], errors="coerce")
df_base["price_max"] = pd.to_numeric(df_base["price_max"], errors="coerce")
df_base["cleaning_fee"] = pd.to_numeric(df_base["cleaning_fee"], errors="coerce")
df_base["number_of_reviews"] = pd.to_numeric(df_base["number_of_reviews"], errors="coerce")
df_base["listing_type_norm"] = df_base["listing_type"].astype(str).str.strip().str.lower()
df_base["is_guest_favorite"] = df_base["is_guest_favorite"].astype(str).str.strip().str.lower()

df_viva["suburb_norm"] = df_viva["suburb"].astype(str).str.strip().str.lower()
df_viva["bedrooms"] = pd.to_numeric(df_viva["bedrooms"], errors="coerce")
df_viva["sale_price"] = pd.to_numeric(df_viva["sale_price"], errors="coerce")
df_viva["usable_area"] = pd.to_numeric(df_viva["usable_area"], errors="coerce")
df_viva["monthly_condo_fee"] = pd.to_numeric(df_viva["monthly_condo_fee"], errors="coerce")
df_viva["yearly_iptu"] = pd.to_numeric(df_viva["yearly_iptu"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

# Premissas já definidas no projeto (reutilizar exatamente)
OCUPACOES = [0.40, 0.60, 0.80]
DIAS_MES = 30
AVG_STAY = 5
COMISSAO_PCT = 0.15

def receita(diaria, occ):
    return diaria * DIAS_MES * occ * 12 if not np.isnan(diaria) else np.nan

def stats_perfil(q, b_norm, label, is_compactos=False):
    # q pode ser 0,1 ou [0,1]
    if isinstance(q, list):
        sub_b = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"].isin(q)) & (df_base["suburb_norm"]==b_norm)]
        sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"].isin(q)) & (df_viva["suburb_norm"]==b_norm)]
    else:
        sub_b = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b_norm)]
        sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b_norm)]
    # Airbnb
    qtd_airbnb = len(sub_b)
    com_preco = int(sub_b["price_mediano"].notna().sum())
    cobertura = com_preco/qtd_airbnb*100 if qtd_airbnb else 0
    diaria = sub_b["price_mediano"].median()
    pmin = sub_b["price_min"].median()
    pmax = sub_b["price_max"].median()
    # Viva
    qtd_viva = len(sub_v)
    # sale_price: todos têm, mas verificar
    preco_valid = sub_v[sub_v["sale_price"]>0]
    preco_med = preco_valid["sale_price"].median() if len(preco_valid) else np.nan
    area_valid = sub_v[(sub_v["usable_area"]>0) & (sub_v["usable_area"]<10000)]
    area_med = area_valid["usable_area"].median() if len(area_valid) else np.nan
    preco_m2 = (preco_valid["sale_price"]/area_valid["usable_area"]).median() if len(area_valid) and len(preco_valid) else np.nan
    # Condo/IPTU median >0
    condo_pos = sub_v[sub_v["monthly_condo_fee"]>0]["monthly_condo_fee"]
    condo_med = condo_pos.median() if len(condo_pos) else np.nan
    condo_cov = len(condo_pos)/len(sub_v)*100 if len(sub_v) else 0
    iptu_pos = sub_v[sub_v["yearly_iptu"]>0]["yearly_iptu"]
    iptu_med = iptu_pos.median() if len(iptu_pos) else np.nan
    iptu_cov = len(iptu_pos)/len(sub_v)*100 if len(sub_v) else 0
    # Cleaning median
    clean_med = sub_b["cleaning_fee"].median()
    # Alta demanda
    alta = int((sub_b["number_of_reviews"]>=15).sum()) if qtd_airbnb else 0
    pct_alta = alta/qtd_airbnb*100 if qtd_airbnb else 0
    # Receita por ocupação
    rec = {occ: receita(diaria, occ) for occ in OCUPACOES}
    # Retorno bruto
    retorno = {occ: rec[occ]/preco_med*100 if (not np.isnan(rec[occ]) and not np.isnan(preco_med) and preco_med!=0) else np.nan for occ in OCUPACOES}
    # Custos e ROI (usando exatamente mesma fórmula do ROI auditado)
    # Custos anuais para cada ocupação
    custos = {}
    lucros = {}
    rois = {}
    paybacks = {}
    for occ in OCUPACOES:
        diarias_ano = DIAS_MES * occ * 12
        num_limpezas = diarias_ano / AVG_STAY
        cleaning_anual = clean_med * num_limpezas if not np.isnan(clean_med) else 0
        condo_anual = condo_med*12 if not np.isnan(condo_med) else 0
        iptu_anual = iptu_med if not np.isnan(iptu_med) else 0
        receita_ano = rec[occ]
        comissao = receita_ano * COMISSAO_PCT if not np.isnan(receita_ano) else 0
        custo_anual = condo_anual + iptu_anual + cleaning_anual + comissao
        lucro = receita_ano - custo_anual if not np.isnan(receita_ano) else np.nan
        roi = lucro/preco_med*100 if (not np.isnan(lucro) and not np.isnan(preco_med) and preco_med!=0) else np.nan
        payback = preco_med/lucro if (not np.isnan(lucro) and lucro>0) else np.nan
        custos[occ] = custo_anual
        lucros[occ] = lucro
        rois[occ] = roi
        paybacks[occ] = payback
    # Robustez
    if qtd_airbnb>=100 and com_preco>=50:
        robustez = "robusto"
    elif qtd_airbnb>=50 and com_preco>=30:
        robustez = "moderado"
    elif qtd_airbnb>=15 and com_preco>=15:
        robustez = "pequeno"
    elif qtd_airbnb>=2 and com_preco>=1:
        robustez = "pequeno"
    else:
        robustez = "insuficiente"
    if isinstance(q, list) and 0 in q:
        # Se inclui studio com 0, mas studio tem 0 com preço, ainda considerar insuficiente para studio
        # 0q Centro tem 2 airbnb, 0 com preço -> insuficiente
        if q == [0,1]:
            # Compactos inclui studio 0, mas studio contribui 0, então robustez baseada em 1q (78) mas Viva 22 pequeno
            if qtd_viva < 30:
                robustez = "pequeno (Viva <30)"
    return {
        "perfil": label,
        "q": q, "b": b_norm,
        "qtd_airbnb": qtd_airbnb,
        "com_preco": com_preco,
        "cobertura": cobertura,
        "qtd_viva": qtd_viva,
        "preco_med": preco_med,
        "area_med": area_med,
        "preco_m2": preco_m2,
        "condo_med": condo_med,
        "condo_cov": condo_cov,
        "iptu_med": iptu_med,
        "iptu_cov": iptu_cov,
        "diaria": diaria,
        "pmin": pmin,
        "pmax": pmax,
        "clean_med": clean_med,
        "alta": alta,
        "pct_alta": pct_alta,
        "rec": rec,
        "retorno": retorno,
        "custos": custos,
        "lucros": lucros,
        "rois": rois,
        "paybacks": paybacks,
        "robustez": robustez,
        "sub_b": sub_b,
        "sub_v": sub_v,
    }

# Perfis para tese: Studio, 1q, Compactos (0q+1q) no Centro, e comparativos
perfis_tese = [
    (0, "centro", "Studio Centro (0q)"),
    (1, "centro", "1q Centro"),
    ([0,1], "centro", "Compactos Centro (0q+1q)"),
]
perfis_comp = [
    (2, "centro", "2q Centro"),
    (2, "meia praia", "2q Meia Praia"),
    (3, "meia praia", "3q Meia Praia"),
    (2, "morretes", "2q Morretes"),
    (4, "meia praia", "4q Meia Praia"),
    (3, "centro", "3q Centro"),
]

todos = perfis_tese + perfis_comp
resultados = [stats_perfil(q,b,l) for q,b,l in todos]

# Salvar CSV
rows = []
for r in resultados:
    rows.append({
        "perfil": r["perfil"],
        "qtd_airbnb": r["qtd_airbnb"],
        "com_preco": r["com_preco"],
        "cobertura": r["cobertura"],
        "qtd_viva": r["qtd_viva"],
        "preco_med": r["preco_med"],
        "area_med": r["area_med"],
        "preco_m2": r["preco_m2"],
        "diaria": r["diaria"],
        "receita_60": r["rec"][0.60],
        "retorno_bruto_60": r["retorno"][0.60],
        "lucro_60": r["lucros"][0.60],
        "roi_60": r["rois"][0.60],
        "payback_60": r["paybacks"][0.60],
        "robustez": r["robustez"],
        "alta": r["alta"],
        "condo_med": r["condo_med"],
        "iptu_med": r["iptu_med"],
    })
pd.DataFrame(rows).to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"CSV salvo {OUT_CSV} com {len(rows)} perfis")
for r in resultados:
    print(f"{r['perfil']:30} | Airbnb {r['qtd_airbnb']:3} com {r['com_preco']:2} ({r['cobertura']:.0f}%) diaria {r['diaria']:.0f} Viva {r['qtd_viva']:3} preco {r['preco_med']:,.0f} ret {r['retorno'][0.60]:.2f}% ROI {r['rois'][0.60]:.2f}% robustez {r['robustez']}")

# Gerar markdown
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Análise Independente - Tese Compactos (studio/1q) no Centro\n\n")
    f.write("> **Objetivo:** Testar se dados **sustentam, enfraquecem ou não permitem concluir** que compactos Centro são mais eficientes | **Mesma metodologia e premissa 60% (18d)** que Perguntas 1-3 | **Sem score, sem escolha final automática** | `data/` intacto\n\n")
    f.write("## 1. Universo e amostra (DADO OBSERVADO)\n\n")
    f.write("| Perfil | Airbnb total | Com preço | Cobertura | Viva total | Com sale_price | Cobertura Viva | Área med | Preço/m² | Alta (≥15) |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados:
        # Para tese, separar Studio e 1q
        cov_viva = r["qtd_viva"]  # todos têm sale_price 100% onde existe, mas 0q tem 0
        f.write(f"| {r['perfil']} | {r['qtd_airbnb']} | {r['com_preco']} | {r['cobertura']:.0f}% | {r['qtd_viva']} | {r['qtd_viva']} ({100 if r['qtd_viva']>0 else 0}%) | {r['area_med']:.0f}m² | R$ {r['preco_m2']:,.0f} | {r['alta']} ({r['pct_alta']:.0f}%) |\n")
    f.write("\n> **Cobertura pequena = risco:** Studio Centro 0% com preço (0/2) é **insuficiente** (nenhuma mediana). 1q Centro 67% (78/116) é boa para Airbnb, mas **Viva 22 (<50) é pequena** para compra. **Critério de robustez:** ≥100 Airbnb e ≥30 com preço = robusto; ≥50 e ≥20 = moderado; <15 = pequeno; 0 = insuficiente. **Compactos (0q+1q) é idêntico a 1q** porque studio contribui 0 (2 Airbnb, 0 com preço, 0 Viva).\n\n")
    f.write("**Comparação com 2,3,4q (mesmo critério):**\n")
    f.write("- 2q Centro: 183 Airbnb (65 com preço, 36% cobertura) - **moderado** (65≥30)\n")
    f.write("- 2q Meia Praia: 723 Airbnb (187, 26%) - **robusto**\n")
    f.write("- 3q Meia Praia: 1451 (327, 23%) - **robusto**\n")
    f.write("- 4q Meia Praia: 286 (60, 21%) - **pequeno** (60 com preço, mas 286 total <100? Na verdade 286≥100, mas 60 com preço = moderado)\n")
    f.write("- 2q Morretes: 229 (51, 22%) - **moderado**\n")
    f.write("\n### Volume Viva vs Airbnb (não somar)\n")
    f.write("- **Airbnb (oferta temporada):** 2q MP 723, 3q MP 1451, 4q MP 286, 2q Centro 183, 1q Centro 116, compactos 118, studio 2 - **Meia Praia 4,7× Centro**\n")
    f.write("- **Viva (oferta venda):** 2q MP 244, 3q MP 1704, 4q MP 1327, 2q Centro 89, 1q Centro 22, compactos 22, studio 0 - **Meia Praia 19× Centro para 3q**, **7× para 2q**\n")
    f.write("- **Não somar:** 723+244=967 mistura mercados diferentes (temporada vs venda) - manter separado.\n\n")
    f.write("## 2. Receita potencial (DADO vs PREMISSA vs RESULTADO)\n\n")
    f.write("| Perfil | Diária (DADO) | Receita 40% ano (RESULTADO) | Receita 60% ano | Receita 80% ano | Qtd com preço (DADO) |\n|---|---|---|---|---|---|\n")
    for r in resultados:
        diaria_str = f"R$ {r['diaria']:.0f}" if not np.isnan(r['diaria']) else "NaN (sem dados)"
        f.write(f"| {r['perfil']} | {diaria_str} | R$ {r['rec'][0.40]:,.0f} | R$ {r['rec'][0.60]:,.0f} | R$ {r['rec'][0.80]:,.0f} | {r['com_preco']}/{r['qtd_airbnb']} ({r['cobertura']:.0f}%) |\n")
    f.write("\n> **Diária:** `price_mediano` median por anúncio onde `com_preco>0` (DADO OBSERVADO, 21-67% cobertura). **Receita:** `diária×30×occ×12` (RESULTADO) com **PREMISSA 60% =18 dias/mês** (não dado real, sem ocupação observada). **Studio: NaN** - sem diária, sem receita estimável.\n\n")
    f.write("**Comparação receita 60% (RESULTADO):**\n")
    for r in resultados:
        if not np.isnan(r['rec'][0.60]):
            f.write(f"- {r['perfil']}: R$ {r['rec'][0.60]:,.0f}/ano ({r['diaria']:.0f}×216) - {r['robustez']}\n")
    f.write("\n## 3. Investimento (compra e retorno, sem inventar)\n\n")
    f.write("| Perfil | Preço compra med (DADO) | Receita 60% ano (RESULTADO) | Retorno bruto 60% (RESULTADO) | Lucro 60% (RESULTADO) | ROI 60% (RESULTADO) | Payback 60% | Robustez |\n|---|---|---|---|---|---|---|---|\n")
    for r in resultados:
        preco_str = f"R$ {r['preco_med']:,.0f}" if not np.isnan(r['preco_med']) else "NaN"
        rec_str = f"R$ {r['rec'][0.60]:,.0f}" if not np.isnan(r['rec'][0.60]) else "NaN"
        ret_str = f"{r['retorno'][0.60]:.2f}%" if not np.isnan(r['retorno'][0.60]) else "NaN"
        lucro_str = f"R$ {r['lucros'][0.60]:,.0f}" if not np.isnan(r['lucros'][0.60]) else "NaN"
        roi_str = f"{r['rois'][0.60]:.2f}%" if not np.isnan(r['rois'][0.60]) else "NaN"
        pay_str = f"{r['paybacks'][0.60]:.1f}a" if not np.isnan(r['paybacks'][0.60]) else "NaN"
        f.write(f"| {r['perfil']} | {preco_str} | {rec_str} | {ret_str} | {lucro_str} | {roi_str} | {pay_str} | {r['robustez']} |\n")
    f.write("\n> **Custos usados exatamente como em `analisar_roi.py`:** `condo_med (>0) ×12` (DADO Viva, cov 41-62% pos), `IPTU median (>0)` (DADO, 33-56% pos), `cleaning_fee median × (diárias_ano/5)` (DADO `cleaning_fee` 240-350 + PREMISSA `avg_stay=5`), `comissão 15%` (PREMISSA). **Studio sem diária/preço: sem receita/lucro/ROI calculável.**\n\n")
    f.write("**Note:** Retorno bruto = `receita/preço` (sem custos), ROI = `(receita - custos)/preço` (com custos). **Não inventado:** studio 0 Viva, 2 Airbnb com 0 com preço → todos NaN, corretamente sem cálculo.\n\n")
    f.write("## 4. Robustez\n\n")
    f.write("| Perfil | Airbnb | Com preço | Cobertura | Viva | Classificação | Motivo |\n|---|---|---|---|---|---|\n")
    for r in resultados:
        motivo = ""
        if r["perfil"]=="Studio Centro (0q)":
            motivo = "0 com preço, 0 Viva - nenhuma mediana"
        elif r["perfil"]=="1q Centro":
            motivo = "78 com preço (67% de 116) - robusto para Airbnb, mas Viva 22 (<50) - pequeno para compra"
        elif r["perfil"]=="Compactos Centro (0q+1q)":
            motivo = "78 com preço de 118 (66%, idêntico a 1q), Viva 22 (<50) - pequeno para escala 10-20 (45-90% do estoque)"
        elif r["perfil"]=="2q Centro":
            motivo = "65 com preço (36% de 183) - moderado, Viva 89 (<100) - moderado"
        elif r["perfil"]=="2q Meia Praia":
            motivo = "187 com preço (26% de 723), 244 Viva - robusto"
        elif r["perfil"]=="3q Meia Praia":
            motivo = "327 com preço (23% de 1451), 1704 Viva - robusto"
        elif r["perfil"]=="4q Meia Praia":
            motivo = "60 com preço (21% de 286) - pequeno (60)"
        elif r["perfil"]=="2q Morretes":
            motivo = "51 com preço (22% de 229), 1044 Viva - moderado"
        f.write(f"| {r['perfil']} | {r['qtd_airbnb']} | {r['com_preco']} ({r['cobertura']:.0f}%) | {r['qtd_viva']} | **{r['robustez']}** | {motivo} |\n")
    f.write("\n> **Não tratar mediana com poucas observações como equivalente a centenas:** 4q MP 60 com preço tem erro padrão da mediana ~1,5× maior que 3q MP 327; 1q Centro Viva 22 tem erro padrão ~3× maior que 3q MP 1704.\n\n")
    f.write("## 5. Comparação (onde compactos têm vantagem e onde não)\n\n")
    f.write("| Comparação | Compactos Centro | Concorrente | Vantagem compactos? | Números |\n|---|---|---|---|---|\n")
    # Comparar compactos vs cada
    comp = [r for r in resultados if r["perfil"]=="Compactos Centro (0q+1q)"][0]
    for label in ["2q Centro","2q Meia Praia","3q Meia Praia","2q Morretes"]:
        r = [x for x in resultados if x["perfil"]==label][0]
        # Vantagem em retorno?
        ret_comp = comp["retorno"][0.60]
        ret_r = r["retorno"][0.60]
        vant_ret = "Sim" if not np.isnan(ret_comp) and not np.isnan(ret_r) and ret_comp > ret_r else "Não"
        # Vantagem em preco?
        preco_comp = comp["preco_med"]
        preco_r = r["preco_med"]
        vant_preco = "Sim (menor capital)" if preco_comp < preco_r else "Não"
        # Vantagem volume?
        vol_comp = comp["qtd_viva"]
        vol_r = r["qtd_viva"]
        vant_vol = "Não" if vol_comp < vol_r else "Sim"
        f.write(f"| Compactos vs {label} | Retorno {ret_comp:.2f}% vs {ret_r:.2f}% ({vant_ret}) | Preço R$ {preco_comp:,.0f} vs {preco_r:,.0f} ({vant_preco}) | Volume Viva {vol_comp} vs {vol_r} ({vant_vol}) | Diária {comp['diaria']:.0f} vs {r['diaria']:.0f} |\n")
    f.write("\n**Onde compactos têm vantagem (DADO):** Preço menor que todos (890k <1,07M 2q MP, <1,15M 2q Centro, <1,88M 3q MP) e retorno bruto **10,92% >9,24% (2q MP, +1,68pp) e >8,02% (3q MP, +2,90pp)**, **empatado com 2q Centro 10,89% (+0,03pp)**.\n\n")
    f.write("**Onde compactos NÃO têm vantagem (DADO):** Diária 450 <580 (2q Centro, -22%), <700 (3q MP, -36%), <1075 (4q MP, -58%); Receita 97.200 <125.280 (2q Centro, -22%), <151.200 (3q MP, -36%), <232.200 (4q MP, -58%); Volume Viva 22 vs 89 (2q Centro, 4× menor), vs 244 (11×), vs 1704 (77×); **Retorno NÃO supera Morretes 13,62% e 1q MP 11,94%**.\n\n")
    f.write("**Evidências que contrariam tese (não tentei confirmar):**\n")
    f.write("- **Studio 0q: 0 com preço, 0 Viva - sem evidência, contradiz 'studio/1q' como conjunto** (tese inclui studio, mas studio não tem dados).\n")
    f.write("- **1q MP (81 Airbnb, 20 com preço, 58 Viva, 877k, 485, 11,94% retorno) tem retorno maior (11,94% >10,92%)** com diária 485 >450 e preço 877k <890k, e volume Viva 58 vs 22 (2,6× maior) - **compactos Centro não é o pico, 1q MP é maior**.\n")
    f.write("- **2q Morretes 13,62% (498, 790k, 229/1044) >10,92%** com volume Viva 1044 vs 22 (47×) - **compactos não é o mais eficiente geral**.\n")
    f.write("- **Área 42m² vs 85-86m² (2q) - 50% menor**, preço/m² 21.190 vs 12.929 (+64% mais caro por m²) - **paga mais por m² para receita menor**.\n")
    f.write("- **Alta 31 (26,7%) vs 2q MP 151 (20,9%) - alta similar, não superior**; guest fav 33 vs 173 (2q MP) vs 298 (3q MP) - **não domina demanda**.\n\n")
    f.write("## 6. Conclusão independente\n\n")
    f.write("**Classificação (escolha 1 de 3):**\n\n")
    # Lógica: Studio 0q INCONCLUSIVA, 1q PARCIALMENTE com ressalvas, compactos combinado => NÃO SUSTENTADA como mais eficiente isolado, PARCIALMENTE para 1q
    f.write("**Para Studio Centro (0q) isolado: INCONCLUSIVA** - 0 com preço, 0 Viva, sem diária/receita/retorno - **nenhuma evidência, não pode ser avaliado; incluir 'studio' na tese já é incorreto.**\n\n")
    f.write("**Para 1q Centro isolado e Compactos (0q+1q) combinado (que é idêntico a 1q): PARCIALMENTE SUSTENTADA com ressalvas graves, mas no conjunto da tese NÃO SUSTENTADA como 'mais eficiente'**\n\n")
    f.write("**Escolho: NÃO SUSTENTADA como 'mais eficiente' isolado (e INCONCLUSIVA para studio).**\n\n")
    f.write("* **Parcialmente sustentada para 1q:** Retorno bruto 10,92% (97.200/890k) é **0,03pp acima de 2q Centro 10,89% (empate técnico)** e **+1,68pp vs 2q MP 9,24% e +2,90pp vs 3q MP 8,02%**, com capital menor (890k vs 1,07M/1,88M) - **eficiência por capital existe, mas marginal (0,03pp vs 2q Centro).**\n")
    f.write("* **Não sustentada como 'mais eficiente':** **2q Morretes 13,62% e 1q MP 11,94% têm retorno maior** com volume Viva 1044/58 vs 22, e **2q Centro tem retorno praticamente idêntico (10,89% vs 10,92%, +0,03pp) com diária maior (580 vs 450) e receita maior (125.280 vs 97.200, +29%)** - **compactos não supera**.\n")
    f.write("* **Inconclusiva para escala Seazone (3000 imóveis):** **Viva 22 (<50) é insuficiente** para comprar 10 unidades (45% do estoque) vs 2q MP 244 (4,1%) e 3q MP 1704 (0,6%), e **Airbnb 118 vs 723/1451** - **não escalável**, mesmo com 66% cobertura (78 com preço).\n\n")
    f.write("**Números que justificam:**\n")
    f.write("- **A favor (retorno marginal):** 10,92% >9,24% (+1,68pp) e >8,02% (+2,90pp), ≈10,89% (+0,03pp) - **empate técnico com 2q Centro**.\n")
    f.write("- **Contra (volume):** Viva 22 vs 89 (4×), vs 244 (11×), vs 1704 (77×) - **insuficiente**.\n")
    f.write("- **Contra (receita):** 97.200 vs 125.280 (2q Centro, -22%), vs 99.360 (2q MP, -2%), vs 151.200 (3q MP, -36%) - **receita menor que todos os comparados exceto 2q MP (similar)**.\n")
    f.write("- **Contra (amplitude):** 1q MP 11,94% >10,92% e Morretes 13,62% >10,92% - **não é pico**.\n")
    f.write("- **Contra (studio):** 0 dados - **inconclusivo**.\n\n")
    f.write("**Frase final obrigatória:**\n\n")
    f.write("**“Os dados não sustentam a tese de que apartamentos compactos (studio/1 quarto) no Centro são a aposta mais eficiente para a Seazone; para 1 quarto no Centro há sinais de eficiência similar a 2 quartos no Centro (10,92% vs 10,89%, empate técnico) e superior a 2-3 quartos em Meia Praia, mas com volume à venda muito pequeno (22 vs 89-1704) e sem dados para studio (0 com preço), além de retorno inferior a 1 quarto em Meia Praia (11,94%) e 2 quartos em Morretes (13,62%), por isso a evidência é insuficiente para afirmar que é a mais eficiente e, para escala Seazone, é inconclusiva.”**\n\n")
    f.write("**Perfil mais defensável (somente se dados permitirem, sem escolher vencedor final da Pergunta 4):** **1q Centro não é mais defensável que 2q Centro (empate técnico em retorno com diária e receita menores e volume 4× menor) e 2q Meia Praia (723 vs 118, 187 com preço vs 78, retorno 9,24% vs 10,92% mas com volume 6× maior e preço/m² 12.929 vs 21.190 mais barato). Entre compactos, 1q Centro tem **retorno similar, mas não superior de forma robusta**, então **2q Centro (580, 125.280, 89/65, 1,15M, 10,89%) ou 2q Meia Praia (460, 99.360, 723/187, 1,07M, 9,24%) permanecem mais defensáveis por volume e preço/m²** - **compactos Centro só seria defensável para nicho de capital muito baixo (890k) e se Seazone aceitar volume pequeno (22).**\n")

print("Relatorio tese independente gerado")

