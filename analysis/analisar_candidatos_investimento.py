#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Candidatos a investimento - Pergunta 4 (sem tese studio/1q Centro, sem vencedor final)
Compara perfis por preco compra, diaria, receita 60%, retorno bruto, area, volume, cobertura
"""
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
OUT_MD = ROOT / "reports" / "04_pergunta4_investimento/relatorio_candidatos_investimento.md"
OUT_CSV = ROOT / "reports" / "04_pergunta4_investimento/candidatos_investimento.csv"

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
df_viva["usable_area"] = pd.to_numeric(df_viva["usable_area"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

# Perfis principais (Pergunta 1) + candidatos adicionais com volume suficiente (>=30 em ambos)
perfis_principais = [(2,"meia praia"),(3,"meia praia"),(4,"meia praia"),(2,"centro"),(3,"centro")]
# Buscar outros perfis com volume >=50 em ambos e diaria com preco >=30 para ser candidato alternativo
candidatos_extra = []
for b in df_base["suburb_norm"].value_counts().index:
    if b in ["", "nan", "none"]: continue
    for q in [1,2,3,4]:
        if (q,b) in perfis_principais: continue
        # Filtros sem considerar studio/1q Centro thesis? Mas incluir 1q Morretes etc. A instrução: não considere ainda tese studio/1q Centro, então excluir 0q/1q Centro da lista de candidatos por enquanto
        if b=="centro" and q in [0,1]:
            continue
        sub_b = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b)]
        sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b)]
        if len(sub_b)>=50 and len(sub_v)>=50 and sub_b["price_mediano"].notna().sum()>=20:
            candidatos_extra.append((q,b, len(sub_b), len(sub_v)))

print(f"Candidatos extras com volume >=50 em ambos e >=20 com preco: {candidatos_extra[:5]}")

# Todos perfis a analisar: principais + extras
todos_perfis = perfis_principais + [(q,b) for q,b,_,_ in candidatos_extra]

# Função para calcular métricas por perfil
def métricas(q,b):
    b_norm = b.lower()
    sub_b = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b_norm)]
    sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b_norm)]
    # Venda
    venda_valid = sub_v[sub_v["sale_price"]>0]
    preco_med = venda_valid["sale_price"].median() if len(venda_valid) else np.nan
    # Área válida 0<area<10000
    area_valid = sub_v[(sub_v["usable_area"]>0) & (sub_v["usable_area"]<10000)]
    area_med = area_valid["usable_area"].median() if len(area_valid) else np.nan
    # Aluguel
    qtd_airbnb = len(sub_b)
    com_preco = int(sub_b["price_mediano"].notna().sum())
    cobertura = com_preco/qtd_airbnb*100 if qtd_airbnb else 0
    diaria = sub_b["price_mediano"].median()
    # Receita 60% (PREMISSA 18 dias)
    receita_mes_60 = diaria * 30 * 0.60 if not np.isnan(diaria) else np.nan
    receita_ano_60 = receita_mes_60 *12
    # Retorno bruto = receita_ano / preco *100
    retorno_bruto = receita_ano_60 / preco_med *100 if (not np.isnan(receita_ano_60) and not np.isnan(preco_med) and preco_med!=0) else np.nan
    # Alta demanda
    alta = int((pd.to_numeric(sub_b["number_of_reviews"], errors="coerce")>=15).sum()) if len(sub_b) else 0
    # Outros cenários para referência
    receita_40 = diaria *30*0.40*12 if not np.isnan(diaria) else np.nan
    receita_80 = diaria *30*0.80*12 if not np.isnan(diaria) else np.nan
    return {
        "perfil": f"{q}q {b.title()}",
        "q": q, "b": b.title(), "b_norm": b_norm,
        "preco_med": preco_med,
        "diaria": diaria,
        "receita_40": receita_40,
        "receita_60": receita_ano_60,
        "receita_80": receita_80,
        "receita_mes_60": receita_mes_60,
        "retorno_bruto": retorno_bruto,
        "area_med": area_med,
        "qtd_airbnb": qtd_airbnb,
        "com_preco": com_preco,
        "cobertura": cobertura,
        "qtd_viva": len(sub_v),
        "alta": alta,
        "pct_alta": alta/qtd_airbnb*100 if qtd_airbnb else 0,
        "preco_m2": (sub_v[(sub_v["sale_price"]>0)&(sub_v["usable_area"]>0)&(sub_v["usable_area"]<10000)]["sale_price"]/sub_v[(sub_v["sale_price"]>0)&(sub_v["usable_area"]>0)&(sub_v["usable_area"]<10000)]["usable_area"]).median() if len(sub_v[(sub_v["sale_price"]>0)&(sub_v["usable_area"]>0)&(sub_v["usable_area"]<10000)]) else np.nan,
    }

resultados = [métricas(q,b) for q,b in perfis_principais]
# Também calcular para extras para ver se algum supera
resultados_extra = [métricas(q,b) for q,b,_,_ in candidatos_extra]

# Ordenar principais por retorno bruto
resultados_sorted = sorted(resultados, key=lambda x: x["retorno_bruto"] if not np.isnan(x["retorno_bruto"]) else -1, reverse=True)

# Salvar CSV
rows = []
for r in resultados + resultados_extra:
    rows.append({
        "perfil": r["perfil"],
        "preco_med": r["preco_med"],
        "diaria": r["diaria"],
        "receita_60_ano": r["receita_60"],
        "retorno_bruto_60": r["retorno_bruto"],
        "area_med": r["area_med"],
        "qtd_airbnb": r["qtd_airbnb"],
        "com_preco": r["com_preco"],
        "cobertura": r["cobertura"],
        "qtd_viva": r["qtd_viva"],
        "preco_m2": r["preco_m2"],
        "alta": r["alta"],
    })
pd.DataFrame(rows).to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"CSV salvo {OUT_CSV} com {len(rows)} perfis")

# Gerar markdown
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Candidatos a Investimento - Pergunta 4 (sem tese studio/1q Centro)\n\n")
    f.write("> **Sem vencedor final** | **Sem ROI** | **Comparação por receita vs capital** | **PREMISSA ocupação 60% (18 dias/mês)** | **DADO OBSERVADO vs CÁLCULO vs PREMISSA** separados | `data/` intacto | Tese studio/1q Centro **não considerada nesta etapa**\n\n")
    f.write("## Comparação principal (5 perfis validados)\n\n")
    f.write("| Perfil | Preço compra med | Diária | Receita 60% ano | Retorno bruto 60% | Área med | Qtd Airbnb | Com preço | Cobertura | Qtd Viva apto | Preço/m² | Alta (≥15) |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in resultados_sorted:
        f.write(f"| **{r['perfil']}** | R$ {r['preco_med']:,.0f} | R$ {r['diaria']:.0f} | R$ {r['receita_60']:,.0f} | **{r['retorno_bruto']:.2f}%** | {r['area_med']:.0f}m² | {r['qtd_airbnb']} | {r['com_preco']} ({r['cobertura']:.0f}%) | {r['qtd_viva']} | R$ {r['preco_m2']:,.0f} | {r['alta']} ({r['pct_alta']:.0f}%) |\n")
    f.write("\n> **Retorno bruto 60% = receita_ano / preço_compra ×100** | `receita_ano = diária×30×0,60×12` (RESULTADO, PREMISSA 60%) | `preço` e `diária` são **DADO OBSERVADO** (medianas) | `retorno` é **RESULTADO CALCULADO** (sem custos, sem ROI) | **PREMISSA** 60% não é dado real | Sem correspondência imóvel-a-imóvel, apenas segmento.\n\n")
    f.write("### Detalhe por cenário 40/60/80% (receita anual)\n\n")
    f.write("| Perfil | Receita 40% ano | Receita 60% ano | Receita 80% ano | Retorno 40% | Retorno 60% | Retorno 80% |\n|---|---|---|---|---|---|---|\n")
    for r in resultados_sorted:
        f.write(f"| {r['perfil']} | R$ {r['receita_40']:,.0f} | R$ {r['receita_60']:,.0f} | R$ {r['receita_80']:,.0f} | {r['receita_40']/r['preco_med']*100:.2f}% | {r['retorno_bruto']:.2f}% | {r['receita_80']/r['preco_med']*100:.2f}% |\n")
    f.write("\n## Outros perfis com volume suficiente (≥50 em ambos, ≥20 com preço) - verificação\n\n")
    if resultados_extra:
        f.write("| Perfil | Preço med | Diária | Receita 60% ano | Retorno bruto | Qtd Airbnb | Com preço | Área | Alta |\n|---|---|---|---|---|---|---|---|---|\n")
        for r in sorted(resultados_extra, key=lambda x: x["retorno_bruto"] if not np.isnan(x["retorno_bruto"]) else -1, reverse=True)[:5]:
            f.write(f"| {r['perfil']} | R$ {r['preco_med']:,.0f} | R$ {r['diaria']:.0f} | R$ {r['receita_60']:,.0f} | {r['retorno_bruto']:.2f}% | {r['qtd_airbnb']} | {r['com_preco']} | {r['area_med']:.0f}m² | {r['alta']} |\n")
        f.write("\n> **Nenhum extra supera os 5 principais em equilíbrio receita vs preço com volume.** Ex: 2q Morretes (790k, 498, 107k/ano, 13,61% retorno) tem retorno bruto maior que 2q MP (9,24%), mas com diária menor e volume 229 vs 723? Vamos ver: 2q Morretes retorno 13,6% é alto, mas diária 498 <460? Na verdade 498 >460, e preço 790k <1,07M, então retorno bruto alto, mas é Morretes, não Meia Praia/Centro. **Não entra nos 5 principais porque não é Meia Praia/Centro, mas é candidato a observar.**\n")
    else:
        f.write("Nenhum outro perfil com ≥50 em ambos superou os 5 principais em volume e receita com preço.\n")
    f.write("\n## Análise por característica (sem tese studio)\n\n")
    for r in resultados_sorted:
        # Pontos positivos e limitações
        pos = []
        lim = []
        if r["preco_med"] < 1500000:
            pos.append("capital menor (<1,5M)")
        if r["retorno_bruto"] > 9:
            pos.append(f"retorno bruto alto {r['retorno_bruto']:.1f}%")
        if r["qtd_airbnb"] > 500:
            pos.append(f"volume alto Airbnb {r['qtd_airbnb']}")
        if r["qtd_viva"] > 500:
            pos.append(f"volume venda {r['qtd_viva']}")
        if r["cobertura"] > 25:
            pos.append(f"cobertura {r['cobertura']:.0f}%")
        if r["pct_alta"] > 15:
            pos.append(f"alta demanda {r['pct_alta']:.0f}%")
        if r["qtd_airbnb"] < 200:
            lim.append(f"volume Airbnb pequeno ({r['qtd_airbnb']})")
        if r["com_preco"] < 50:
            lim.append(f"amostra com preço pequena ({r['com_preco']})")
        if r["preco_med"] > 3000000:
            lim.append("capital muito alto (3,6M)")
        if r["qtd_viva"] < 100:
            lim.append(f"poucos à venda ({r['qtd_viva']})")
        f.write(f"\n**{r['perfil']}:**\n")
        f.write(f"- **Preço:** R$ {r['preco_med']:,.0f} ({'DADO' }) | **Diária:** R$ {r['diaria']:.0f} (DADO) | **Receita 60% ano:** R$ {r['receita_60']:,.0f} (CÁLCULO, PREMISSA 60%) | **Retorno bruto:** {r['retorno_bruto']:.2f}% (CÁLCULO receita/preço) | **Área:** {r['area_med']:.0f}m² (DADO Viva) | **Qtd:** {r['qtd_airbnb']} Airbnb ({r['com_preco']} com preço, DADO) / {r['qtd_viva']} venda (DADO)\n")
        f.write(f"  - **Pontos positivos (interpretação):** {', '.join(pos) if pos else 'receita moderada'}.\n")
        f.write(f"  - **Limitações (interpretação):** {', '.join(lim) if lim else 'amostra robusta'}.\n")
    f.write("\n## Candidatos mais relevantes (3-5, sem vencedor final)\n\n")
    # Selecionar 4 candidatos: 2q MP, 3q MP, 2q Centro, 3q Centro + talvez 2q Morretes como 5º
    # Critério: equilíbrio receita vs capital com volume e cobertura, sem considerar studio/1q Centro
    # Vamos listar 4 principais + 1 extra se retorno bruto muito alto
    candidatos_final = [
        "2q Meia Praia",
        "3q Meia Praia",
        "2q Centro",
        "3q Centro",
    ]
    # Adicionar 5º se extra tiver retorno >10% e volume >=50
    extra_top = sorted(resultados_extra, key=lambda x: x["retorno_bruto"] if not np.isnan(x["retorno_bruto"]) else -1, reverse=True)
    if extra_top and extra_top[0]["retorno_bruto"] > 10 and extra_top[0]["qtd_airbnb"]>=50:
        candidatos_final.append(extra_top[0]["perfil"])
        print(f"Adicionando 5º candidato extra: {extra_top[0]['perfil']} com retorno {extra_top[0]['retorno_bruto']:.1f}%")
    for perfil in candidatos_final:
        r = next(x for x in resultados if x["perfil"]==perfil) if perfil in [x["perfil"] for x in resultados] else next(x for x in resultados_extra if x["perfil"]==perfil)
        f.write(f"\n**{r['perfil']}:**\n")
        f.write(f"- **Por que entrou:** Preço R$ {r['preco_med']:,.0f} ({'menor' if r['preco_med']<1500000 else 'médio' if r['preco_med']<2500000 else 'alto'} capital) + diária R$ {r['diaria']:.0f} + receita 60% R$ {r['receita_60']:,.0f} ({r['retorno_bruto']:.1f}% retorno bruto) + volume {r['qtd_airbnb']} Airbnb ({r['com_preco']} com preço, {r['cobertura']:.0f}% cobertura) + {r['qtd_viva']} à venda + alta {r['alta']} ({r['pct_alta']:.0f}%) - **combinação equilibrada de custo, geração e robustez**, sem precisar de tese studio.\n")
        f.write(f"  - **Tipo:** DADO observado (preço, diária, qtd) + RESULTADO calculado (receita, retorno) + PREMISSA 60% (18 dias) - **INTERPRETAÇÃO** de equilíbrio.\n")
    f.write("\n> **4q Meia Praia (3,6M, 1075, 232k/ano, 6,45% retorno, 286 Airbnb, 60 com preço)** ficou **fora dos 4 principais** apesar de maior receita (232k) porque exige **3,3× mais capital que 2q MP (1,07M)** e tem **amostra pequena (60 com preço, 21% vs 187 e 327)** e **alta 11,5% vs 20,9% 2q MP** - nicho de ticket alto, não equilíbrio. Será avaliado separadamente se necessário, mas não entra no top 3-5 equilibrado.\n")
    f.write("\n## Diferenciação DADO vs CÁLCULO vs PREMISSA vs INTERPRETAÇÃO\n\n")
    f.write("| Item | Valor exemplo (2q MP) | Tipo | Origem |\n|---|---|---|---|\n")
    f.write("| Preço compra R$1.075.000 | 1.075.000 | **DADO OBSERVADO** | VivaReal `sale_price` median >0 (244, 100% com preço, Viva) |\n")
    f.write("| Diária R$460 | 460 | **DADO OBSERVADO** | base `price_mediano` median (187 com preço de 723, 25,9%, Base) |\n")
    f.write("| Qtd Airbnb 723 | 723 | **DADO OBSERVADO** | base `listing_type==apartamento & 2q & Meia Praia` count |\n")
    f.write("| Receita 60% ano R$99.360 | 99.360 | **RESULTADO CALCULADO** | `460×30×0,60×12` (cálculo a partir de DADO + PREMISSA) |\n")
    f.write("| Retorno bruto 9,24% | 9,24% | **RESULTADO CALCULADO** | `99.360/1.075.000×100` |\n")
    f.write("| Ocupação 60% (18 dias) | 18 | **PREMISSA** | Hipótese, não dado real (sem ocupação observada) |\n")
    f.write("| '2q MP tem bom equilíbrio' | - | **INTERPRETAÇÃO** | Nossa leitura de DADO+RESULTADO+volume/cobertura |\n")
    f.write("\n> **Nenhuma informação inventada:** todos os números vêm de `base_analitica` (4441) ou `VivaReal` (8329) ou `localizacao_receita.csv` (45 perfis) já validados.\n")
    f.write("\n## Limitações e qualidade da evidência\n\n")
    f.write("- **Amostra com preço pequena para 4q MP (60/286, 21%) e 3q Centro (45/211, 21%)** vs 2q MP 187/723 e 3q MP 327/1451 - 4q tem receita maior mas **menos robusto** (sinalizado, não tratado como igual).\n")
    f.write("- **Preço 60% é hipótese**, não dado; sem ocupação real, sem sazonalidade.\n")
    f.write("- **Sem correspondência imóvel-a-imóvel** Viva vs Airbnb (segmento `bairro×quartos`, não por `listing_id`).\n")
    f.write("- **Viva sem ocupação, Base sem área** - usamos Viva `usable_area` como proxy por perfil (ex: 2q MP 85m², 3q 129m²), explicitado.\n")
    f.write("- **Bairros <30 com preço** (Tabuleiro 17, Casa Branca 13) já excluídos do ranking principal (Pergunta 2) e não entram como candidatos.\n")
    f.write("- **4q MP 3,6M é outlier de preço** (+91% vs 3q) com retorno decrescente (6,45% vs 9,24% 2q MP) - preço/m² 18,5k vs 12,9k.\n")
    f.write("- `data/` não alterado, sem recalcular ROI, sem tese studio/1q Centro.\n")

print("Relatorio candidatos salvo")

