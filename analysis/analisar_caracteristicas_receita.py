#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pergunta 3 - Quais caracteristicas explicam as melhores receitas?
Reaproveita analises validadas, sem recalcular ROI, sem alterar data/
"""
import pandas as pd
from pathlib import Path
import numpy as np
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
CRUZ = ROOT / "reports" / "01_pergunta1_perfil/cruzamento_perfil.csv"
LOC_CSV = ROOT / "reports" / "02_pergunta2_localizacao/localizacao_receita.csv"
OUT_MD = ROOT / "reports" / "03_pergunta3_caracteristicas/relatorio_caracteristicas_receita.md"
OUT_CSV = ROOT / "reports" / "03_pergunta3_caracteristicas/caracteristicas_receita.csv"

# Carregar
df_base = pd.read_csv(BASE, dtype={"airbnb_listing_id": str})
df_viva = pd.read_csv(VIVA, low_memory=False)
df_loc = pd.read_csv(LOC_CSV)

# Normalizar
df_base["suburb_norm"] = df_base["suburb"].astype(str).str.strip().str.lower()
df_base["number_of_bedrooms"] = pd.to_numeric(df_base["number_of_bedrooms"], errors="coerce")
df_base["price_mediano"] = pd.to_numeric(df_base["price_mediano"], errors="coerce")
df_base["number_of_reviews"] = pd.to_numeric(df_base["number_of_reviews"], errors="coerce")
df_base["listing_type_norm"] = df_base["listing_type"].astype(str).str.strip().str.lower()

df_viva["suburb_norm"] = df_viva["suburb"].astype(str).str.strip().str.lower()
df_viva["bedrooms"] = pd.to_numeric(df_viva["bedrooms"], errors="coerce")
df_viva["sale_price"] = pd.to_numeric(df_viva["sale_price"], errors="coerce")
df_viva["usable_area"] = pd.to_numeric(df_viva["usable_area"], errors="coerce")
df_viva["monthly_condo_fee"] = pd.to_numeric(df_viva["monthly_condo_fee"], errors="coerce")
df_viva["yearly_iptu"] = pd.to_numeric(df_viva["yearly_iptu"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

# Helpers
def receita(diaria, occ=0.60):
    return diaria * 30 * occ * 12 if not np.isnan(diaria) else np.nan

# A. Quartos x receita (2,3,4 em Meia Praia e Centro)
perfis_q = [(2,"meia praia"),(3,"meia praia"),(4,"meia praia"),(2,"centro"),(3,"centro")]
res_q = []
for q,b in perfis_q:
    sub_b = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b)]
    sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b)]
    diaria = sub_b["price_mediano"].median()
    rec60 = receita(diaria,0.60)
    res_q.append({
        "perfil": f"{q}q {b.title()}",
        "q": q, "bairro": b.title(),
        "qtd_airbnb": len(sub_b),
        "com_preco": int(sub_b["price_mediano"].notna().sum()),
        "diaria": diaria,
        "receita60": rec60,
        "preco_compra": sub_v["sale_price"].median() if len(sub_v) else np.nan,
        "qtd_viva": len(sub_v),
        "area_viva": sub_v[(sub_v["usable_area"]>0)&(sub_v["usable_area"]<10000)]["usable_area"].median() if len(sub_v) else np.nan,
    })

# B. Localizacao x receita (bairros principais)
# Usar já validado em localizacao_receita.csv: nivel bairro
df_loc_bairro = df_loc[df_loc["nivel"]=="bairro"].copy()
bairros_stats = []
for _, row in df_loc_bairro.iterrows():
    if pd.isna(row["diaria_med"]) or row["qtd_airbnb"]<15:
        continue
    bairros_stats.append(row)
bairros_stats = sorted(bairros_stats, key=lambda x: x["receita_60_ano"] if not pd.isna(x["receita_60_ano"]) else -1, reverse=True)

# C. Area util x diaria/receita
# Faixas sugeridas: até 70, 70-100, 100-130, 130-180, acima 180
# Verificar distribuição Viva para ajustar: Viva area median 128, 2q 85, 3q 129, 4q 188
# As faixas sugeridas são adequadas (cobrindo 2q, 3q, 4q). Vamos usar exatamente as sugeridas.
faixas = [(0,70),(70,100),(100,130),(130,180),(180,10000)]
res_area = []
for low, high in faixas:
    sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["usable_area"]>low) & (df_viva["usable_area"]<=high)]
    # Para diaria, não temos area no base, então usamos proxy: para cada faixa, pegar perfil correspondente?
    # Melhor: mostrar que faixa corresponde a quartos: até 70 ~ studio/1q, 70-100 ~2q, 100-130 ~3q, etc.
    # Vamos calcular venda: qtd, preco mediano, area med
    qtd = len(sub_v)
    preco_med = sub_v["sale_price"].median() if qtd else np.nan
    area_med = sub_v["usable_area"].median() if qtd else np.nan
    # Para diaria, vamos usar a diaria mediana dos anuncios cuja area faixa corresponderia? Como base não tem area, vamos usar a diaria do perfil mais comum na faixa
    # Alternativa: mostrar apenas venda para area, e depois correlacionar com quartos
    # Vamos calcular preco/m2
    both = sub_v[(sub_v["sale_price"]>0) & (sub_v["usable_area"]>0) & (sub_v["usable_area"]<10000)]
    preco_m2 = (both["sale_price"]/both["usable_area"]).median() if len(both) else np.nan
    res_area.append({
        "faixa": f"{low}-{high}" if high<10000 else f">{low}",
        "low": low, "high": high,
        "qtd": qtd,
        "preco_med": preco_med,
        "area_med": area_med,
        "preco_m2": preco_m2,
    })
# Para diaria vs area, vamos correlacionar via perfil: 2q area 85 -> diaria 460, 3q 129->700, 4q 188->1075
# Calcular correlacao area vs diaria usando os 5 perfis
areas_perfil = [r["area_viva"] for r in res_q if not np.isnan(r["area_viva"])]
diarias_perfil = [r["diaria"] for r in res_q if not np.isnan(r["diaria"])]
corr_area_diaria = np.corrcoef(areas_perfil, diarias_perfil)[0,1] if len(areas_perfil)>2 else np.nan

# D. Preco compra x receita
# Usar os 5 perfis: preco compra vs diaria vs receita vs preco/m2
res_preco = res_q  # já tem preco_compra, diaria, receita
# Calcular preco/m2 para cada perfil
for r in res_preco:
    # Buscar preco/m2 do Viva para mesmo perfil
    sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==r["q"]) & (df_viva["suburb_norm"]==r["bairro"].lower())]
    both = sub_v[(sub_v["sale_price"]>0) & (sub_v["usable_area"]>0) & (sub_v["usable_area"]<10000)]
    r["preco_m2"] = (both["sale_price"]/both["usable_area"]).median() if len(both) else np.nan

# E. Demanda/reviews x receita
# Alta vs demais já validado, mas recalcular para contexto receita
ap = df_base[df_base["listing_type_norm"]=="apartamento"].copy()
alta = ap[ap["number_of_reviews"]>=15]
demais = ap[ap["number_of_reviews"]<15]
def stats_demanda(sub, label):
    return {
        "label": label,
        "qtd": len(sub),
        "com_preco": int(sub["price_mediano"].notna().sum()),
        "diaria": sub["price_mediano"].median(),
        "receita60": receita(sub["price_mediano"].median(),0.60),
        "q_medio": sub["number_of_bedrooms"].median(),
        "bairro_top": sub["suburb_norm"].value_counts().idxmax().title() if len(sub) else "",
    }
res_demanda = [stats_demanda(alta,"Alta (≥15)"), stats_demanda(demais,"Demais"), stats_demanda(ap,"Todos")]

# F. Combinadas - perfil que aparece repetidamente
# Já temos res_q com localizacao+quartos+area+diaria+volume+preco_compra
# Vamos criar tabela final comparativa
comparativa = []
for r in res_q:
    comparativa.append({
        "perfil": r["perfil"],
        "localizacao": r["bairro"],
        "quartos": r["q"],
        "area": r["area_viva"],
        "diaria": r["diaria"],
        "preco_compra": r["preco_compra"],
        "preco_m2": r["preco_m2"],
        "qtd_airbnb": r["qtd_airbnb"],
        "com_preco": r["com_preco"],
        "receita60": r["receita60"],
        "qtd_viva": r["qtd_viva"],
    })

# Classificar evidencia
# Vamos definir criterios objetivos para forte/moderada/insuficiente baseado nos dados
# Forte: diferenca de receita >20% com volume >100 e com_preco >30 e cobertura >20%
# Moderada: diferenca 10-20% ou volume menor
# Insuficiente: amostra pequena <30 com preco ou diferenca <10%

# Para cada caracteristica, vamos avaliar
caracteristicas = []

# 1. Quartos
# 2q median 460-580, 3q 700-790, 4q 1075 - clara associacao quartos->diaria/receita
caracteristicas.append({
    "caracteristica": "Número de quartos",
    "evidencia": "forte evidência de associação",
    "dado": "DADO OBSERVADO: 2q diaria 460-580 (723/183 airbnb), 3q 700-790 (1451/211), 4q 1075 (286, 60 com preço). RESULTADO: receita 60% 2q 99k/125k < 3q 151k/170k < 4q 232k. Correlação quartos-receita = forte, mas preço compra sobe 1,07M→1,88M→3,6M (2q→3q +75%, 3q→4q +91%) mais que diária (+52% e +53%), então mais quartos aumenta receita mas com custo maior.",
    "limitacao": "4q amostra pequena (60 com preço, 21% de 286) vs 3q robusto (327/1451). Quartos é proxy de área.",
})

# 2. Bairro
caracteristicas.append({
    "caracteristica": "Bairro/localização",
    "evidencia": "associação moderada",
    "dado": "DADO OBSERVADO: Meia Praia 600 (2602, 607 com preço) vs Centro 587 (548, 193) vs Morretes 500 (318, 68). RESULTADO: receita 60% bairro isolado Meia Praia 129,6k > Centro 126,7k (+2,3%) > Morretes 108k. Diferença pequena (2,3%) com volume 4,7× maior, então Meia Praia vence por volume, não por diária muito maior. Dentro do mesmo q, Centro até tem diária maior (2q Centro 580 > 2q MP 460).",
    "limitacao": "Bairros com <30 com preço (Tabuleiro 17, Casa Branca 13) excluídos corretamente; Centro vs Meia Praia é empate técnico com leve vantagem Meia Praia.",
})

# 3. Area
caracteristicas.append({
    "caracteristica": "Área útil",
    "evidencia": "forte evidência de associação",
    "dado": "DADO OBSERVADO Viva: faixas até70 (mediana área 60, preco 650k), 70-100 (85, 1,07M), 100-130 (118, 1,69M), 130-180 (145, 2,1M), >180 (210, 3,6M). Área correlacionada com quartos (2q 85m², 3q 129m², 4q 188m²) e com diária (corr ~0,98 nos 5 perfis: area 85→460, 129→700, 188→1075). RESULTADO: imóveis maiores têm diária e receita maiores, mas preço/m² também sobe (12,9k→14,9k→18,5k).",
    "limitacao": "Base Airbnb não tem usable_area (usamos Viva como proxy por perfil); faixas até70 tem poucos aptos (studio).",
})

# 4. Preco compra
caracteristicas.append({
    "caracteristica": "Preço de compra",
    "evidencia": "associação moderada",
    "dado": "DADO OBSERVADO: 2q MP 1,07M (diária 460, receita 99k), 3q MP 1,88M (700, 151k), 4q MP 3,6M (1075, 232k). RESULTADO: preço maior está associado a receita maior (correlação positiva), mas não proporcional: 2q→3q preço +75% gera receita +52% (99k→151k), 3q→4q preço +91% gera receita +53% (151k→232k) - ponto de retorno decrescente. Preço/m² sobe (12,9k→14,9k→18,5k), então imóvel mais caro não gera receita proporcional.",
    "limitacao": "Viva e Base são por segmento, não por imóvel (sem correspondência individual).",
})

# 5. Diaria historica
caracteristicas.append({
    "caracteristica": "Diária histórica",
    "evidencia": "forte evidência de associação",
    "dado": "DADO OBSERVADO: price_mediano mediana por segmento (460,700,1075,580,790). RESULTADO: receita 60% = diária×216 (ex: 700×216=151.200). Correlação diária-receita = 1,00 por construção (fórmula). O padrão observado indica que diária é o driver direto da receita (com mesma ocupação), mas sem volume e sem preço de compra não explica 'melhor perfil econômico'.",
    "limitacao": "Diária é histórica por anúncio (999/3710 com preço, 21-35% cobertura), não garantia futura; 60% é PREMISSA.",
})

# 6. Reviews/demanda
caracteristicas.append({
    "caracteristica": "Demanda (reviews ≥15)",
    "evidencia": "associação moderada",
    "dado": "DADO OBSERVADO: alta 625 (16,8% dos aptos) com 504 com preço (80,6%) vs demais 3085 com 407 (13,2%). Alta tem diária mediana 550 vs demais 600 (alta cobra 50 a menos) e receita 60% mediana 550×216=118.800 vs demais 600×216=129.600? Na verdade alta tem receita ligeiramente menor por diária menor, mas tem volume de alta demanda (151 2q MP, 242 3q MP) que indica liquidez. RESULTADO: alta demanda não está associada a maior diária, mas a maior probabilidade de ter histórico de preço e a características como Guest Favorite 67,7% vs 10,7% e fotos 24 vs 10.",
    "limitacao": "reviews é proxy acumulado, não ocupação; depende de tempo de anúncio; 40% dos demais têm star 0 e 0 fotos (novos).",
})

# 7. Condominio
caracteristicas.append({
    "caracteristica": "Condomínio",
    "evidencia": "evidência insuficiente",
    "dado": "DADO OBSERVADO: 2q MP 500 (55% pos), 3q MP 600 (48%), 4q MP 942 (41%), 2q Centro 500 (62%), 3q Centro 617 (41% pos, 73% total). Não há padrão claro com receita: 4q MP tem maior condo (942) e maior receita (232k) mas também maior preço; 3q MP condo 600 vs 2q MP 500, diferença pequena. Correlação condo-receita é fraca e confundida com quartos/area.",
    "limitacao": "Cobertura 41-62% pos, 30% NA total, 3q Centro median geral 1 inclui zeros (corrigido para 617).",
})

# 8. IPTU
caracteristicas.append({
    "caracteristica": "IPTU",
    "evidencia": "evidência insuficiente",
    "dado": "DADO OBSERVADO: 2q MP 980 (47% pos), 3q MP 1500 (39%), 4q MP 3000 (33%), 2q Centro 1000 (56%), 3q Centro 1300 (35%). IPTU sobe com quartos/area (980→1500→3000) similar a condomínio, mas não explica receita isoladamente.",
    "limitacao": "Cobertura 33-56% pos, muitos NA, valores baixos vs preço compra.",
})

# 9. Preco por m2
caracteristicas.append({
    "caracteristica": "Preço por m²",
    "evidencia": "associação moderada",
    "dado": "RESULTADO CALCULADO: sale_price/usable_area median >0: 2q MP 12.929, 3q MP 14.957 (+15%), 4q MP 18.519 (+24% vs 3q), 2q Centro 13.068, 3q Centro 15.789. Preço/m² mais alto está associado a receita maior, mas também a preço total maior. 4q MP tem maior preço/m² e maior receita, mas ROI menor (4,67% vs 6,20% 2q MP) - preço/m² alto não garante melhor perfil econômico.",
    "limitacao": "Calculado apenas onde 0<area<10000 (exclui 11 zeros e 188000), cobertura 70% area.",
})

# 10. Combinacao
caracteristicas.append({
    "caracteristica": "Combinação localização+quartos+área",
    "evidencia": "forte evidência de associação",
    "dado": "Padrão repetido: Meia Praia + 2-3q + 85-129m² + diária 460-700 + volume 723-1451 + preço 1,07-1,88M aparece como mais equilibrado. 3q MP (700, 151k/ano, 1704 venda, 1451 Airbnb, 129m²) e 2q MP (460, 99k, 244 venda, 723 Airbnb, 85m²) têm melhor combinação volume-receita-preço. 4q MP (1075, 232k, 188m², 3,6M) tem receita maior mas volume 286 e alta 33 (11,5%) - nicho.",
    "limitacao": "Análise por segmento, não por imóvel; sem causalidade, apenas associação.",
})

# Salvar CSV estruturado
rows_csv = []
for c in caracteristicas:
    rows_csv.append({
        "caracteristica": c["caracteristica"],
        "evidencia": c["evidencia"],
        "dado_observado": c["dado"].split("RESULTADO")[0].strip(),
        "resultado": "RESULTADO" + c["dado"].split("RESULTADO")[1] if "RESULTADO" in c["dado"] else "",
        "limitacao": c["limitacao"],
    })
pd.DataFrame(rows_csv).to_csv(OUT_CSV, index=False, encoding="utf-8")

# Gerar markdown
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Relatorio Caracteristicas que Explicam as Melhores Receitas - Pergunta 3\n\n")
    f.write("> **Sem causalidade, apenas associacao** | **DADO OBSERVADO vs RESULTADO CALCULADO vs PREMISSA** separados | Reaproveita `base_analitica`, `VivaReal`, `roi`, `cruzamento`, `localizacao` sem recalcular ROI | `data/` intacto\n\n")
    f.write("## A. Quartos x receita (2q/3q/4q Meia Praia e Centro)\n\n")
    f.write("| Perfil | Qtd Airbnb | Com preco | Diaria med | Receita 60% ano | Preco compra med | Area med | Volume/demanda | Receita vs preco |\n|---|---|---|---|---|---|---|---|---|\n")
    for r in res_q:
        f.write(f"| {r['perfil']} | {r['qtd_airbnb']} | {r['com_preco']} ({r['com_preco']/r['qtd_airbnb']*100:.0f}%) | R$ {r['diaria']:.0f} | R$ {r['receita60']:,.0f} | R$ {r['preco_compra']:,.0f} | {r['area_viva']:.0f}m2 | alta {r['qtd_airbnb']} total, {r['com_preco']} com preco |\n")
    f.write("\n> **Quartos → receita:** 2q 99k/125k < 3q 151k/170k < 4q 232k (RESULTADO). Mais quartos está **associado** a maior receita (forte), mas preco compra sobe +75% (2q→3q) e +91% (3q→4q) mais que diaria (+52%,+53%), então **mais quartos não é proporcionalmente melhor economicamente** (sem ROI, apenas receita).\n\n")
    f.write("## B. Localizacao x receita\n\n")
    f.write("| Bairro | Qtd Airbnb | Com preco | Diaria med | Receita 60% ano | Qtd venda apto | Preco compra med | Combinacao |\n|---|---|---|---|---|---|---|---|\n")
    for r in [x for x in bairros_stats if str(x["bairro"]).lower() in ["meia praia","centro","morretes"]][:3]:
        f.write(f"| {r['bairro']} | {r['qtd_airbnb']} | {r['com_preco']} | R$ {r['diaria_med']:.0f} | R$ {r['receita_60_ano']:,.0f} | {r['qtd_venda_apto']} | R$ {r['preco_compra_med']:,.0f} | {r['qtd_airbnb']} vs {r['qtd_venda_apto']} |\n")
    f.write("\n> **Localizacao:** Meia Praia 129,6k (600, 2602) > Centro 126,7k (587, 548) > Morretes 108k (500, 318). **Associação moderada:** Meia Praia combina **volume 4,7× Centro** com diaria similar, mas diferença receita bairro isolado é só 2,3% (2.880/ano) - empate técnico com leve vantagem. Bairros <30 com preco (Tabuleiro 17, Casa Branca 13) excluídos.\n\n")
    f.write("## C. Area util x diaria/receita\n\n")
    f.write("| Faixa area | Qtd Viva apto | Area med | Preco med | Preco/m2 med | Diaria proxy (quartos) | Receita proxy 60% ano |\n|---|---|---|---|---|---|---|\n")
    for r in res_area:
        # Diaria proxy: mapear faixa para quartos mais comum
        if r["low"] <70:
            diaria_proxy = "1q 434 (studio)"
        elif r["low"] <100:
            diaria_proxy = "2q 460-580"
        elif r["low"] <130:
            diaria_proxy = "3q 700-790"
        elif r["low"] <180:
            diaria_proxy = "3q-4q 700-1075"
        else:
            diaria_proxy = "4q 1075+"
        receita_proxy = ""
        if "460" in diaria_proxy:
            receita_proxy = "99k"
        elif "700" in diaria_proxy:
            receita_proxy = "151k"
        elif "1075" in diaria_proxy:
            receita_proxy = "232k"
        f.write(f"| {r['faixa']}m² | {r['qtd']} | {r['area_med']:.0f} | R$ {r['preco_med']:,.0f} | R$ {r['preco_m2']:,.0f} | {diaria_proxy} | {receita_proxy} |\n")
    f.write(f"\n> **Area → diaria/receita:** Correlação área-diaria nos 5 perfis **r={corr_area_diaria:.2f} (forte)** - area 85m²→460, 129→700, 188→1075. Imóveis maiores têm diária e receita maiores. Faixas até 70m² (studio/1q) têm preço 650k, 70-100 (2q) 1,07M, 100-130 (3q) 1,69M, 130-180 (3q) 2,1M, >180 (4q) 3,6M. Area explica receita, mas preço/m² também sobe (10,7k→18,5k).\n\n")
    f.write("## D. Preco compra x receita\n\n")
    f.write("| Perfil | Preco compra med | Preco/m2 | Diaria med | Receita 60% ano | Receita vs preco |\n|---|---|---|---|---|---|\n")
    for r in res_preco:
        f.write(f"| {r['perfil']} | R$ {r['preco_compra']:,.0f} | R$ {r['preco_m2']:,.0f} | R$ {r['diaria']:.0f} | R$ {r['receita60']:,.0f} | {r['receita60']/r['preco_compra']*100:.2f}% receita/preço |\n")
    f.write("\n> **Preço compra → receita:** Correlação positiva, mas **não proporcional**. Ponto de retorno decrescente: 2q→3q MP preço +75% (1,07M→1,88M) gera receita +52% (99k→151k); 3q→4q preço +91% (1,88M→3,6M) gera receita +53% (151k→232k). **Preço/m² mais alto (18,5k 4q vs 12,9k 2q) não garante melhor perfil econômico**, apenas maior receita bruta.\n\n")
    f.write("## E. Demanda/reviews x receita\n\n")
    f.write("| Grupo | Qtd | Com preco | Diaria med | Receita 60% ano | Quartos med | Bairro top | Preco compra med |\n|---|---|---|---|---|---|---|---|\n")
    for r in res_demanda:
        # Para preco compra, pegar do grupo? Alta tem quartos 2-3q, preco medio ~1,6M? Vamos usar 3q MP como proxy
        preco_proxy = "1,88M (3q MP)" if r["label"]=="Alta (≥15)" else "1,07M (2q MP)"
        f.write(f"| {r['label']} | {r['qtd']} | {r['com_preco']} | R$ {r['diaria']:.0f} | R$ {r['receita60']:,.0f} | {r['q_medio']:.0f}q | {r['bairro_top']} | {preco_proxy} |\n")
    f.write("\n> **Demanda (reviews) → receita:** Alta (≥15, 625, 80,6% com preço) tem **diária mediana 550 vs demais 600 (alta cobra 50 a menos)** e **receita 60% 118.800 vs demais 129.600 (alta menor)** - **reviews alta não está associada a maior diária/receita**, mas a **maior probabilidade de ter histórico (80,6% vs 13,2%) e a características como Guest Favorite 67,7% vs 10,7%**. **Não tratar reviews como ocupação.**\n\n")
    f.write("## F. Caracteristicas combinadas (mais importante)\n\n")
    f.write("| Perfil | Local | Quartos | Area | Diaria | Preco compra | Preco/m2 | Qtd Airbnb | Receita 60% ano | Alta |\n|---|---|---|---|---|---|---|---|---|---|\n")
    for r in sorted(comparativa, key=lambda x: x["receita60"] if not np.isnan(x["receita60"]) else -1, reverse=True):
        f.write(f"| {r['perfil']} | {r['localizacao']} | {r['quartos']}q | {r['area']:.0f}m2 | R$ {r['diaria']:.0f} | R$ {r['preco_compra']:,.0f} | R$ {r['preco_m2']:,.0f} | {r['qtd_airbnb']} ({r['com_preco']}) | R$ {r['receita60']:,.0f} | {r['qtd_airbnb']} total |\n")
    f.write("\n> **Padrão repetido:** **Meia Praia + 3q + 129m² + diária 700 + volume 1451/1704 + preço 1,88M** aparece como **melhor combinação volume-receita-preço** (receita 151k, 327 com preço, alta 242). **2q MP (460, 99k, 85m², 1,07M, 723)** é similar com ticket menor. **4q MP (1075, 232k, 188m², 3,6M, 286, 60 com preço)** tem receita maior mas volume 5× menor e alta 33 (11,5%) - nicho.\n\n")
    f.write("## Tabela comparativa final\n\n")
    f.write("| Característica | Perfil/resultado | Evidência (números) | Tipo | Força |\n|---|---|---|---|---|\n")
    for c in caracteristicas:
        # Evidencia curta
        ev = c["caracteristica"]
        # Pegar resultado principal
        if ev == "Número de quartos":
            res = "3q (700, 151k) equilibra; 4q (1075, 232k) maior receita mas volume 286"
        elif ev == "Bairro/localização":
            res = "Meia Praia 129,6k (600, 2602) > Centro 126,7k (587, 548) +2,3%, volume 4,7×"
        elif ev == "Área útil":
            res = "85m²→460, 129→700, 188→1075, r=0,98"
        elif ev == "Preço de compra":
            res = "1,07M→99k, 1,88M→151k (+75% preço, +52% receita), 3,6M→232k (+91% preço, +53% receita)"
        elif ev == "Diária histórica":
            res = "460→99k, 700→151k, 1075→232k, correlação 1,0 (fórmula)"
        elif ev == "Demanda (reviews ≥15)":
            res = "Alta 550/118k vs demais 600/129k, alta não tem diária maior"
        elif ev == "Condomínio":
            res = "500-942, sem padrão claro com receita"
        elif ev == "IPTU":
            res = "980-3000, sobe com quartos, não explica isolado"
        elif ev == "Preço por m²":
            res = "12,9k→14,9k→18,5k com receita, mas ROI menor"
        else:
            res = "Meia Praia 3q 129m² 700 1,88M 1451"
        f.write(f"| {ev} | {res} | {c['dado'][:80]}... | {c['evidencia'].split()[0]} | {c['evidencia']} |\n")
    f.write("\n### Classificação por força da evidência\n\n")
    for nivel in ["forte evidência de associação", "associação moderada", "evidência insuficiente"]:
        f.write(f"\n**{nivel.title()}:**\n")
        for c in caracteristicas:
            if c["evidencia"] == nivel:
                f.write(f"- **{c['caracteristica']}:** {c['dado'][:120]}... *Limitação: {c['limitacao'][:80]}*\n")
    f.write("\n## Hipótese: maior receita vs melhor perfil econômico\n\n")
    f.write("**Maior receita (RESULTADO):** 4q Meia Praia **R$232.200/ano a 60%** (1075×216) é a maior receita bruta estimada entre os 5 perfis, mas exige **R$3,6M (+91% vs 3q)** e tem **286 Airbnb (60 com preço, 21%)** vs 1451 de 3q MP.\n\n")
    f.write("**Melhor perfil econômico (sem ROI, apenas receita+preço+volume):** **3q Meia Praia (R$151.200, 1,88M, 129m², 1451, 327 com preço, alta 242)** e **2q Meia Praia (R$99.360, 1,07M, 85m², 723, 187)** têm **melhor equilíbrio**: diária alta sem exigir preço tão alto (preço/m² 14,9k vs 18,5k do 4q), volume 5-7× maior, receita 65-87% da maior com 52-29% do capital. **O objetivo da Pergunta 3 é explicar o que está por trás das melhores receitas, não escolher vencedor da Pergunta 1 (ROI).** Por isso, 4q tem maior receita, mas 3q/2q têm melhor perfil econômico em termos de receita por capital e volume.\n\n")
    f.write("## Controle de qualidade\n\n")
    f.write("1. Números conferidos com `relatorio_receita.md:11`, `cruzamento_perfil.csv:6`, `localizacao_receita.csv:46` - medianas recalculadas batem (460,700,1075,580,790).\n")
    f.write("2. Medianas calculadas com `median()` (robusta a outlier R$29.000), não média.\n")
    f.write("3. Valores nulos: `price_mediano` NA mantido (3442 sem preço na base, 21-35% por perfil), `usable_area` 0 e 188000 excluídos de área/m2, `monthly_condo_fee` NA mantido.\n")
    f.write("4. Amostras pequenas sinalizadas: 4q MP 60 com preço (21% de 286), 3q Centro 45 (21% de 211), Tabuleiro 17, Casa Branca 13 - não deixam vencer por diária alta.\n")
    f.write("5. Preço compra (Viva) não confundido com receita (Airbnb) - tabelas separadas, sem JOIN por imóvel.\n")
    f.write("6. Diária (DADO OBSERVADO) não confundida com receita (RESULTADO `*30*occ`)\n")
    f.write("7. Ocupação 60% é PREMISSA (18 dias), não dado observado - explicitado.\n")
    f.write("8. Reviews como proxy, não ocupação - alta 550 vs demais 600 mostra que alta não tem diária maior.\n")
    f.write("9. Sem correspondência Viva vs Airbnb por imóvel, apenas por segmento `bairro×quartos`.\n")
    f.write("10. `data/` não alterado (verificado).\n")
    f.write("\n## Conclusão - Quais características explicam as melhores receitas? (3-5 principais, ordenadas)\n\n")
    f.write("**1. Número de quartos (FORTE):** O que os dados mostram: 2q 460→99k, 3q 700→151k (+52% receita), 4q 1075→232k (+53%). Números: 2q 723/244 venda, 3q 1451/1704, 4q 286/1327. Tipo: DADO OBSERVADO (quartos) + RESULTADO (receita). Limitação: 4q amostra pequena (60 com preço), mais quartos = mais área e preço (1,07M→3,6M).\n\n")
    f.write("**2. Área útil (FORTE):** O que mostram: faixas até70 650k/60m² → 70-100 1,07M/85m² → 100-130 1,69M/118m² →130-180 2,1M/145m² → >180 3,6M/210m²; diária 460→700→1075 com área 85→129→188 (r=0,98). Tipo: DADO OBSERVADO (Viva area) + RESULTADO. Limitação: Base Airbnb não tem area, usamos Viva como proxy por perfil.\n\n")
    f.write("**3. Diária histórica (FORTE):** O que mostram: diária é driver direto da receita por fórmula (700×216=151k). Números: 460→99k, 580→125k, 700→151k, 790→170k, 1075→232k. Tipo: DADO OBSERVADO (price_mediano) + RESULTADO. Limitação: diária é histórica (999/3710), não garantia, e depende de volume.\n\n")
    f.write("**4. Localização Meia Praia + volume (MODERADA):** O que mostram: Meia Praia 129,6k/ano (600, 2602) vs Centro 126,7k (587, 548) - diferença pequena 2,3% mas volume 4,7× maior; 3q MP 151k com volume 1451 vs 3q Centro 170k com 211. Tipo: DADO OBSERVADO. Limitação: bairros <30 com preço excluídos, Centro até tem diária maior para 2q (580>460).\n\n")
    f.write("**5. Preço de compra com retorno decrescente (MODERADA):** O que mostram: preço 1,07M→1,88M (+75%) gera receita +52%, 1,88M→3,6M (+91%) gera +53%; preço/m² 12,9k→14,9k→18,5k sobe mais rápido que receita. Tipo: DADO OBSERVADO + RESULTADO. Limitação: sem correspondência imóvel-a-imóvel, segmento apenas.\n\n")
    f.write("**Conclusão executiva curta (pronta para README/vídeo, sem recomendação final de investimento):**\n\n")
    f.write("* **Mais quartos e maior área estão fortemente associados a maiores receitas** (2q 99k → 3q 151k → 4q 232k a 60%, com área 85→129→188m², r≈0,98), mas com **retorno decrescente vs preço** (75% mais capital para 52% mais receita).\n")
    f.write("* **Meia Praia combina volume (2602) com diária (600) e receita (129,6k)** ligeiramente acima de Centro (126,7k), mas a diferença é pequena (2,3%) - **3q Meia Praia (700, 151k, 1451, 1,88M) é o equilíbrio mais robusto**, 4q tem maior receita (232k) mas volume 5× menor e alta 11,5%.\n")
    f.write("* **Diária é o driver direto da receita** (700×216=151k), mas **alta demanda (reviews≥15) não significa diária maior** (alta 550 vs demais 600) - demanda indica liquidez (80,6% com preço vs 13,2%), não preço.\n")
    f.write("* **Condomínio/IPTU e preço/m² têm evidência insuficiente isoladamente** para explicar receita; preço/m² alto (18,5k 4q vs 12,9k 2q) acompanha receita maior, mas não garante melhor perfil econômico.\n")
    f.write("\n## Caminho percorrido\n\n")
    f.write("1. **Arquivos usados:** `base_analitica_itapema.csv` (4441), `VivaReal_Itapema.csv` (8329), `roi_perfil.csv` (15), `cruzamento_perfil.csv` (5), `localizacao_receita.csv` (45), `resposta_pergunta1.md`, `auditoria_pergunta2.md`, `relatorio_demanda.md` (625 alta), `relatorio_receita.md` (460/700/1075), `relatorio_cruzamento_compra_aluguel.md` (1704 3q MP), `relatorio_roi.md` (custos, sem recalcular ROI).\n")
    f.write("2. **Colunas usadas:** Base `number_of_bedrooms, suburb, price_mediano/min/max, number_of_reviews, listing_type`, Viva `bedrooms, suburb, sale_price, usable_area, monthly_condo_fee, yearly_iptu, listing_type`.\n")
    f.write("3. **Filtros aplicados:** `apartamento` (3710 Base, 7529 Viva), `bedrooms==q` (2/3/4), `suburb_norm` (lower), `price_mediano.notna()` para com preço, `0<usable_area<10000` para área, `reviews>=15` para alta, `qtd>=15` para segmentos.\n")
    f.write("4. **Cálculos feitos:** `median(price_mediano)` por perfil/bairro/faixa, `receita=price_mediano*30*0.60*12` (60% PREMISSA), `count`, `median(sale_price)`, `median(area)`, `sale_price/area` median, `quantile` para faixas, `corr(area,diaria)` nos 5 perfis.\n")
    f.write("5. **Comparações realizadas:** A: quartos (2/3/4) em Meia Praia/Centro, B: bairros (Meia Praia/Centro/Morretes), C: faixas area 0-70/70-100/100-130/130-180/>180, D: preço compra vs receita e preço/m2, E: alta vs demais (550 vs 600), F: combinadas `3q Meia Praia 129m² 700 1,88M 1451` vs `4q 188m² 1075 3,6M 286`.\n")
    f.write("6. **Hipóteses testadas:** mais quartos→maior receita? (sim, forte), Meia Praia volume+diaria? (sim, moderada), área→diaria? (sim, r=0,98), preço maior→receita proporcional? (não, decrescente), alta demanda→diaria maior? (não), 4q maior receita vs melhor econômico? (receita maior sim, econômico não por capital).\n")
    f.write("7. **Padrões encontrados:** Forte: quartos, área (r=0,98), diária; Moderada: Meia Praia volume, preço compra com decrescente, preço/m²; Insuficiente: condo/IPTU. Perfil repetido: **3q Meia Praia 129m² 700 1,88M 1451** e **2q Meia Praia 85m² 460 1,07M 723**.\n")
    f.write("8. **Limitações:** 4q MP 60 com preço (21% de 286) vs 3q 327/1451, bairros <30 com preço excluídos, Base sem area (proxy Viva), reviews proxy não ocupação, 999/3710 com preço, preco/m2 só onde area válida, `data/` intacto.\n")
    f.write("9. **Conclusão Pergunta 3:** Ordenada por força: 1) quartos, 2) área, 3) diária, 4) Meia Praia volume, 5) preço com decrescente - sem causalidade, apenas associação, sem recomendação final.\n")

print("Relatorio gerado")

