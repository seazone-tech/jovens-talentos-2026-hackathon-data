#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validacao tese: compactos (studio/1q) no Centro seriam aposta mais eficiente
Mesma metodologia e premissa 60% (18d), sem score, sem escolha final
"""
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
OUT_MD = ROOT / "reports" / "05_tese_compactos/relatorio_tese_compactos_centro.md"
OUT_CSV = ROOT / "reports" / "05_tese_compactos/tese_compactos_centro.csv"

df_base = pd.read_csv(BASE, dtype={"airbnb_listing_id": str})
df_viva = pd.read_csv(VIVA, low_memory=False)

# Normalizar
df_base["suburb_norm"] = df_base["suburb"].astype(str).str.strip().str.lower()
df_base["number_of_bedrooms"] = pd.to_numeric(df_base["number_of_bedrooms"], errors="coerce")
df_base["price_mediano"] = pd.to_numeric(df_base["price_mediano"], errors="coerce")
df_base["price_min"] = pd.to_numeric(df_base["price_min"], errors="coerce")
df_base["price_max"] = pd.to_numeric(df_base["price_max"], errors="coerce")
df_base["number_of_reviews"] = pd.to_numeric(df_base["number_of_reviews"], errors="coerce")
df_base["star_rating"] = pd.to_numeric(df_base["star_rating"], errors="coerce")
df_base["picture_count"] = pd.to_numeric(df_base["picture_count"], errors="coerce")
df_base["listing_type_norm"] = df_base["listing_type"].astype(str).str.strip().str.lower()
df_base["is_guest_favorite"] = df_base["is_guest_favorite"].astype(str).str.strip().str.lower()
df_base["is_professional"] = df_base["is_professional"].astype(str).str.strip().str.lower()

df_viva["suburb_norm"] = df_viva["suburb"].astype(str).str.strip().str.lower()
df_viva["bedrooms"] = pd.to_numeric(df_viva["bedrooms"], errors="coerce")
df_viva["sale_price"] = pd.to_numeric(df_viva["sale_price"], errors="coerce")
df_viva["usable_area"] = pd.to_numeric(df_viva["usable_area"], errors="coerce")
df_viva["monthly_condo_fee"] = pd.to_numeric(df_viva["monthly_condo_fee"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

# Helpers
def receita(diaria, occ=0.60):
    return diaria *30*occ*12 if not np.isnan(diaria) else np.nan

def stats_base(q, b_norm, label):
    # q pode ser 0,1 ou lista [0,1] para compactos
    if isinstance(q, list):
        sub = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"].isin(q)) & (df_base["suburb_norm"]==b_norm)]
    else:
        sub = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b_norm)]
    qtd = len(sub)
    com_preco = int(sub["price_mediano"].notna().sum())
    cobertura = com_preco/qtd*100 if qtd else 0
    diaria = sub["price_mediano"].median()
    pmin = sub["price_min"].median()
    pmax = sub["price_max"].median()
    receita60 = receita(diaria,0.60)
    # Demanda
    alta = int((sub["number_of_reviews"]>=15).sum()) if qtd else 0
    pct_alta = alta/qtd*100 if qtd else 0
    # Outros sinais
    star_med = sub[sub["star_rating"]>0]["star_rating"].median() if len(sub[sub["star_rating"]>0]) else np.nan
    pic_med = sub["picture_count"].median() if qtd else np.nan
    guest_fav = (sub["is_guest_favorite"]=="true").sum()
    prof_true = (sub["is_professional"]=="true").sum()
    return {
        "label": label,
        "q": q, "b": b_norm,
        "qtd": qtd,
        "com_preco": com_preco,
        "cobertura": cobertura,
        "diaria": diaria,
        "pmin": pmin,
        "pmax": pmax,
        "receita60": receita60,
        "receita40": receita(diaria,0.40),
        "receita80": receita(diaria,0.80),
        "alta": alta,
        "pct_alta": pct_alta,
        "star_med": star_med,
        "pic_med": pic_med,
        "guest_fav": guest_fav,
        "prof_true": prof_true,
        "sub": sub,
    }

def stats_viva(q, b_norm, label):
    if isinstance(q, list):
        sub = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"].isin(q)) & (df_viva["suburb_norm"]==b_norm)]
    else:
        sub = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b_norm)]
    qtd = len(sub)
    valid_price = sub[sub["sale_price"]>0]
    preco_med = valid_price["sale_price"].median() if len(valid_price) else np.nan
    area_valid = sub[(sub["usable_area"]>0) & (sub["usable_area"]<10000)]
    area_med = area_valid["usable_area"].median() if len(area_valid) else np.nan
    preco_m2 = (valid_price["sale_price"]/area_valid["usable_area"]).median() if len(area_valid) and len(valid_price) else np.nan
    # Na verdade preco_m2 precisa both valid
    both = sub[(sub["sale_price"]>0) & (sub["usable_area"]>0) & (sub["usable_area"]<10000)]
    preco_m2 = (both["sale_price"]/both["usable_area"]).median() if len(both) else np.nan
    condo_valid = sub[sub["monthly_condo_fee"]>0]
    condo_med = condo_valid["monthly_condo_fee"].median() if len(condo_valid) else np.nan
    return {
        "label": label,
        "qtd": qtd,
        "preco_med": preco_med,
        "area_med": area_med,
        "preco_m2": preco_m2,
        "condo_med": condo_med,
        "qtd_valid_price": len(valid_price),
        "qtd_valid_area": len(area_valid),
    }

# Perfis compactos Centro
perfis_compactos = [
    (0, "centro", "Studio Centro (0q)"),
    (1, "centro", "1q Centro"),
    ([0,1], "centro", "Compactos Centro (0q+1q)"),
]
# Perfis comparação (mesma metodologia)
perfis_comp = [
    (2, "centro", "2q Centro"),
    (2, "meia praia", "2q Meia Praia"),
    (3, "meia praia", "3q Meia Praia"),
    (2, "morretes", "2q Morretes"),
]

todos = perfis_compactos + perfis_comp

resultados = []
for q,b,label in todos:
    sb = stats_base(q,b,label)
    sv = stats_viva(q,b,label)
    # Retorno bruto = receita60 / preco_med
    retorno = sb["receita60"]/sv["preco_med"]*100 if (not np.isnan(sb["receita60"]) and not np.isnan(sv["preco_med"]) and sv["preco_med"]!=0) else np.nan
    resultados.append({
        "perfil": label,
        "q": q, "b": b,
        "qtd_airbnb": sb["qtd"],
        "com_preco": sb["com_preco"],
        "cobertura": sb["cobertura"],
        "diaria": sb["diaria"],
        "pmin": sb["pmin"],
        "pmax": sb["pmax"],
        "receita60": sb["receita60"],
        "receita40": sb["receita40"],
        "receita80": sb["receita80"],
        "alta": sb["alta"],
        "pct_alta": sb["pct_alta"],
        "star_med": sb["star_med"],
        "pic_med": sb["pic_med"],
        "guest_fav": sb["guest_fav"],
        "qtd_viva": sv["qtd"],
        "preco_med": sv["preco_med"],
        "area_med": sv["area_med"],
        "preco_m2": sv["preco_m2"],
        "condo_med": sv["condo_med"],
        "retorno_bruto": retorno,
    })

# Salvar CSV
pd.DataFrame(resultados).to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"CSV tese salvo {OUT_CSV} com {len(resultados)} perfis")

# Prints
for r in resultados:
    print(f"{r['perfil']:25} | Airbnb {r['qtd_airbnb']:3} com_preco {r['com_preco']:2} ({r['cobertura']:.0f}%) diaria {r['diaria']:.0f} receita60 {r['receita60']:.0f} | Viva {r['qtd_viva']:3} preco {r['preco_med']:,.0f} area {r['area_med']:.0f} retorno {r['retorno_bruto']:.2f}% | alta {r['alta']} ({r['pct_alta']:.0f}%)")

# Gerar markdown
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Validacao Tese - Compactos (studio/1q) no Centro\n\n")
    f.write("> **Tese:** \"apartamentos compactos (studio/1 quarto) na região do Centro seriam a aposta mais eficiente\" | **Mesma metodologia e premissa 60% (18d)** que Pergunta 1 | **Sem score, sem escolha final** | `data/` intacto | **PREMISSA 60% ≠ dado**\n\n")
    f.write("## Dados observados vs Premissa\n\n")
    f.write("| Tipo | Exemplo | Valor compactos Centro |\n|---|---|---|\n")
    f.write("| **DADO OBSERVADO** | `sale_price` Viva 1q Centro median | R$ 750.000 (exemplo, ver tabela) |\n")
    f.write("| **DADO OBSERVADO** | `price_mediano` Base median 1q Centro | R$ 384 (exemplo) |\n")
    f.write("| **PREMISSA** | Ocupação 60% =18 dias | 60% |\n")
    f.write("| **RESULTADO CALCULADO** | Receita 60% = 384×216 | R$ 82.944 |\n")
    f.write("| **INTERPRETAÇÃO** | \"Compactos são eficientes\" | Nossa leitura |\n\n")
    f.write("## Quantidade - Compactos Centro\n\n")
    f.write("| Perfil | Airbnb total | Com preço | Cobertura | Viva total | Preço med | Área med | Preço/m² | Alta (≥15) | Guest fav | Pic med |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados[:3]:
        f.write(f"| {r['perfil']} | {r['qtd_airbnb']} | {r['com_preco']} | {r['cobertura']:.0f}% | {r['qtd_viva']} | R$ {r['preco_med']:,.0f} | {r['area_med']:.0f}m² | R$ {r['preco_m2']:,.0f} | {r['alta']} ({r['pct_alta']:.0f}%) | {r['guest_fav']} | {r['pic_med']:.0f} |\n")
    f.write("\n> **Cobertura pequena = risco**: 0q Centro e 1q Centro separados têm poucos com preço (<20), juntos (0q+1q) têm mais, mas ainda menor que 2q Centro (65 com preço).\n\n")
    f.write("## Comparação direta (mesma metodologia 60%)\n\n")
    f.write("| Perfil | Qtd Airbnb | Com preço | Diária | Receita 60% ano | Qtd Viva | Preço med | Retorno bruto 60% | Área med | Alta | Star med |\n|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados:
        f.write(f"| {r['perfil']} | {r['qtd_airbnb']} | {r['com_preco']} ({r['cobertura']:.0f}%) | R$ {r['diaria']:.0f} | R$ {r['receita60']:,.0f} | {r['qtd_viva']} | R$ {r['preco_med']:,.0f} | **{r['retorno_bruto']:.2f}%** | {r['area_med']:.0f}m² | {r['alta']} ({r['pct_alta']:.0f}%) |\n")
    f.write("\n> **Retorno bruto = receita_60_ano / preço_med ×100** (RESULTADO, sem custos, sem ROI). Não é ROI líquido.\n\n")
    f.write("### Evidências que sustentam a tese (a favor)\n\n")
    # Identificar se compactos têm retorno maior
    compactos = [r for r in resultados if "Compactos Centro" in r["perfil"]][0]
    r_2c = [r for r in resultados if r["perfil"]=="2q Centro"][0]
    r_2mp = [r for r in resultados if r["perfil"]=="2q Meia Praia"][0]
    r_3mp = [r for r in resultados if r["perfil"]=="3q Meia Praia"][0]
    if not np.isnan(compactos["retorno_bruto"]) and compactos["retorno_bruto"] > r_2c["retorno_bruto"]:
        f.write(f"- Compactos Centro retorno **{compactos['retorno_bruto']:.2f}%** > 2q Centro {r_2c['retorno_bruto']:.2f}% (+{compactos['retorno_bruto']-r_2c['retorno_bruto']:.2f}pp) - **a favor** (preço menor compensa diária menor).\n")
    else:
        f.write(f"- Compactos Centro retorno **{compactos['retorno_bruto']:.2f}%** vs 2q Centro {r_2c['retorno_bruto']:.2f}% - **não supera**.\n")
    if not np.isnan(compactos["preco_med"]) and compactos["preco_med"] < r_2c["preco_med"]:
        f.write(f"- Preço compactos R$ {compactos['preco_med']:,.0f} < 2q Centro R$ {r_2c['preco_med']:,.0f} (-{(1-compactos['preco_med']/r_2c['preco_med'])*100:.0f}%) - **a favor** (capital menor).\n")
    if compactos["qtd_viva"] >= 50:
        f.write(f"- Volume Viva {compactos['qtd_viva']} ≥50 - **a favor** (mercado existe).\n")
    else:
        f.write(f"- Volume Viva {compactos['qtd_viva']} <50 - **contra** (poucos à venda).\n")
    f.write("\n### Evidências que contrariam a tese (contra)\n\n")
    if compactos["com_preco"] < 30:
        f.write(f"- **Amostra com preço pequena: {compactos['com_preco']}/{compactos['qtd_airbnb']} ({compactos['cobertura']:.0f}%)** vs 2q Centro 65/183 (36%), 2q MP 187/723 (26%) - **contra** (menos robusto).\n")
    if compactos["diaria"] < r_2c["diaria"]:
        f.write(f"- **Diária menor: R$ {compactos['diaria']:.0f} vs 2q Centro R$ {r_2c['diaria']:.0f} (-{(1-compactos['diaria']/r_2c['diaria'])*100:.0f}%)** - **contra** (receita 60% {compactos['receita60']:,.0f} vs {r_2c['receita60']:,.0f}).\n")
    if compactos["pct_alta"] < 15:
        f.write(f"- **Alta demanda baixa: {compactos['alta']} ({compactos['pct_alta']:.0f}%)** vs 2q MP 151 (21%), 2q Centro 34 (19%) - **contra** (menos tração).\n")
    if compactos["area_med"] < 50:
        f.write(f"- **Área muito pequena: {compactos['area_med']:.0f}m²** vs 2q Centro 86m², 2q MP 85m² - **contra** (pode limitar família, sazonalidade).\n")
    # Comparar com Morretes (que tem retorno alto)
    r_mor = [r for r in resultados if r["perfil"]=="2q Morretes"]
    if r_mor:
        r_m = r_mor[0]
        if r_m["retorno_bruto"] > compactos["retorno_bruto"]:
            f.write(f"- **2q Morretes tem retorno bruto maior ({r_m['retorno_bruto']:.2f}% vs {compactos['retorno_bruto']:.2f}%)** com diária {r_m['diaria']:.0f} e preço {r_m['preco_med']:,.0f} - **contra** tese de que Centro compactos é *o* mais eficiente.\n")
    f.write("\n## Volume de mercado e cobertura (qualidade da evidência)\n\n")
    for r in resultados:
        nivel = "robusto" if r["com_preco"]>=30 and r["qtd_airbnb"]>=100 else "moderado" if r["com_preco"]>=20 else "insuficiente"
        f.write(f"- **{r['perfil']}:** {r['qtd_airbnb']} Airbnb, {r['com_preco']} com preço ({r['cobertura']:.0f}%), {r['qtd_viva']} à venda - **{nivel}** (DADO). Alta {r['alta']} ({r['pct_alta']:.0f}%), star {r['star_med']:.2f}, pic {r['pic_med']:.0f}, guest fav {r['guest_fav']}.\n")
    f.write("\n> **Sem volume suficiente, não há escala para Seazone (3000 imóveis):** 0q Centro separado tem 5-15 com preço vs 2q MP 187.\n\n")
    f.write("## Classificação da tese\n\n")
    f.write("**Critério:** sustentada se (a) retorno bruto maior que 2q Centro/2q MP/3q MP com **amostra ≥30 com preço e ≥100 Airbnb** e **volume Viva ≥50**, e (b) sem contradição de diária/volume/alta.\n\n")
    # Lógica de classificação
    # Vamos classificar baseado nos números reais que serão calculados
    # Por enquanto deixar placeholders que serão preenchidos após execução com valores reais
    f.write("**Classificação será preenchida após execução com números reais abaixo.**\n")

print("Gerado esqueleto, aguardando execução para preencher classificação com números reais")

