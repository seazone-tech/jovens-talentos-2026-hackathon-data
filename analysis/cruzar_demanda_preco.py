#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cruza demanda (reviews >=15) com precos - base_analitica_itapema.csv
Sem receita/ocupacao/ROI, apenas relacao demanda x preco
"""
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"

df = pd.read_csv(BASE, dtype={"airbnb_listing_id": str, "owner_id": str})
# Filtrar apartamento
ap = df[df["listing_type"].str.strip().str.lower() == "apartamento"].copy()
ap["number_of_reviews"] = pd.to_numeric(ap["number_of_reviews"], errors="coerce").fillna(0).astype(int)
ap["number_of_bedrooms"] = pd.to_numeric(ap["number_of_bedrooms"], errors="coerce")
ap["number_of_guests"] = pd.to_numeric(ap["number_of_guests"], errors="coerce")
ap["price_mediano"] = pd.to_numeric(ap["price_mediano"], errors="coerce")
ap["price_medio"] = pd.to_numeric(ap["price_medio"], errors="coerce")
ap["price_min"] = pd.to_numeric(ap["price_min"], errors="coerce")
ap["price_max"] = pd.to_numeric(ap["price_max"], errors="coerce")

# Alta demanda mesmo criterio anterior
alta = ap[ap["number_of_reviews"] >= 15].copy()
demais = ap[ap["number_of_reviews"] < 15].copy()

print(f"Apartamentos totais: {len(ap)} | Alta (reviews>=15): {len(alta)} | Demais: {len(demais)}")
print(f"Com preco: alta {alta['price_mediano'].notna().sum()}/{len(alta)} | demais {demais['price_mediano'].notna().sum()}/{len(demais)}")

def resumo_preco(subset, label):
    com = subset["price_mediano"].notna().sum()
    total = len(subset)
    if com == 0:
        return {"label": label, "qtd": total, "com_preco": com, "mediana_pm": np.nan, "media_pm": np.nan, "mediana_rev": subset["number_of_reviews"].median(), "mediana_pmin": np.nan, "mediana_pmax": np.nan}
    return {
        "label": label,
        "qtd": total,
        "com_preco": com,
        "mediana_pm": subset["price_mediano"].median(),
        "media_pm": subset["price_mediano"].mean(),
        "mediana_rev": subset["number_of_reviews"].median(),
        "mediana_pmin": subset["price_min"].median(),
        "mediana_pmax": subset["price_max"].median(),
        "media_pmax": subset["price_max"].mean(),
        "mediana_medio": subset["price_medio"].median(),
    }

# Overall alta vs demais
print("\n=== OVERALL Alta vs Demais (price_mediano) ===")
for lab, sub in [("Alta", alta), ("Demais", demais), ("Todos aptos", ap)]:
    r = resumo_preco(sub, lab)
    print(f"{r['label']:12} n={r['qtd']:4} com_preco={r['com_preco']:3} | mediana price_mediano={r['mediana_pm']:.0f} | media={r['media_pm']:.0f} | mediana reviews={r['mediana_rev']:.0f} | mediana pmin={r['mediana_pmin']:.0f} pmax={r['mediana_pmax']:.0f}")

# Por quartos
print("\n=== POR QUARTOS (todos aptos) ===")
print(f"{'Quartos':7} | {'Qtd':5} | {'ComPreco':8} | {'Mediana PM':11} | {'Media PM':10} | {'Mediana Rev':12} | {'Mediana pmin/pmax'}")
for q in sorted(ap["number_of_bedrooms"].dropna().unique()):
    sub = ap[ap["number_of_bedrooms"]==q]
    r = resumo_preco(sub, f"{int(q)}q")
    print(f"{int(q):2}q      | {r['qtd']:4} | {r['com_preco']:4} ({r['com_preco']/r['qtd']*100:.0f}%) | {r['mediana_pm']:8.0f} | {r['media_pm']:8.0f} | {r['mediana_rev']:6.0f} | {r['mediana_pmin']:.0f}/{r['mediana_pmax']:.0f}")

print("\n=== POR QUARTOS - SÓ ALTA ===")
for q in sorted(alta["number_of_bedrooms"].dropna().unique()):
    sub = alta[alta["number_of_bedrooms"]==q]
    r = resumo_preco(sub, f"{int(q)}q alta")
    print(f"{int(q):2}q alta | {r['qtd']:3} | com {r['com_preco']:3} | med PM {r['mediana_pm']:6.0f} | media {r['media_pm']:6.0f} | med rev {r['mediana_rev']:4.0f}")

# Por hospedes
print("\n=== POR CAPACIDADE HOSPEDES (todos) ===")
for g in sorted(ap["number_of_guests"].dropna().unique()):
    if g>10: continue
    sub = ap[ap["number_of_guests"]==g]
    if len(sub)<20: continue
    r = resumo_preco(sub, f"{int(g)}")
    print(f"{int(g):2} hosp | n={r['qtd']:4} com={r['com_preco']:3} | med PM {r['mediana_pm']:6.0f} | rev {r['mediana_rev']:4.0f}")

print("\n=== POR CAPACIDADE - ALTA ===")
for g in sorted(alta["number_of_guests"].dropna().unique()):
    if g>10: continue
    sub = alta[alta["number_of_guests"]==g]
    if len(sub)<15: continue
    r = resumo_preco(sub, f"{int(g)}")
    print(f"{int(g):2} hosp alta | n={r['qtd']:3} | med PM {r['mediana_pm']:6.0f} | rev {r['mediana_rev']:3.0f}")

# Por bairro
print("\n=== POR BAIRRO (todos aptos) ===")
for b in ["Meia Praia","Centro","Morretes","Tabuleiro dos Oliveiras","Casa Branca","Alto Sao Bento","Ilhota"]:
    sub = ap[ap["suburb"]==b]
    if len(sub)==0: continue
    r = resumo_preco(sub, b)
    print(f"{b:25} | n={r['qtd']:4} com={r['com_preco']:3} ({r['com_preco']/r['qtd']*100:.0f}%) | med PM {r['mediana_pm']:6.0f} | media {r['media_pm']:6.0f} | rev {r['mediana_rev']:4.0f} | pmax med {r['mediana_pmax']:6.0f}")

print("\n=== POR BAIRRO - ALTA ===")
for b in ["Meia Praia","Centro","Morretes"]:
    sub = alta[alta["suburb"]==b]
    r = resumo_preco(sub, b+" alta")
    print(f"{b:15} alta | n={r['qtd']:3} com={r['com_preco']:3} | med PM {r['mediana_pm']:6.0f} | rev {r['mediana_rev']:3.0f} | pmin {r['mediana_pmin']:4.0f} pmax {r['mediana_pmax']:4.0f}")

# Combinacao relevante: quartos x bairro (para alta)
print("\n=== COMBINACAO QUARTOS x BAIRRO - ALTA (n>=20) ===")
comb = alta.groupby(["number_of_bedrooms","suburb"])
rows=[]
for (q,b), g in comb:
    if len(g)<20: continue
    r = resumo_preco(g, f"{int(q)}q {b}")
    rows.append((q,b,len(g), g["price_mediano"].notna().sum(), r["mediana_pm"], r["media_pm"], r["mediana_rev"], r["mediana_pmax"]))
rows = sorted(rows, key=lambda x: x[5], reverse=True)  # por media
print(f"{'Perfil':20} | {'Qtd':3} | {'ComPreco':8} | {'Mediana PM':10} | {'Media PM':9} | {'Med Rev':7} | {'Med pmax'}")
for q,b,n,com,med,mean,rev,pmax in rows:
    print(f"{int(q)}q {b:12} | {n:3} | {com:3} ({com/n*100:.0f}%) | {med:8.0f} | {mean:8.0f} | {rev:5.0f} | {pmax:6.0f}")

# Extra: quartos x hospedes para alta
print("\n=== COMPARATIVO ALTA vs DEMAIS por preco (price_mediano) ===")
# Mostrar que alta consegue cobrar mais?
# Calcular diferenca media
med_alta = alta["price_mediano"].median()
med_demais = demais["price_mediano"].median()
mean_alta = alta["price_mediano"].mean()
mean_demais = demais["price_mediano"].mean()
print(f"Alta  mediana price_mediano {med_alta:.0f} (n={alta['price_mediano'].notna().sum()}) | media {mean_alta:.0f}")
print(f"Demais mediana {med_demais:.0f} (n={demais['price_mediano'].notna().sum()}) | media {mean_demais:.0f}")
print(f"Diferenca mediana (Alta-Demais): {med_alta-med_demais:+.0f} | diferenca media {mean_alta-mean_demais:+.0f}")

# Salvar markdown
out = ROOT / "reports" / "01_pergunta1_perfil/relatorio_demanda_preco.md"
with open(out, "w", encoding="utf-8") as f:
    f.write("# Demanda x Preco - Apartamentos Itapema\n\n")
    f.write("> Base `base_analitica_itapema.csv` | Alta = `reviews>=15` (625) vs Demais 3085 | Preco = `price_mediano` (mediana historica por anuncio, nao receita)\n\n")
    f.write(f"Apartamentos totais 3710 | Alta 625 | Demais 3085 | Com preco: alta {alta['price_mediano'].notna().sum()} | demais {demais['price_mediano'].notna().sum()}\n\n")
    f.write("## Overall\n")
    f.write("| Perfil | Qtd | Com preco | Mediana PM | Media PM | Mediana reviews | Mediana pmin | Mediana pmax |\n|---|---|---|---|---|---|---|---|\n")
    for lab, sub in [("Alta", alta), ("Demais", demais), ("Todos", ap)]:
        r = resumo_preco(sub, lab)
        f.write(f"| {lab} | {r['qtd']} | {r['com_preco']} | {r['mediana_pm']:.0f} | {r['media_pm']:.0f} | {r['mediana_rev']:.0f} | {r['mediana_pmin']:.0f} | {r['mediana_pmax']:.0f} |\n")
    f.write("\n## Por quartos (todos)\n")
    f.write("| Quartos | Qtd | Com preco | Mediana PM | Media PM | Mediana rev | pmin/pmax |\n|---|---|---|---|---|---|---|\n")
    for q in sorted(ap["number_of_bedrooms"].dropna().unique()):
        sub = ap[ap["number_of_bedrooms"]==q]
        r = resumo_preco(sub, "")
        f.write(f"| {int(q)}q | {r['qtd']} | {r['com_preco']} ({r['com_preco']/r['qtd']*100:.0f}%) | {r['mediana_pm']:.0f} | {r['media_pm']:.0f} | {r['mediana_rev']:.0f} | {r['mediana_pmin']:.0f}/{r['mediana_pmax']:.0f} |\n")
    f.write("\n## Por bairro (todos)\n")
    f.write("| Bairro | Qtd | Com preco | Mediana PM | Media PM | Mediana rev |\n|---|---|---|---|---|---|\n")
    for b in ["Meia Praia","Centro","Morretes","Tabuleiro dos Oliveiras","Casa Branca"]:
        sub = ap[ap["suburb"]==b]
        if len(sub)==0: continue
        r = resumo_preco(sub, b)
        f.write(f"| {b} | {r['qtd']} | {r['com_preco']} | {r['mediana_pm']:.0f} | {r['media_pm']:.0f} | {r['mediana_rev']:.0f} |\n")
    f.write("\n## Combinacao quartos x bairro - Alta (n>=20)\n")
    f.write("| Perfil | Qtd | Com preco | Mediana PM | Media PM | Med rev | Med pmax |\n|---|---|---|---|---|---|---|\n")
    for q,b,n,com,med,mean,rev,pmax in rows:
        f.write(f"| {int(q)}q {b} | {n} | {com} | {med:.0f} | {mean:.0f} | {rev:.0f} | {pmax:.0f} |\n")
    f.write("\n## Observacoes\n")
    f.write("- Preco mediano e historico por anuncio (price_mediano), nao receita; sem ocupacao.\n")
    f.write("- Alta consegue cobrar levemente mais na mediana, mas diferenca vem mais de perfil 3-4q e Centro/Morretes com pmax maior.\n")
    f.write("- Studio/1q tem volume pequeno e preco mediano menor, mas amostra com preco pequena.\n")

print(f"\nRelatorio salvo em {out}")

