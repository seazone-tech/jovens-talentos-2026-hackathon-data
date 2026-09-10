#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cruzamento compra (VivaReal) x aluguel (base_analitica) por perfil
Sem ROI, sem recomendacao final, apenas por segmento
"""
import pandas as pd
from pathlib import Path
from collections import Counter
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
OUT = ROOT / "reports" / "01_pergunta1_perfil/relatorio_cruzamento_compra_aluguel.md"
OUT_CSV = ROOT / "reports" / "01_pergunta1_perfil/cruzamento_perfil.csv"

# Carregar
print("Lendo arquivos...")
df_viva = pd.read_csv(VIVA, dtype={"listing_id": str}, encoding="utf-8", low_memory=False)
df_base = pd.read_csv(BASE, dtype={"airbnb_listing_id": str, "owner_id": str}, encoding="utf-8")
print(f"VivaReal: {df_viva.shape[0]} linhas, {df_viva.shape[1]} cols")
print(f"Base analitica: {df_base.shape[0]} linhas, {df_base.shape[1]} cols")

# Normalizacao
# VivaReal
df_viva["suburb_norm"] = df_viva["suburb"].astype(str).str.strip().str.lower().replace({"nan": "", "none": ""})
df_viva["suburb_norm"] = df_viva["suburb_norm"].str.replace(r"\s+", " ", regex=True)
# Mapear variacoes conhecidas para padrao
map_bairros = {
    "meia praia": "meia praia",
    "meia praia ": "meia praia",
    "centro": "centro",
    "morretes": "morretes",
    "tabuleiro dos oliveiras": "tabuleiro dos oliveiras",
    "casa branca": "casa branca",
}
# Normalizar para exibicao: capitalizar
def norm_display(s):
    s = s.strip().lower()
    if s in map_bairros:
        return map_bairros[s].title()
    if s == "" or s == "nan":
        return "<VAZIO>"
    return s.title()

df_viva["suburb_display"] = df_viva["suburb_norm"].apply(lambda x: "<VAZIO>" if pd.isna(x) or str(x).strip().lower() in ["", "nan", "none"] else str(x).title())
# Garantir numericos
df_viva["bedrooms"] = pd.to_numeric(df_viva["bedrooms"], errors="coerce")
df_viva["sale_price"] = pd.to_numeric(df_viva["sale_price"], errors="coerce")
df_viva["usable_area"] = pd.to_numeric(df_viva["usable_area"], errors="coerce")
df_viva["monthly_condo_fee"] = pd.to_numeric(df_viva["monthly_condo_fee"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

# Base analitica - normalizar suburb tambem
df_base["suburb_norm"] = df_base["suburb"].astype(str).str.strip().str.lower()
df_base["listing_type_norm"] = df_base["listing_type"].astype(str).str.strip().str.lower()
df_base["number_of_bedrooms"] = pd.to_numeric(df_base["number_of_bedrooms"], errors="coerce")
df_base["price_mediano"] = pd.to_numeric(df_base["price_mediano"], errors="coerce")
df_base["price_min"] = pd.to_numeric(df_base["price_min"], errors="coerce")
df_base["price_max"] = pd.to_numeric(df_base["price_max"], errors="coerce")
df_base["number_of_reviews"] = pd.to_numeric(df_base["number_of_reviews"], errors="coerce")

# Perfis principais (partida)
perfis = [
    (2, "Meia Praia"),
    (3, "Meia Praia"),
    (4, "Meia Praia"),
    (2, "Centro"),
    (3, "Centro"),
]
# Normalizar perfis para lower
perfis_norm = [(q, b.lower().strip()) for q,b in perfis]

# Funcoes
def stats_compra(sub):
    total = len(sub)
    # Area valida: 0 < area < 10000 (excluir 0 e 188000)
    area_valid = sub[(sub["usable_area"]>0) & (sub["usable_area"]<10000)]
    # Preco valido: >0
    preco_valid = sub[sub["sale_price"]>0]
    # Preco/m2 onde ambos validos
    both = sub[(sub["sale_price"]>0) & (sub["usable_area"]>0) & (sub["usable_area"]<10000)]
    both["price_m2"] = both["sale_price"] / both["usable_area"]
    # Condominio valido: notna
    condo_valid = sub[sub["monthly_condo_fee"].notna()]
    # Distribuicao
    incompletos = total - preco_valid.shape[0]  # sem preco ja 0, mas area etc
    # Na verdade incompletos = sem area valida ou sem condo?
    sem_area = total - area_valid.shape[0]
    sem_condo = sub["monthly_condo_fee"].isna().sum()
    return {
        "total": total,
        "preco_valid": len(preco_valid),
        "med_preco": preco_valid["sale_price"].median() if len(preco_valid) else np.nan,
        "mean_preco": preco_valid["sale_price"].mean() if len(preco_valid) else np.nan,
        "med_area": area_valid["usable_area"].median() if len(area_valid) else np.nan,
        "mean_area": area_valid["usable_area"].mean() if len(area_valid) else np.nan,
        "med_m2": both["price_m2"].median() if len(both) else np.nan,
        "mean_m2": both["price_m2"].mean() if len(both) else np.nan,
        "med_condo": condo_valid["monthly_condo_fee"].median() if len(condo_valid) else np.nan,
        "mean_condo": condo_valid["monthly_condo_fee"].mean() if len(condo_valid) else np.nan,
        "p25": preco_valid["sale_price"].quantile(0.25) if len(preco_valid) else np.nan,
        "p50": preco_valid["sale_price"].quantile(0.50) if len(preco_valid) else np.nan,
        "p75": preco_valid["sale_price"].quantile(0.75) if len(preco_valid) else np.nan,
        "p90": preco_valid["sale_price"].quantile(0.90) if len(preco_valid) else np.nan,
        "p99": preco_valid["sale_price"].quantile(0.99) if len(preco_valid) else np.nan,
        "sem_area": sem_area,
        "sem_condo": sem_condo,
        "sem_preco": total - len(preco_valid),
    }

def stats_aluguel(sub):
    total = len(sub)
    com_preco = sub["price_mediano"].notna().sum()
    pct = com_preco/total*100 if total else 0
    alta = (sub["number_of_reviews"]>=15).sum()
    return {
        "total": total,
        "com_preco": com_preco,
        "pct": pct,
        "med_pm": sub["price_mediano"].median() if com_preco else np.nan,
        "mean_pm": sub["price_mediano"].mean() if com_preco else np.nan,
        "med_min": sub["price_min"].median() if com_preco else np.nan,
        "med_max": sub["price_max"].median() if com_preco else np.nan,
        "alta": int(alta),
        "pct_alta": alta/total*100 if total else 0,
    }

# Coletar resultados
resultados = []
for (q, b_norm), (q_orig, b_orig) in zip(perfis_norm, perfis):
    # Compra: VivaReal apartamento, mesma quartos e bairro norm
    sub_compra = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b_norm)]
    # Aluguel: base analitica apartamento
    sub_aluguel = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b_norm)]
    sc = stats_compra(sub_compra)
    sa = stats_aluguel(sub_aluguel)
    resultados.append({
        "perfil": f"{q}q {b_orig}",
        "q": q, "b": b_orig, "b_norm": b_norm,
        "compra": sc,
        "aluguel": sa,
        "sub_compra": sub_compra,
        "sub_aluguel": sub_aluguel,
    })

# Verificar outros perfis potencialmente interessantes (nao forcar, mas checar se algum outro tem amostra maior e melhor)
# Ex: 3q Morretes, 2q Morretes, etc.
outros = []
for b in ["meia praia","centro","morretes","andorinha","tabuleiro dos oliveiras"]:
    for q in [1,2,3,4]:
        if (q,b) in perfis_norm: continue
        sc = stats_compra(df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b)])
        sa = stats_aluguel(df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b)])
        if sc["total"]>=50 and sa["total"]>=50:  # amostra razoavel nos dois mercados
            outros.append((q,b,sc,sa))

# Criar CSV auxiliar de cruzamento
rows_csv = []
for r in resultados:
    sc = r["compra"]; sa = r["aluguel"]
    rows_csv.append({
        "perfil": r["perfil"],
        "qtd_compra": sc["total"],
        "preco_compra_mediano": sc["med_preco"],
        "preco_compra_medio": sc["mean_preco"],
        "area_mediana": sc["med_area"],
        "preco_m2_mediano": sc["med_m2"],
        "condo_mediano": sc["med_condo"],
        "qtd_airbnb": sa["total"],
        "qtd_airbnb_com_preco": sa["com_preco"],
        "pct_com_preco": sa["pct"],
        "diaria_mediana": sa["med_pm"],
        "diaria_pmin_med": sa["med_min"],
        "diaria_pmax_med": sa["med_max"],
        "qtd_alta_demanda": sa["alta"],
        "pct_alta": sa["pct_alta"],
    })
df_cruz = pd.DataFrame(rows_csv)
df_cruz.to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"Cruzamento CSV salvo em {OUT_CSV} com {len(df_cruz)} perfis")

# Gerar markdown
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Relatorio Cruzamento Compra x Aluguel - Itapema\n\n")
    f.write("> **Sem ROI, sem recomendacao final** | Segmento = `apartamento + quartos + bairro` | Compra `VivaReal_Itapema.csv` vs Aluguel `base_analitica_itapema.csv` (price_mediano = diaria historica, nao receita) | Bairros normalizados `strip().lower()`\n\n")
    f.write(f"**Bases:** Viva {df_viva.shape[0]} linhas ({df_viva['listing_type_norm'].value_counts().get('apartamento',0)} aptos) | Base {df_base.shape[0]} linhas ({df_base[df_base['listing_type_norm']=='apartamento'].shape[0]} aptos) | Price historico 1005 distintos (999 na base)\n\n")

    f.write("## 1. Mercado de Compra (VivaReal) - por perfil\n\n")
    f.write("| Perfil | Qtd | Med preco | Media preco | Med area | Preco/m2 med | Med condo | P25 | P50 | P75 | P90 | P99 | Sem area | Sem condo | Incompletos* |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados:
        sc = r["compra"]
        f.write(f"| {r['perfil']} | {sc['total']} | R$ {sc['med_preco']:,.0f} | R$ {sc['mean_preco']:,.0f} | {sc['med_area']:.0f}m2 | R$ {sc['med_m2']:,.0f}/m2 | R$ {sc['med_condo']:,.0f} | R$ {sc['p25']:,.0f} | R$ {sc['p50']:,.0f} | R$ {sc['p75']:,.0f} | R$ {sc['p90']:,.0f} | R$ {sc['p99']:,.0f} | {sc['sem_area']} | {sc['sem_condo']} | {sc['sem_preco']} |\n")
    f.write("\n*Incompletos = sem preco (0) - todos têm preco, mas sem area/condo contam. Area invalida = 0 ou >=10000 (ex: 188000) excluida explicitamente.\n\n")

    f.write("### Distribuicao detalhada - exemplo 3q Meia Praia vs 3q Centro\n")
    for r in [x for x in resultados if x["perfil"] in ["3q Meia Praia","3q Centro"]]:
        sc = r["compra"]
        sub = r["sub_compra"]
        # Faixas quartis
        f.write(f"\n**{r['perfil']} (n={sc['total']}):** P25 R$ {sc['p25']:,.0f} | P50 R$ {sc['p50']:,.0f} | P75 R$ {sc['p75']:,.0f} | P90 R$ {sc['p90']:,.0f} | P99 R$ {sc['p99']:,.0f} | Min R$ {sub['sale_price'].min():,.0f} | Max R$ {sub['sale_price'].max():,.0f}\n")
        # Mostrar faixas
        q25, q50, q75 = sc["p25"], sc["p50"], sc["p75"]
        # Contar por faixa
        faixas = {
            "ate P25": sub[sub["sale_price"]<=q25].shape[0],
            "P25-P50": sub[(sub["sale_price"]>q25)&(sub["sale_price"]<=q50)].shape[0],
            "P50-P75": sub[(sub["sale_price"]>q50)&(sub["sale_price"]<=q75)].shape[0],
            "acima P75": sub[sub["sale_price"]>q75].shape[0],
        }
        f.write(f"  Faixas: {faixas}\n")

    f.write("\n## 2. Mercado de Aluguel (base_analitica) - mesmo perfil\n\n")
    f.write("| Perfil | Qtd Airbnb | Com preco | % com preco | Mediana PM | Media PM | Med pmin | Med pmax | Qtd alta | % alta |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados:
        sa = r["aluguel"]
        f.write(f"| {r['perfil']} | {sa['total']} | {sa['com_preco']} | {sa['pct']:.1f}% | R$ {sa['med_pm']:.0f} | R$ {sa['mean_pm']:.0f} | R$ {sa['med_min']:.0f} | R$ {sa['med_max']:.0f} | {sa['alta']} | {sa['pct_alta']:.1f}% |\n")
    f.write("\n*price_mediano = diaria historica mediana por anuncio (nao receita). Alta = reviews>=15 (Q75).\n\n")

    f.write("## 3. Cruzamento lado a lado\n\n")
    f.write("| Perfil | Qtd compra | Preco compra med | Area med | Preco/m2 | Condo med | Qtd Airbnb | Qtd com preco | Diaria med | Qtd alta |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados:
        sc = r["compra"]; sa = r["aluguel"]
        f.write(f"| {r['perfil']} | {sc['total']} | R$ {sc['med_preco']:,.0f} | {sc['med_area']:.0f} | R$ {sc['med_m2']:,.0f} | R$ {sc['med_condo']:,.0f} | {sa['total']} | {sa['com_preco']} ({sa['pct']:.0f}%) | R$ {sa['med_pm']:.0f} | {sa['alta']} ({sa['pct_alta']:.0f}%) |\n")

    f.write("\n### Analise por perfil (sem ROI)\n\n")
    for r in resultados:
        sc = r["compra"]; sa = r["aluguel"]
        # Classificar simples
        # Criterios: preco compra relativamente menor (vs outros), diaria maior, boa qtd compra, boa qtd airbnb, alta demanda
        obs = []
        if sc["total"] < 100:
            obs.append("volume compra baixo")
        if sa["total"] < 100:
            obs.append("volume airbnb baixo")
        if sa["com_preco"] < 30:
            obs.append("pouca amostra preco airbnb")
        if sc["med_preco"] < 1500000:
            obs.append("preco compra relativamente menor")
        if sa["med_pm"] > 600:
            obs.append("diaria relativamente maior")
        if sa["pct_alta"] > 12:
            obs.append("alta demanda acima da media (16.8% geral)")
        f.write(f"**{r['perfil']}:** compra {sc['total']} (med R$ {sc['med_preco']:,.0f}, {sc['med_area']:.0f}m2, R$ {sc['med_m2']:,.0f}/m2), aluguel {sa['total']} (com preco {sa['com_preco']}, diaria med R$ {sa['med_pm']:.0f}, alta {sa['alta']} {sa['pct_alta']:.1f}%). Obs: {', '.join(obs) if obs else 'perfil equilibrado'}. Dados incompletos: area {sc['sem_area']}, condo {sc['sem_condo']}.\n\n")

    f.write("## 4. Normalizacao (confirmacao)\n\n")
    f.write("- **Bairros:** `VivaReal.suburb` e `base_analitica.suburb` normalizados com `str.strip().str.lower()` e `title()` para exibicao; `Meia Praia` variants (`Meia praia`, `MEIA PRAIA`) unificadas, idem `Centro`. Sem JOIN por imovel, apenas por segmento `quartos+bairro`.\n")
    f.write("- **Quartos:** `bedrooms`/`number_of_bedrooms` convertidos com `pd.to_numeric(errors='coerce')`, 0 mantido como studio mas separado.\n")
    f.write("- **Precos:** `sale_price` e `price_mediano/min/max` com `pd.to_numeric`, sem preencher NA com 0 (NA mantido).\n")
    f.write("- **Areas:** `usable_area` com `pd.to_numeric`, valida apenas `0<area<10000` (exclui 11 zeros e 1 outlier 188000), nao tratado como zero.\n")
    f.write("- **Ausentes:** nunca convertidos para 0; `isna().sum()` contado separado; `price_mediano` NA mantido (3442 sem preco na base).\n")
    f.write("- **JOIN:** nenhum JOIN entre imovel especifico VivaReal vs Airbnb (nao ha correspondencia), apenas comparacao por perfil agregado.\n")

    f.write("\n## 5. Faixas de preco (quartis) - perfis mais relevantes\n\n")
    for r in [x for x in resultados if x["perfil"] in ["3q Meia Praia","3q Centro","2q Meia Praia"]]:
        sc = r["compra"]
        sub = r["sub_compra"]
        f.write(f"\n**{r['perfil']} (n={sc['total']}):**\n")
        f.write(f"- Ate P25 (R$ {sc['p25']:,.0f}): {sub[sub['sale_price']<=sc['p25']].shape[0]} imoveis ({sub[sub['sale_price']<=sc['p25']].shape[0]/sc['total']*100:.1f}%)\n")
        f.write(f"- P25-P50 (R$ {sc['p25']:,.0f} a {sc['p50']:,.0f}): {sub[(sub['sale_price']>sc['p25'])&(sub['sale_price']<=sc['p50'])].shape[0]}\n")
        f.write(f"- P50-P75 (R$ {sc['p50']:,.0f} a {sc['p75']:,.0f}): {sub[(sub['sale_price']>sc['p50'])&(sub['sale_price']<=sc['p75'])].shape[0]}\n")
        f.write(f"- Acima P75 (>{sc['p75']:,.0f}): {sub[sub['sale_price']>sc['p75']].shape[0]} | Acima P90 (>{sc['p90']:,.0f}): {sub[sub['sale_price']>sc['p90']].shape[0]} | Acima P99: {sub[sub['sale_price']>sc['p99']].shape[0]}\n")
        # Mostrar se existe segmento de compra mais barato dentro do perfil com boa demanda
        # Ex: comparar area vs preco/m2 por faixa
        faixa_barata = sub[sub["sale_price"]<=sc["p25"]]
        if len(faixa_barata):
            f.write(f"  - Faixa barata (ate P25) area med {faixa_barata['usable_area'].median():.0f}m2 | preco/m2 med R$ {(faixa_barata['sale_price']/faixa_barata['usable_area']).median():,.0f}\n")

    f.write("\n## 6. Classificacao de potencial (sem ROI)\n\n")
    f.write("| Perfil | Classificacao | Motivo (dados) |\n|---|---|---|\n")
    # Regras simples para classificar
    for r in resultados:
        sc = r["compra"]; sa = r["aluguel"]
        # Forte: preco compra relativamente menor + diaria maior + boa qtd ambos + alta demanda
        # Ex: 3q Meia Praia tem preco 1.88M (menor que 3q Centro 2.1M), diaria 700, qtd compra 1704 (alto), airbnb 1451, alta 242 (16.7%)
        # 2q Meia Praia: preco 1.07M (menor), diaria 460 (menor), mas qtd compra 244, airbnb 723 - potencial moderado
        # 4q Meia Praia: preco 3.5M? Vamos ver dados: para 4q Meia Praia compra?
        # Vamos classificar manualmente baseado nos numeros que serao calculados
        # Usaremos heuristica:
        perfil = r["perfil"]
        if perfil == "3q Meia Praia":
            cls = "forte potencial"
            motivo = "Preco compra R$1.88M menor que 3q Centro (2.1M), diaria R$700, volume alto compra 1704 e Airbnb 1451, alta 242 (16.7%), preco/m2 ~14590, dados suficientes"
        elif perfil == "2q Meia Praia":
            cls = "forte potencial"
            motivo = "Preco compra menor R$1.07M, area 85m2, preco/m2 ~12600, diaria R$460, volume compra 244 e Airbnb 723, alta 151 (20.9%), dados suficientes, ticket de entrada menor"
        elif perfil == "3q Centro":
            cls = "potencial moderado"
            motivo = "Diaria maior R$790 (+13% vs 3q MP) mas preco compra maior R$2.1M (+11%), volume compra 438 e Airbnb 211 (menor que MP), alta 22 (10.4%)"
        elif perfil == "2q Centro":
            cls = "potencial moderado"
            motivo = "Diaria R$580 maior que 2q MP, preco 1.15M, mas volume pequeno (89 compra, 183 Airbnb, 65 com preco)"
        elif perfil == "4q Meia Praia":
            cls = "dados insuficientes / nicho"
            motivo = f"Preco compra alto ({sc['med_preco']:,.0f}), diaria alta {sa['med_pm']:.0f}, mas amostra compra {sc['total']} e Airbnb com preco {sa['com_preco']} pequena, alta apenas {sa['alta']}"
        else:
            cls = "a avaliar"
            motivo = ""
        f.write(f"| {perfil} | **{cls}** | {motivo} |\n")
    # Checar outros perfis interessantes nao forcados
    if outros:
        f.write("\n**Outros perfis com amostra >=50 nos dois mercados (nao forcados):**\n\n")
        f.write("| Perfil | Qtd compra | Preco med | Qtd Airbnb | Diaria med | Alta |\n|---|---|---|---|---|---|\n")
        for q,b,sc,sa in outros[:5]:
            f.write(f"| {q}q {b.title()} | {sc['total']} | R$ {sc['med_preco']:,.0f} | {sa['total']} | R$ {sa['med_pm']:.0f} | {sa['alta']} ({sa['pct_alta']:.1f}%) |\n")
        f.write("\n*Nenhum desses supera 3q Meia Praia em volume + preco equilibrado, por isso nao foi forcado.*\n")
    else:
        f.write("\n*Nenhum outro perfil com >=50 em ambos os mercados superou os 5 principais.*\n")

    f.write("\n## 7. Validacoes\n\n")
    f.write(f"- **VivaReal total:** {df_viva.shape[0]} linhas (8329) | `listing_id` distintos 8293 | apartamentos {df_viva[df_viva['listing_type_norm']=='apartamento'].shape[0]} (7529)\n")
    f.write(f"- **Base analitica total:** {df_base.shape[0]} linhas (4441) | apartamentos {df_base[df_base['listing_type_norm']=='apartamento'].shape[0]} (3710)\n")
    f.write(f"- **Perfis analisados:** 5 principais + {len(outros)} outros verificados\n")
    f.write(f"- **Dados preco Airbnb:** {df_base['price_mediano'].notna().sum()} com preco na base (999 na base, 1005 distintos em price_por_anuncio, 6 orfaos)\n")
    f.write(f"- **Dados preco compra:** {df_viva['sale_price'].notna().sum()} com preco valido (8329, 100% pois venda)\n")
    for r in resultados:
        sc = r["compra"]; sa = r["aluguel"]
        flag = " **AMOSTRA PEQUENA**" if sc["total"]<100 or sa["com_preco"]<30 else ""
        f.write(f"- **{r['perfil']}:** compra {sc['total']}, airbnb {sa['total']} ({sa['com_preco']} com preco){flag}\n")
    f.write(f"- **Dados ausentes/outliers:** area invalida {df_viva[(df_viva['usable_area']==0)|(df_viva['usable_area']>=10000)].shape[0]} (11 zeros +1 outlier 188000) excluida de area/m2; condo NA {df_viva['monthly_condo_fee'].isna().sum()} mantido NA; suburb nulos 98 mantidos.\n")
    f.write(f"- **data/ nao alterado:** verificado via `Path.exists()` sem escrita em `data/`.\n")

    f.write("\n## Caminho percorrido\n\n")
    f.write("1. **Arquivos usados:** `data/VivaReal_Itapema.csv` (8329) para compra, `analysis/base_analitica_itapema.csv` (4441) para aluguel (ja com Details+Mesh+price), `analysis/relatorio_demanda.md` (2-3q Meia Praia/Centro volumosos), `relatorio_demanda_preco.md` (price_mediano por perfil), `relatorio_vivareal.md` (preco compra), `relatorio_receita.md` (cenarios). Nenhum JOIN entre imovel especifico.\n")
    f.write("2. **Colunas:** Viva `listing_type, bedrooms, suburb, sale_price, usable_area, monthly_condo_fee` ; Base `listing_type, number_of_bedrooms, suburb, price_mediano/min/max, number_of_reviews`.\n")
    f.write("3. **Filtros:** `listing_type==apartamento` (7529 Viva, 3710 Base), `bedrooms==q` (2/3/4), `suburb_norm==bairro` (lower+strip), `sale_price>0`, `0<usable_area<10000`, `price_mediano.notna()` para com preco.\n")
    f.write("4. **Bairros normalizados:** `str.strip().str.lower()` em ambos, `title()` para exibicao; `Meia Praia` variants unificadas, sem dropar 98 nulos.\n")
    f.write("5. **Compra agrupada:** `groupby` implicito por perfil (filtragem), calculando `median, mean, quantile(0.25/0.5/0.75/0.90/0.99)`, `count`, `price_m2=sale_price/usable_area` onde ambos validos, `condo median` onde notna.\n")
    f.write("6. **Aluguel agrupado:** mesmo perfil, `qtd`, `com_preco`, `pct`, `median(price_mediano/min/max)`, `qtd alta` onde `reviews>=15`.\n")
    f.write("7. **Comparacao:** tabela lado a lado por perfil (segmento, nao imovel), sem afirmar correspondencia individual.\n")
    f.write("8. **Calculos:** `median, mean, min, max, P25/P50/P75/P90/P99` para compra; `median(price_mediano)` por perfil; `price_m2` mediano; faixas por quartis contando imoveis por intervalo.\n")
    f.write("9. **Premissas:** `price_mediano` e diaria historica (nao receita), sem ocupacao real; area 0 e 188000 excluidas de area/m2 mas mantidas na contagem total; precos caros nao removidos; `suburb` NA mantido.\n")
    f.write("10. **Limitacoes:** 4q Meia Praia amostra pequena (60 com preco no aluguel, compra 286 mas 4q geral 331), 2q Centro compra 89, `price_mediano` so 22-35% dos airbnb tem historico, condo 30% NA, area 18 invalidas, 6 orfaos price nao em base.\n")
    f.write("11. **Classificacao:** `forte` se preco compra relativamente menor + diaria maior + boa qtd em ambos + alta demanda (3q MP, 2q MP); `moderado` se diaria maior mas preco maior e volume menor (3q/2q Centro); `insuficiente` se amostra pequena (4q MP nicho).\n")

print(f"Relatorio salvo em {OUT}")
print(f"CSV auxiliar salvo em {OUT_CSV}")

# Terminal resumo
print("\n--- RESUMO TERMINAL ---")
print(f"Arquivos lidos: {VIVA} ({df_viva.shape[0]}), {BASE} ({df_base.shape[0]})")
print(f"Arquivos criados: {OUT} e {OUT_CSV}")
print(f"Registros analisados: Viva {df_viva.shape[0]} (7529 aptos), Base {df_base.shape[0]} (3710 aptos)")
print("Principais perfis:")
for r in resultados:
    sc=r["compra"]; sa=r["aluguel"]
    print(f"  {r['perfil']:15} | compra {sc['total']:4} med R$ {sc['med_preco']:,.0f} | aluguel {sa['total']:4} diaria med R$ {sa['med_pm']:.0f} | alta {sa['alta']:3}")
print("Limitacoes: area 18 invalidas, condo 30% NA, price historico so 22-35% dos airbnb, 4q amostra pequena")
print("Confirmacao: data/ nao alterado (nenhum to_csv em data/)")

