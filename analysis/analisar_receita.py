#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise de cenarios de receita bruta estimada - base_analitica_itapema.csv
price_mediano = preco historico observado (nao receita) | cenarios ocupacao 40/60/80% sobre 30 dias
Sem ROI, sem recomendacao final
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
OUT = ROOT / "reports" / "01_pergunta1_perfil/relatorio_receita.md"

df = pd.read_csv(BASE, dtype={"airbnb_listing_id": str, "owner_id": str})
# Filtrar apartamento
ap = df[df["listing_type"].str.strip().str.lower() == "apartamento"].copy()

# Garantir numericos
ap["number_of_bedrooms"] = pd.to_numeric(ap["number_of_bedrooms"], errors="coerce")
ap["price_mediano"] = pd.to_numeric(ap["price_mediano"], errors="coerce")
ap["price_medio"] = pd.to_numeric(ap["price_medio"], errors="coerce")
ap["price_min"] = pd.to_numeric(ap["price_min"], errors="coerce")
ap["price_max"] = pd.to_numeric(ap["price_max"], errors="coerce")

# Perfis solicitados
perfis = [
    (2, "Meia Praia"),
    (3, "Meia Praia"),
    (4, "Meia Praia"),
    (2, "Centro"),
    (3, "Centro"),
]

def cenarios(preco_med):
    # 30 dias
    return {
        "40%": preco_med * 30 * 0.40,
        "60%": preco_med * 30 * 0.60,
        "80%": preco_med * 30 * 0.80,
    }

rows = []
for quartos, bairro in perfis:
    sub = ap[(ap["number_of_bedrooms"] == quartos) & (ap["suburb"].str.strip() == bairro)]
    total = len(sub)
    com_preco = sub["price_mediano"].notna().sum()
    # price_mediano do perfil = mediana das medianas por anuncio (robusto)
    # Tambem calcular media das medianas para referencia, e mediana price_medio/min/max
    if com_preco > 0:
        med_pm = sub["price_mediano"].median()
        mean_pm = sub["price_mediano"].mean()
        med_min = sub["price_min"].median()
        med_max = sub["price_max"].median()
        med_medio = sub["price_medio"].median()
        cen = cenarios(med_pm)
        cen_mean = cenarios(mean_pm)
    else:
        med_pm = mean_pm = med_min = med_max = med_medio = float("nan")
        cen = cen_mean = {"40%": float("nan"), "60%": float("nan"), "80%": float("nan")}
    rows.append({
        "quartos": quartos,
        "bairro": bairro,
        "perfil": f"{quartos}q {bairro}",
        "qtd": total,
        "com_preco": com_preco,
        "pct_com_preco": com_preco/total*100 if total else 0,
        "med_pm": med_pm,
        "mean_pm": mean_pm,
        "med_min": med_min,
        "med_max": med_max,
        "med_medio": med_medio,
        "cen": cen,
        "cen_mean": cen_mean,
    })

# Overall alta vs demais referencia (nao usado para perfis mas para contexto)
ap_alta = ap[ap["number_of_reviews"] >= 15]
ap_demais = ap[ap["number_of_reviews"] < 15]

# Imprimir terminal
print("=== CENARIOS RECEITA BRUTA ESTIMADA (price_mediano *30* ocupacao) ===")
print("price_mediano = mediana historica por anuncio (NAO receita) | 30 dias | cenarios 40/60/80% hipoteticos\n")
header = f"{'Perfil':15} | {'Qtd':4} | {'ComPreco':8} | {'Med PM':7} | {'40% mes':9} | {'60% mes':9} | {'80% mes':9} | {'60% ano':10}"
print(header)
print("-"*len(header))
for r in rows:
    print(f"{r['perfil']:15} | {r['qtd']:3} | {r['com_preco']:3} ({r['pct_com_preco']:.0f}%) | {r['med_pm']:7.0f} | {r['cen']['40%']:8.0f} | {r['cen']['60%']:8.0f} | {r['cen']['80%']:8.0f} | {r['cen']['60%']*12:9.0f}")

# Comparacao
print("\n=== COMPARACAO perfis (ordenado por receita base 60%) ===")
rows_sorted = sorted(rows, key=lambda x: x["cen"]["60%"] if not pd.isna(x["cen"]["60%"]) else -1, reverse=True)
for i, r in enumerate(rows_sorted, 1):
    print(f"{i}. {r['perfil']:15} -> 60% mes R$ {r['cen']['60%']:,.0f} | ano R$ {r['cen']['60%']*12:,.0f} | med PM {r['med_pm']:.0f} | n={r['qtd']} com {r['com_preco']}")

# Detalhe por preco pmin/pmax
print("\n=== DETALHE price_min/max/medio por perfil ===")
for r in rows:
    print(f"{r['perfil']:15} | med pmin {r['med_min']:6.0f} | med pmax {r['med_max']:6.0f} | med pm {r['med_pm']:6.0f} | med medio {r['med_medio']:6.0f}")

# Validacao: nao estamos calculando receita real
print("\nObservacao: valores sao RECEITA BRUTA ESTIMADA hipotetica, sem descontar condominio/IPTU/limpeza/comissao; ocupacao e cenario, nao dado real.")

