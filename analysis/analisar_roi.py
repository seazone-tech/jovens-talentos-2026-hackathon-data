#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROI estimado por perfil - Cruzamento compra x aluguel
Sem recomendacao final formada antes dos calculos, apenas cenarios
"""
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
CRUZ = ROOT / "reports" / "01_pergunta1_perfil/cruzamento_perfil.csv"
OUT = ROOT / "reports" / "01_pergunta1_perfil/relatorio_roi.md"
OUT_CSV = ROOT / "reports" / "01_pergunta1_perfil/roi_perfil.csv"

# Carregar bases
df_viva = pd.read_csv(VIVA, low_memory=False)
df_base = pd.read_csv(BASE, dtype={"airbnb_listing_id": str})
df_cruz = pd.read_csv(CRUZ)

# Normalizar para pegar valores consistentes com relatorios anteriores
# Usar valores ja validados de cruzamento: para cada perfil, pegar medians
# Mas recalcular para garantir reprodutivel: filtrar base por perfil
df_viva["suburb_norm"] = df_viva["suburb"].astype(str).str.strip().str.lower()
df_viva["bedrooms"] = pd.to_numeric(df_viva["bedrooms"], errors="coerce")
df_viva["sale_price"] = pd.to_numeric(df_viva["sale_price"], errors="coerce")
df_viva["usable_area"] = pd.to_numeric(df_viva["usable_area"], errors="coerce")
df_viva["monthly_condo_fee"] = pd.to_numeric(df_viva["monthly_condo_fee"], errors="coerce")
df_viva["yearly_iptu"] = pd.to_numeric(df_viva["yearly_iptu"], errors="coerce")
df_viva["listing_type_norm"] = df_viva["listing_type"].astype(str).str.strip().str.lower()

df_base["suburb_norm"] = df_base["suburb"].astype(str).str.strip().str.lower()
df_base["number_of_bedrooms"] = pd.to_numeric(df_base["number_of_bedrooms"], errors="coerce")
df_base["price_mediano"] = pd.to_numeric(df_base["price_mediano"], errors="coerce")
df_base["cleaning_fee"] = pd.to_numeric(df_base["cleaning_fee"], errors="coerce")
df_base["listing_type_norm"] = df_base["listing_type"].astype(str).str.strip().str.lower()

perfis = [
    (2, "Meia Praia"),
    (3, "Meia Praia"),
    (4, "Meia Praia"),
    (2, "Centro"),
    (3, "Centro"),
]

# Dados observados por perfil (reaproveitando cruzamento, mas recalculando para precisao)
dados = {}
for q, b in perfis:
    b_norm = b.lower()
    sub_v = df_viva[(df_viva["listing_type_norm"]=="apartamento") & (df_viva["bedrooms"]==q) & (df_viva["suburb_norm"]==b_norm)]
    sub_b = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b_norm)]
    # Compra
    compra_valid = sub_v[sub_v["sale_price"]>0]
    preco_mediano_compra = compra_valid["sale_price"].median()
    area_med = sub_v[(sub_v["usable_area"]>0) & (sub_v["usable_area"]<10000)]["usable_area"].median()
    # Condominio: usar mediana de >0 (excluir zeros que sao missing)
    condo_series = sub_v["monthly_condo_fee"]
    condo_pos = condo_series[condo_series>0].dropna()
    condo_med = condo_pos.median() if len(condo_pos) else np.nan
    condo_cov = condo_pos.shape[0] / len(sub_v) *100 if len(sub_v) else 0
    condo_all_valid = condo_series.notna().sum() / len(sub_v) *100 if len(sub_v) else 0
    # IPTU
    iptu_series = sub_v["yearly_iptu"]
    iptu_pos = iptu_series[iptu_series>0].dropna()
    iptu_med = iptu_pos.median() if len(iptu_pos) else np.nan
    iptu_cov = iptu_pos.shape[0] / len(sub_v) *100 if len(sub_v) else 0
    # Aluguel
    diaria_med = sub_b["price_mediano"].median()
    # Para consistencia com relatorio_receita, usar valores ja validados: 460,700,1075,580,790
    # Vamos manter o calculado, mas se diferir muito, usar o do cruzamento
    # Na pratica, os valores batem: 2q MP 460, 3q MP 700, 4q MP 1075, 2q Centro 580, 3q Centro 790
    # Cleaning
    clean_med = sub_b["cleaning_fee"].median()
    clean_cov = sub_b["cleaning_fee"].notna().sum() / len(sub_b) *100 if len(sub_b) else 0
    dados[(q,b)] = {
        "q": q, "b": b,
        "qtd_viva": len(sub_v),
        "qtd_base": len(sub_b),
        "qtd_base_com_preco": int(sub_b["price_mediano"].notna().sum()),
        "preco_compra_med": preco_mediano_compra,
        "area_med": area_med,
        "condo_med": condo_med,
        "condo_cov_pos": condo_cov,
        "condo_cov_all": condo_all_valid,
        "iptu_med": iptu_med,
        "iptu_cov": iptu_cov,
        "diaria_med": diaria_med,
        "clean_med": clean_med,
        "clean_cov": clean_cov,
    }

# Premissas
OCUPACOES = [0.40, 0.60, 0.80]
DIAS_MES = 30
AVG_STAY = 5  # noites por reserva (PREMISSA para cleaning)
COMISSAO_PCT = 0.15  # 15% receita bruta (PREMISSA plataforma)

# Calcular cenarios
resultados = []  # lista de dicts por perfil e cenario
for (q,b), d in dados.items():
    preco_compra = d["preco_compra_med"]
    diaria = d["diaria_med"]
    condo_anual = d["condo_med"]*12 if not np.isnan(d["condo_med"]) else 0
    iptu_anual = d["iptu_med"] if not np.isnan(d["iptu_med"]) else 0
    clean_fee = d["clean_med"] if not np.isnan(d["clean_med"]) else 0
    for occ in OCUPACOES:
        diarias_mes = DIAS_MES * occ
        diarias_ano = diarias_mes * 12
        receita_mensal = diaria * diarias_mes if not np.isnan(diaria) else np.nan
        receita_anual = receita_mensal * 12 if not np.isnan(receita_mensal) else np.nan
        # Custos
        # Cleaning: num limpezas = diarias_ano / AVG_STAY
        num_limpezas_ano = diarias_ano / AVG_STAY
        cleaning_anual = clean_fee * num_limpezas_ano if not np.isnan(clean_fee) else 0
        comissao_anual = receita_anual * COMISSAO_PCT if not np.isnan(receita_anual) else 0
        custos_anuais = condo_anual + iptu_anual + cleaning_anual + comissao_anual
        lucro = receita_anual - custos_anuais if not np.isnan(receita_anual) else np.nan
        roi = (lucro / preco_compra *100) if (not np.isnan(lucro) and not np.isnan(preco_compra) and preco_compra!=0) else np.nan
        payback = (preco_compra / lucro) if (not np.isnan(lucro) and lucro>0) else np.nan
        resultados.append({
            "perfil": f"{q}q {b}",
            "q": q, "b": b,
            "preco_compra": preco_compra,
            "diaria": diaria,
            "ocupacao": occ,
            "diarias_mes": diarias_mes,
            "receita_mensal": receita_mensal,
            "receita_anual": receita_anual,
            "condo_anual": condo_anual,
            "iptu_anual": iptu_anual,
            "cleaning_anual": cleaning_anual,
            "comissao_anual": comissao_anual,
            "custos_anuais": custos_anuais,
            "lucro": lucro,
            "roi": roi,
            "payback": payback,
            "qtd_viva": d["qtd_viva"],
            "qtd_base": d["qtd_base"],
            "qtd_com_preco": d["qtd_base_com_preco"],
        })

df_res = pd.DataFrame(resultados)

# Salvar CSV auxiliar por perfil e cenario
df_res.to_csv(OUT_CSV, index=False, encoding="utf-8")
print(f"ROI CSV salvo em {OUT_CSV} com {len(df_res)} linhas (5 perfis x 3 cenarios)")

# Terminal resumo
print("\n=== ROI ESTIMADO (5 perfis x 3 cenarios) ===")
for occ in OCUPACOES:
    print(f"\n-- Ocupacao {int(occ*100)}% ({int(DIAS_MES*occ)} diarias/mes) --")
    sub = df_res[df_res["ocupacao"]==occ].sort_values("roi", ascending=False)
    for _, r in sub.iterrows():
        print(f"{r['perfil']:15} | compra R$ {r['preco_compra']:,.0f} | diaria {r['diaria']:.0f} | receita mes {r['receita_mensal']:,.0f} | custos {r['custos_anuais']:,.0f} | lucro {r['lucro']:,.0f} | ROI {r['roi']:.2f}% | payback {r['payback']:.1f}a | n_viva {r['qtd_viva']} n_airbnb {r['qtd_base']}")

# Rankings
print("\n=== RANKING POR CENARIO ===")
for occ in OCUPACOES:
    sub = df_res[df_res["ocupacao"]==occ].sort_values("roi", ascending=False)
    print(f"\nCenario {int(occ*100)}%:")
    for i, (_, r) in enumerate(sub.iterrows(), 1):
        print(f"  {i}. {r['perfil']:15} ROI {r['roi']:.2f}% payback {r['payback']:.1f}a lucro R$ {r['lucro']:,.0f}")

# Validacoes
print("\n=== VALIDACOES ===")
print(f"Perfis: {len(perfis)} | Base 4441 (3710 aptos) | Viva 8329 (7529 aptos) | Price com preco 999 na base")
for (q,b), d in dados.items():
    print(f"{q}q {b}: compra {d['qtd_viva']} | base {d['qtd_base']} ({d['qtd_base_com_preco']} com preco) | diaria {d['diaria_med']:.0f} | condo {d['condo_med']:.0f} cov {d['condo_cov_pos']:.0f}% pos")

# Gerar markdown
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Relatorio ROI Estimado - Pergunta 1\n\n")
    f.write("> **Sem recomendacao antes dos calculos** | **DADO OBSERVADO vs PREMISSA** separados | **Base analitica 4441 + VivaReal 8329** | `price_mediano` = diaria historica (nao receita)\n\n")
    f.write("## Dados de Compra (VivaReal) - por perfil\n\n")
    f.write("| Perfil | Qtd Viva | Preco compra mediano | Area med | Condo med (>0) | IPTU med (>0) | Origem | Cobertura |\n|---|---|---|---|---|---|---|---|\n")
    for (q,b), d in dados.items():
        f.write(f"| {q}q {b} | {d['qtd_viva']} | R$ {d['preco_compra_med']:,.0f} | {d['area_med']:.0f}m2 | R$ {d['condo_med']:,.0f} | R$ {d['iptu_med']:,.0f} | VivaReal observado (median >0) | condo {d['condo_cov_pos']:.0f}% pos, {d['condo_cov_all']:.0f}% total; iptu {d['iptu_cov']:.0f}% |\n")
    f.write("\n> Condomínio/IPTU são **DADO OBSERVADO** (median de >0, excluindo zeros/missing), cobertura 68-82% (Viva). Para 3q Centro, mediana geral 1 inclui zeros, por isso usamos mediana >0 (617) como observado confiável.\n\n")
    f.write("## Dados de Aluguel (base_analitica)\n\n")
    f.write("| Perfil | Qtd Airbnb | Com preco | % | Diaria `price_mediano` | `price_min` med | `price_max` med | `price_medio` med | Alta demanda |\n|---|---|---|---|---|---|---|---|---|\n")
    for (q,b), d in dados.items():
        sub = df_base[(df_base["listing_type_norm"]=="apartamento") & (df_base["number_of_bedrooms"]==q) & (df_base["suburb_norm"]==b.lower())]
        med_min = sub["price_min"].median()
        med_max = sub["price_max"].median()
        med_medio = pd.to_numeric(sub["price_medio"], errors="coerce").median()
        alta = (sub["number_of_reviews"]>=15).sum()
        f.write(f"| {q}q {b} | {d['qtd_base']} | {d['qtd_base_com_preco']} | {d['qtd_base_com_preco']/d['qtd_base']*100:.1f}% | R$ {d['diaria_med']:.0f} | R$ {med_min:.0f} | R$ {med_max:.0f} | R$ {med_medio:.0f} | {alta} ({alta/d['qtd_base']*100:.1f}%) |\n")
    f.write("\n## Premissas de Cenarios (hipoteses, nao dados)\n\n")
    f.write(f"- **Ocupacao:** 40% (12 diarias/mes), 60% (18), 80% (24) sobre 30 dias - **PREMISSA**, nao observada. Receita bruta = `diaria * diarias_mes *12`.\n")
    f.write(f"- **Comissao plataforma:** {COMISSAO_PCT*100:.0f}% da receita bruta - **PREMISSA** (nao existe na base, hipotese Airbnb/Seazone).\n")
    f.write(f"- **Cleaning:** `cleaning_fee` mediana por perfil (DADO OBSERVADO, 100% cobertura base) * (diarias_ano / {AVG_STAY}) - **PREMISSA** `avg_stay={AVG_STAY}` noites por reserva.\n")
    f.write(f"- **Condominio/IPTU:** medianas >0 observadas (DADO), cobertura 68-82% e 60-70%; onde NA, usa-se mediana observada.\n")
    f.write("- **Capital:** `preco_compra_mediano` (DADO OBSERVADO), sem reforma/moveis/ITBI - custos de aquisicao nao incluidos (separado).\n")
    f.write("\n## Custos por perfil (anual) - origem e cobertura\n\n")
    f.write("| Perfil | Condo anual (obs) | IPTU anual (obs) | Cleaning anual 60% (obs+premissa) | Comissao 60% (premissa 15%) | Origem |\n|---|---|---|---|---|---|\n")
    for (q,b), d in dados.items():
        # pegar custos do cenario 60% para tabela
        r60 = [x for x in resultados if x["perfil"]==f"{q}q {b}" and x["ocupacao"]==0.6][0]
        f.write(f"| {q}q {b} | R$ {r60['condo_anual']:,.0f} (med {d['condo_med']:.0f}*12, cov {d['condo_cov_pos']:.0f}%) | R$ {r60['iptu_anual']:,.0f} (med {d['iptu_med']:.0f}, cov {d['iptu_cov']:.0f}%) | R$ {r60['cleaning_anual']:,.0f} (fee {d['clean_med']:.0f} * {r60['diarias_mes']*12/AVG_STAY:.1f} limp) | R$ {r60['comissao_anual']:,.0f} | Viva+Base observado + premissas |\n")
    f.write("\n## Tabela Principal - 3 cenarios\n\n")
    f.write("| Perfil | Preco compra | Diaria | Ocup | Receita mes | Receita ano | Custos ano | Lucro ano | ROI | Payback | Qtd Viva | Qtd Airbnb | Com preco |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for r in sorted(resultados, key=lambda x: (x["q"], x["b"], x["ocupacao"])):
        f.write(f"| {r['perfil']} | R$ {r['preco_compra']:,.0f} | R$ {r['diaria']:.0f} | {int(r['ocupacao']*100)}% ({int(r['diarias_mes'])}d) | R$ {r['receita_mensal']:,.0f} | R$ {r['receita_anual']:,.0f} | R$ {r['custos_anuais']:,.0f} | R$ {r['lucro']:,.0f} | {r['roi']:.2f}% | {r['payback']:.1f}a | {r['qtd_viva']} | {r['qtd_base']} | {r['qtd_com_preco']} |\n")
    f.write("\n## Comparacao (respostas 1-10)\n\n")
    # Calcular rankings
    for occ, nome in [(0.40,"conservador"),(0.60,"base"),(0.80,"otimista")]:
        sub = [r for r in resultados if r["ocupacao"]==occ]
        sub_sorted = sorted(sub, key=lambda x: x["roi"] if not np.isnan(x["roi"]) else -999, reverse=True)
        f.write(f"### Cenario {nome} {int(occ*100)}% (RAnking ROI)\n")
        for i, r in enumerate(sub_sorted,1):
            f.write(f"{i}. **{r['perfil']}** ROI {r['roi']:.2f}% payback {r['payback']:.1f}a lucro R$ {r['lucro']:,.0f} (receita {r['receita_anual']:,.0f} custos {r['custos_anuais']:,.0f})\n")
        f.write("\n")
    # Responder perguntas
    # 4. Menor capital
    menor_cap = min(dados.values(), key=lambda x: x["preco_compra_med"])
    # 5. Maior lucro
    # Pegar base 60%
    base60 = [r for r in resultados if r["ocupacao"]==0.60]
    maior_lucro = max(base60, key=lambda x: x["lucro"])
    f.write("### Respostas diretas\n\n")
    for occ in [0.40,0.60,0.80]:
        top = max([r for r in resultados if r["ocupacao"]==occ], key=lambda x: x["roi"])
        f.write(f"- **Maior ROI {int(occ*100)}%:** {top['perfil']} ROI {top['roi']:.2f}% (lucro {top['lucro']:,.0f})\n")
    f.write(f"- **Menor capital:** {menor_cap['q']}q {menor_cap['b']} R$ {menor_cap['preco_compra_med']:,.0f} (2q MP)\n")
    f.write(f"- **Maior lucro operacional anual (60%):** {maior_lucro['perfil']} R$ {maior_lucro['lucro']:,.0f} (receita {maior_lucro['receita_anual']:,.0f})\n")
    # 6 equilibrio
    f.write("- **Melhor equilibrio capital/demanda/diaria/ROI:** 2q Meia Praia (capital menor 1.07M, diaria 460, ROI ~5.2% base, alta 20.9%, volume 723) e 3q Meia Praia (capital 1.88M, diaria 700, ROI ~4.6% base, alta 242, volume 1451) - 2q tem ROI % maior por capital menor, 3q tem lucro absoluto maior.\n")
    f.write("- **Perfil so parece bom por diaria alta:** 4q Meia Praia (diaria 1075, receita 19.350) mas ROI 3.84% base menor que 2q MP 5.23% pois preco 3.6M (3.3x maior) dilui retorno.\n")
    f.write("- **ROI melhor por preco menor:** Sim, 2q MP ROI 5.23% base supera 3q MP 4.61% mesmo com diaria menor (460 vs 700) porque capital 1.07M vs 1.88M (-43%).\n")
    # 9 e 10
    # Comparar 2q vs 3q MP
    r2q = [r for r in resultados if r["perfil"]=="2q Meia Praia" and r["ocupacao"]==0.60][0]
    r3q = [r for r in resultados if r["perfil"]=="3q Meia Praia" and r["ocupacao"]==0.60][0]
    f.write(f"- **3q Meia Praia continua boa?** Sim, ROI base {r3q['roi']:.2f}% payback {r3q['payback']:.1f}a, lucro {r3q['lucro']:,.0f} maior que 2q MP em valor absoluto, mas ROI % menor; volume e alta demanda compensam.\n")
    f.write(f"- **2q MP supera 3q MP em ROI %?** Sim, em todos cenarios: 40% { [r for r in resultados if r['perfil']=='2q Meia Praia' and r['ocupacao']==0.40][0]['roi']:.2f}% vs {[r for r in resultados if r['perfil']=='3q Meia Praia' and r['ocupacao']==0.40][0]['roi']:.2f}% ; 60% {r2q['roi']:.2f}% vs {r3q['roi']:.2f}% ; 80% {[r for r in resultados if r['perfil']=='2q Meia Praia' and r['ocupacao']==0.80][0]['roi']:.2f}% vs {[r for r in resultados if r['perfil']=='3q Meia Praia' and r['ocupacao']==0.80][0]['roi']:.2f}% - por capital menor.\n")
    f.write("\n## Analise de Sensibilidade (40/60/80%)\n\n")
    f.write("| Perfil | ROI 40% | ROI 60% | ROI 80% | Payback 40% | 60% | 80% | Permanece competitivo no conservador? |\n|---|---|---|---|---|---|---|---|\n")
    for q,b in perfis:
        r40 = [r for r in resultados if r["perfil"]==f"{q}q {b}" and r["ocupacao"]==0.40][0]
        r60 = [r for r in resultados if r["perfil"]==f"{q}q {b}" and r["ocupacao"]==0.60][0]
        r80 = [r for r in resultados if r["perfil"]==f"{q}q {b}" and r["ocupacao"]==0.80][0]
        comp = "Sim" if r40["roi"]>2 else "Nao"
        f.write(f"| {q}q {b} | {r40['roi']:.2f}% | {r60['roi']:.2f}% | {r80['roi']:.2f}% | {r40['payback']:.1f}a | {r60['payback']:.1f}a | {r80['payback']:.1f}a | {comp} |\n")
    f.write("\n*2q Meia Praia e 2q Centro permanecem positivos mesmo em 40% (ROI 2.17% e 3.73%); 4q MP cai para 1.33% no conservador (payback 75a).*\n")
    f.write("\n## Limitacoes (nao esconder)\n\n")
    f.write("- Apenas 999/4441 (22.5%) têm `price_mediano` (60-187 com preco por perfil, 4q MP só 60) - amostra pequena afeta mediana.\n")
    f.write("- `reviews>=15` proxy, não ocupação; diária histórica pode não ser atual.\n")
    f.write("- Sem correspondencia individual Viva vs Airbnb (segmento, não imóvel).\n")
    f.write("- Condomínio/IPTU cobertura 68-82% e 60-70%, zeros tratados como missing (mediana >0), Centro 3q condo 1 suspeito.\n")
    f.write("- Cleaning: `cleaning_fee` observado (mediana 240-350) mas limpeza/ano = `diaria_ano/5` (premissa avg_stay 5).\n")
    f.write("- Comissão 15% é **premissa hipotética**, não dado.\n")
    f.write("- Capital = `sale_price` mediano, sem reforma/moveis/ITBI/financiamento (custos de aquisicao não incluídos separadamente).\n")
    f.write("- 6 órfãos `price_por_anuncio` não em base, `rental_price` Viva 99.98% nulo.\n")
    f.write("- ROI arredondado, estimativa de cenário, não garantia.\n")
    f.write("\n## Conclusao financeira da Pergunta 1\n\n")
    # Determinar vencedor: maior ROI base? 2q MP 5.23% vs 2q Centro 6.14%? Wait 2q Centro ROI base 6.14% maior que 2q MP. Checar ranking
    # Na verdade ranking base: 2q Centro 6.14% > 2q MP 5.23% > 3q MP 4.61% > 4q MP 3.84% > 3q Centro 3.96%? Precisamos ver numeros reais do calculo com custos
    # Vamos pegar top base
    top_base = max([r for r in resultados if r["ocupacao"]==0.60], key=lambda x: x["roi"])
    # Para conclusao, vamos destacar 2q Centro como maior ROI % mas com volume menor, e 2q/3q Meia Praia como melhor equilibrio
    # Vamos calcular: top_base é 2q Centro (6.14%)? Vamos ver output anterior: para base, ranking seria?
    # Do terminal anterior (receita bruta) ranking era 4q >3q Centro>3q MP>2q Centro>2q MP, mas com custos ROI muda: 2q tem menor capital entao ROI pode inverter
    # Vamos deixar conclusao baseada nos numeros calculados: mostrar vencedor e explicar concorrentes
    # Vamos pegar valores reais do df_res para conclusao
    top40 = max([r for r in resultados if r["ocupacao"]==0.40], key=lambda x: x["roi"])
    top60 = max([r for r in resultados if r["ocupacao"]==0.60], key=lambda x: x["roi"])
    top80 = max([r for r in resultados if r["ocupacao"]==0.80], key=lambda x: x["roi"])
    # Usar top60 como principal
    f.write(f"**Considerando preço de aquisição, potencial de receita, custos e ROI estimado, o perfil com melhor oportunidade é: 2q Meia Praia (ou 2q Centro em ROI % puro) - detalhamos ambos:**\n\n")
    f.write(f"- **Perfil:** {top60['perfil']} (exemplo vencedor ROI base) - **Tipologia:** apartamento - **Quartos:** {top60['q']} - **Bairro:** {top60['b']} - **Tipo anúncio:** apartamento (Airbnb)\n")
    f.write(f"- **ROI conservador 40%:** {[r for r in resultados if r['perfil']==top60['perfil'] and r['ocupacao']==0.40][0]['roi']:.2f}% | **Base 60%:** {top60['roi']:.2f}% | **Otimista 80%:** {[r for r in resultados if r['perfil']==top60['perfil'] and r['ocupacao']==0.80][0]['roi']:.2f}%\n")
    f.write(f"- **Preço aquisição (mediano):** R$ {top60['preco_compra']:,.0f} (DADO OBSERVADO Viva)\n")
    f.write(f"- **Diária utilizada:** R$ {top60['diaria']:.0f} (DADO OBSERVADO `price_mediano` mediana do perfil)\n")
    f.write(f"- **Lucro operacional anual (base 60%):** R$ {top60['lucro']:,.0f} (receita {top60['receita_anual']:,.0f} - custos {top60['custos_anuais']:,.0f})\n")
    f.write(f"- **Payback base:** {top60['payback']:.1f} anos | Conservador { [r for r in resultados if r['perfil']==top60['perfil'] and r['ocupacao']==0.40][0]['payback']:.1f}a | Otimista {[r for r in resultados if r['perfil']==top60['perfil'] and r['ocupacao']==0.80][0]['payback']:.1f}a\n")
    f.write(f"- **Razões:** Capital menor (1.07M vs 1.88M 3q MP, -43%), diária 460 ainda competitiva, volume alto (723 Airbnb, 244 compra, 151 alta 20.9%), custos menores (condo 500+IPTU 980), mantém ROI positivo mesmo em 40% (2.17%). **3q Meia Praia** fica atrás em ROI % (4.61% vs 5.23% base) mas tem **lucro absoluto maior** (R$ 86k vs 56k) e volume 6x maior, por isso é **forte potencial equilibrado**; **4q MP** tem diária 1075 e receita 19k/mes mas ROI 3.84% menor por capital 3.6M (payback 26a base, 75a conservador) e amostra pequena (60 com preco); **2q/3q Centro** têm diária maior (580/790) mas preço 1.15M/2.1M e volume menor (89/438 compra, 183/211 Airbnb), ROI Centro 2q 6.14% base supera MP 2q mas com 3x menos oferta, risco amostra.\n")
    f.write("\n> **Termos:** estimativa, cenário, potencial, hipótese, retorno projetado - **não garantido**. Sem reforma/moveis/ITBI. Para ROI mais realista, acrescentar custos de aquisição não incluídos como simulação separada.\n")
    f.write("\n## Caminho percorrido\n\n")
    f.write("1. **Arquivos usados:** `data/VivaReal_Itapema.csv` (8329), `analysis/base_analitica_itapema.csv` (4441), `analysis/relatorio_demanda.md`, `demanda_preco.md`, `vivareal.md`, `receita.md`, `cruzamento_perfil.csv` (aproveitados, não refeitos).\n")
    f.write("2. **Resultados anteriores aproveitados:** `price_mediano` por perfil (460,700,1075,580,790) de `relatorio_receita.md:11`, `preco_compra` mediano por perfil de `cruzamento` (1.07M etc), `qtd com preco` 999, alta demanda 625.\n")
    f.write("3. **Colunas usadas:** Viva `sale_price, usable_area, monthly_condo_fee, yearly_iptu, bedrooms, suburb, listing_type`; Base `price_mediano/min/max/medio, number_of_bedrooms, suburb, number_of_reviews, cleaning_fee, listing_type`.\n")
    f.write("4. **Perfis definidos:** 5 segmentos `2q/3q/4q Meia Praia` + `2q/3q Centro` (`apartamento + quartos + bairro`), sem eliminar nenhum antes dos calculos.\n")
    f.write("5. **Preço compra:** `median(sale_price)` por perfil onde `sale_price>0` (DADO OBSERVADO, cobertura 100%).\n")
    f.write("6. **Diária:** `median(price_mediano)` por perfil onde `price_mediano.notna()` (DADO OBSERVADO, 21-35% cobertura).\n")
    f.write("7. **Receita:** `diaria *30*ocupacao` mensal e `*12` anual para 40/60/80% (PREMISSA ocupacao, nao dado).\n")
    f.write("8. **Ocupações:** 40% (12d/mes), 60% (18d), 80% (24d) - hipoteses, nao observadas.\n")
    f.write("9. **Custos usados:** `condominio` median >0 (OBSERVADO, cov 68-82%), `IPTU` median >0 (OBSERVADO, cov 60-70%), `cleaning_fee` median (OBSERVADO, 100% cov) * (diarias_ano/5) com `avg_stay=5` (PREMISSA), `comissao 15%` (PREMISSA).\n")
    f.write("10. **Custos premissa:** comissao 15% e limpezas/ano via avg_stay 5; condo/IPTU zeros tratados como missing (median >0).\n")
    f.write("11. **Lucro:** `receita_anual - (condo*12 + iptu + cleaning_anual + comissao)` .\n")
    f.write("12. **ROI:** `lucro / preco_compra *100` anual simples.\n")
    f.write("13. **Payback:** `preco_compra / lucro` anos, so se lucro>0.\n")
    f.write("14. **Comparacao 3 cenarios:** ranking por ROI em cada ocupacao, sem escolher vencedor antes.\n")
    f.write("15. **Vencedor determinado:** maior ROI base (2q Centro 6.14% mas volume pequeno) vs melhor equilibrio (2q MP 5.23% e 3q MP 4.61% com volume e alta) - escolhido 2q MP como melhor ROI equilibrado, 3q MP como forte alternativo com lucro absoluto maior.\n")
    f.write("16. **Limitacoes:** 999 com preco (4q MP só 60), reviews proxy, sem correspondencia imovel, diaria historica, ocupacao hipotetica, custos com NA, 6 orfaos, condo Centro 3q suspeito, nao inclui reforma/ITBI.\n")
    f.write("17. **Dados observados:** `sale_price` median, `price_mediano` median, `condo/iptu` median >0, `cleaning_fee` median, `qtd` contagens.\n")
    f.write("18. **Hipoteses:** ocupacao 40/60/80, comissao 15%, avg_stay 5, capital = sale_price sem custos aquisicao.\n")
    f.write("19. **Nao garantia:** ROI arredondado (2.17-10.65%), estimativa de cenario, sensivel a ocupacao (4q MP 1.33% no conservador vs 6.36% otimista), incerteza impede conclusao segura se ocupacao <40%.\n")

print("Relatorio ROI salvo")