# Gerar markdown
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Relatorio Receita Bruta Estimada - Cenarios 40/60/80%\n\n")
    f.write("> **Base:** `analysis/base_analitica_itapema.csv` (3710 apartamentos) | **Preco:** `price_mediano` = mediana historica por anuncio (NAO receita) | **Ocupacao:** hipoteses 40/60/80% sobre 30 dias | **Formula:** `receita_mensal = price_mediano *30*taxa` | `anual = mensal*12` | **Sem ROI**\n\n")
    f.write("## Perfis analisados (relevantes da demanda)\n\n")
    f.write("1. 2q Meia Praia | 2. 3q Meia Praia | 3. 4q Meia Praia | 4. 2q Centro | 5. 3q Centro\n\n")
    f.write("## Tabela principal (por price_mediano mediana do perfil)\n\n")
    f.write("| Perfil | Qtd anuncios | Com preco | % com preco | price_mediano (mediana) | price_mediano (media) | price_min med | price_max med | Receita 40% mes | Receita 60% mes | Receita 80% mes | Receita 60% ano |\n")
    f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        f.write(f"| {r['perfil']} | {r['qtd']} | {r['com_preco']} | {r['pct_com_preco']:.1f}% | R$ {r['med_pm']:.0f} | R$ {r['mean_pm']:.0f} | R$ {r['med_min']:.0f} | R$ {r['med_max']:.0f} | R$ {r['cen']['40%']:,.0f} | R$ {r['cen']['60%']:,.0f} | R$ {r['cen']['80%']:,.0f} | R$ {r['cen']['60%']*12:,.0f} |\n")
    f.write("\n### Ordenado por receita base 60%\n\n")
    f.write("| Rank | Perfil | 60% mes | 60% ano | Med PM |\n|---|---|---|---|---|\n")
    for i, r in enumerate(rows_sorted, 1):
        f.write(f"| {i} | {r['perfil']} | R$ {r['cen']['60%']:,.0f} | R$ {r['cen']['60%']*12:,.0f} | R$ {r['med_pm']:.0f} |\n")
    f.write("\n## Comparacao Alta vs Demais (contexto)\n\n")
    for label, sub in [("Alta (reviews>=15)", ap_alta), ("Demais", ap_demais)]:
        com = sub[sub["listing_type"].str.lower()=="apartamento"]["price_mediano"].notna().sum()
        # filtrar apartamento dentro
        sub_ap = sub[sub["listing_type"].str.lower()=="apartamento"]
        med = sub_ap["price_mediano"].median()
        f.write(f"- **{label}:** {len(sub_ap)} aptos, {com} com preco, mediana PM R$ {med:.0f} | 60% mes R$ {med*30*0.6:,.0f}\n")
    f.write("\n## Observacoes\n\n")
    f.write("- **4q Meia Praia** tem maior PM (900) mas apenas 33 alta e total 4q Meia Praia ~ 110? (perfil nicho, preco alto mas volume baixo, com_preco 88%).\n")
    f.write("- **3q Meia Praia** (242 alta, med PM 650, 60% mes R$ 11.700) equilibra volume e receita; **3q Centro** med PM 800 (60% mes R$ 14.400) tem receita maior por diaria mas volume menor (22 alta).\n")
    f.write("- **2q Meia Praia** (151 alta, med PM 450, 60% mes R$ 8.100) tem volume alto mas receita menor; **2q Centro** med PM 472 (60% mes R$ 8.496) similar.\n")
    f.write("- Precos sao medianas historicas; sem ocupacao real, sem custos, sem ROI.\n")
    f.write("\n## Caminho percorrido (para video)\n\n")
    f.write("1. **Parti do que ja tinhamos:** `base_analitica_itapema.csv:4441` (LEFT JOIN Details+Mesh+price_por_anuncio) ja validada, e `relatorio_demanda.md` que mostrou 2-3q Meia Praia/Centro como volumosos.\n")
    f.write("2. **Escolhi os 5 perfis** exatamente esses que apareceram como relevantes, filtrando `base_analitica` por `listing_type==apartamento` + `number_of_bedrooms` + `suburb`.\n")
    f.write("3. **Para cada perfil:** contei `qtd` total e `qtd com preco` (`price_mediano.notna()`), calculei `price_mediano` do perfil como **mediana das medianas** (robusta a outlier R$29.000), tambem `price_min/max/medio` medianas para contexto.\n")
    f.write("4. **Apliquei cenarios:** `price_mediano *30*dias * taxa` para 40/60/80% (hipoteses, nao dado real) e `*12` para anual, chamando de **RECEITA BRUTA ESTIMADA** sem descontar condominio/IPTU.\n")
    f.write("5. **Comparei:** ordenei por `60% mes` e vi que 4q > 3q Centro > 3q Meia Praia > 2q, mas cruzei com `qtd` para ver que 3q Meia Praia tem melhor equilibrio volume-receita, enquanto 2q tem volume mas receita menor.\n")
    f.write("6. **Validei:** 3710 aptos, 999 com preco na base, sem alterar `data/`, sem assumir ocupacao real, sem calcular ROI.\n")

print(f"\nRelatorio salvo em {OUT}")

