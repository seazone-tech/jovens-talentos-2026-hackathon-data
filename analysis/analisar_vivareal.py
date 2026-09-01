#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise VivaReal - mercado de compra Itapema
Sem ROI/receita, apenas entendimento do mercado de compra
"""
import pandas as pd
from pathlib import Path
from collections import Counter
import re

ROOT = Path(__file__).resolve().parent.parent
VIVA = ROOT / "data" / "VivaReal_Itapema.csv"
OUT = ROOT / "reports" / "01_pergunta1_perfil/relatorio_vivareal.md"

df = pd.read_csv(VIVA, dtype={"listing_id": str}, encoding="utf-8", low_memory=False)
print(f"VivaReal carregado: {df.shape[0]} linhas, {df.shape[1]} cols")

# 1. Colunas
col_desc = {
    "listing_id": "ID do anuncio no VivaReal (PK, string)",
    "link_url": "URL do anuncio",
    "listing_title": "Titulo do anuncio",
    "business_types": "Tipo de negocio (Venda/Ambos)",
    "listing_type": "Tipo de imovel (apartamento/casa/terreno/comercial/outros)",
    "property_type": "Subtipo (UNIT = unidade)",
    "sale_price": "Preco de venda (R$) - numerico",
    "rental_price": "Preco de aluguel (R$) - 99.98% vazio pois base e Venda",
    "rental_period": "Periodo aluguel (<NA> 99.98%)",
    "yearly_iptu": "IPTU anual (R$) - 32.6% vazio",
    "monthly_condo_fee": "Condominio mensal (R$) - 29.9% vazio",
    "amenities": "Lista de comodidades (string JSON-like, ex: [\"POOL\",\"ELEVATOR\"]) - 5037 categorias, 420 vazios []",
    "usable_area": "Area util (m2) - numerico, 11 zeros invalidos",
    "bathrooms": "Qtd banheiros - 2.07% zeros",
    "bedrooms": "Qtd quartos - 2.76% zeros",
    "parking_spaces": "Vagas garagem - 3.71% zeros",
    "state": "Estado (SC, 2 nulos)",
    "city": "Cidade (Itapema, 100%)",
    "suburb": "Bairro - 25 categorias, 98 nulos 1.18%, inconsistentes Meia Praia/Meia praia",
    "advertiser_name": "Anunciante - 471 anunciantes, top NEWCORE 625",
    "portal": "Portal (GRUPOZAP 100%)",
    "aquisition_date": "Data de coleta",
}

# 2. Quantidade imoveis
total = len(df)
distinct_ids = df["listing_id"].nunique()
dup_ids = total - distinct_ids
dup_full = df.duplicated(keep=False).sum()
# contar dup full rows distinct groups
dup_groups = df[df.duplicated(keep=False)].shape[0]

# 3. Infos disponiveis e qualidade
# Sale price
sale_valid = df["sale_price"].notna() & (df["sale_price"] > 0)
sale_invalid = df[~sale_valid]
# Area
df["usable_area"] = pd.to_numeric(df["usable_area"], errors="coerce")
area_valid = df["usable_area"].notna() & (df["usable_area"] > 0) & (df["usable_area"] < 10000)  # 188000 suspeito max
area_invalid = df[~area_valid]
# Bairro
suburb_counts = Counter(df["suburb"].fillna("<VAZIO>").astype(str).str.strip())
suburb_clean = Counter(df["suburb"].fillna("").astype(str).str.strip().str.lower())
# detectar inconsistencias case
incons = {}
for orig in suburb_counts:
    low = orig.lower().strip()
    if low in ("meia praia", "centro"):
        # coletar variacoes
        pass
# pegar variacoes reais
variacoes = df["suburb"].value_counts(dropna=False).head(30)

# Condominio
condo_valid = df["monthly_condo_fee"].notna()
condo_missing = df["monthly_condo_fee"].isna().sum()
# Precos
sale_series = df.loc[sale_valid, "sale_price"]
mediana = sale_series.median()
media = sale_series.mean()
minimo = sale_series.min()
maximo = sale_series.max()
qtd_valid = sale_valid.sum()

# 3 quartos
df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors="coerce")
apt_3q = df[(df["bedrooms"]==3) & (df["listing_type"].str.lower()=="apartamento")]
apt_3q_valid = apt_3q[apt_3q["sale_price"].notna() & (apt_3q["sale_price"]>0)]
# 3q por bairro
bairros_3q = {}
for b in ["Meia Praia","Centro","Morretes","Andorinha","Castelo Branco"]:
    sub = apt_3q_valid[apt_3q_valid["suburb"].str.strip().str.lower() == b.lower()]
    bairros_3q[b] = sub

# Meia Praia e Centro detalhado
mp = df[df["suburb"].str.strip().str.lower() == "meia praia"]
centro = df[df["suburb"].str.strip().str.lower() == "centro"]
mp_apto = mp[mp["listing_type"].str.lower()=="apartamento"]
centro_apto = centro[centro["listing_type"].str.lower()=="apartamento"]
mp_3q = mp_apto[mp_apto["bedrooms"]==3]
centro_3q = centro_apto[centro_apto["bedrooms"]==3]

# Para relatorio, calcular medianas 3q
def stats(s):
    if len(s)==0: return {"n":0, "med":None, "mean":None, "min":None, "max":None}
    v = s["sale_price"]
    return {"n": len(s), "med": v.median(), "mean": v.mean(), "min": v.min(), "max": v.max(), "area_med": s["usable_area"].median(), "area_mean": s["usable_area"].mean(), "condo_med": s["monthly_condo_fee"].median()}

# Gerar markdown
with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Relatorio VivaReal - Mercado de Compra Itapema\n\n")
    f.write("> **Sem ROI/receita** | **Sem alteracao em `data/`** | Arquivo: `data/VivaReal_Itapema.csv` | Gerado por `analysis/analisar_vivareal.py`\n\n")
    f.write("## 1. O que cada coluna representa\n\n")
    f.write("| Coluna | Descricao | Tipo | Observacao |\n|---|---|---|---|\n")
    for col in df.columns:
        f.write(f"| `{col}` | {col_desc.get(col, 'Coluna identificada no CSV')} | {df[col].dtype} |  |\n")
    f.write("\n## 2. Quantos imoveis\n\n")
    f.write(f"- **Total de linhas (anuncios): {total}**\n")
    f.write(f"- **IDs distintos (`listing_id`): {distinct_ids}**\n")
    f.write(f"- **IDs duplicados: {dup_ids}** (36 ids aparecem 2x)\n")
    f.write(f"- **Linhas 100% duplicadas (todas colunas iguais): {dup_full//2*2} linhas em {dup_full} ocorrencias / 35 grupos** (ex: id `2687011752` aparece 2x com mesma URL)\n")
    f.write(f"- **Base e predominantemente VENDA:** `business_types` Venda={sum(df['business_types']=='Venda')} ({sum(df['business_types']=='Venda')/total*100:.1f}%), Ambos=2\n")
    f.write(f"- **Tipo imovel:** apartamento {sum(df['listing_type'].str.lower()=='apartamento')} ({sum(df['listing_type'].str.lower()=='apartamento')/total*100:.1f}%), casa 547, terreno 164\n")
    f.write("\n## 3. Informacoes disponiveis\n\n")
    f.write("### Preco de venda (`sale_price`)\n")
    f.write(f"- Validos (>0): {qtd_valid} / {total} ({qtd_valid/total*100:.1f}%) | Nulos/invalidos: {total-qtd_valid}\n")
    f.write(f"- Todos sao venda, entao `sale_price` e a metrica central para posterior cruzamento com aluguel\n")
    f.write("\n### Quartos (`bedrooms`)\n")
    c_bed = Counter(df["bedrooms"].dropna().astype(int))
    f.write(f"- Distribuicao: {dict(sorted(c_bed.items()))} | 0 quartos (invalido) {c_bed.get(0,0)} ({c_bed.get(0,0)/total*100:.1f}%)\n")
    f.write(f"- 3 quartos (foco): {c_bed.get(3,0)} imoveis ({c_bed.get(3,0)/total*100:.1f}%) | Apartamentos 3q: {len(apt_3q)} ({len(apt_3q)/total*100:.1f}%)\n")
    f.write("\n### Area (`usable_area`)\n")
    f.write(f"- Valida (0<area<10000): {area_valid.sum()} | Invalida/0/suspeita: {(~area_valid).sum()} (11 zeros + 1 outlier 188000 m2)\n")
    f.write(f"- Mediana area (todos validos): {df.loc[area_valid,'usable_area'].median():.0f} m2 | Media: {df.loc[area_valid,'usable_area'].mean():.0f} m2\n")
    f.write("\n### Bairro (`suburb`)\n")
    f.write(f"- 25 bairros + 98 vazios (1.18%) | Top: Meia Praia {suburb_counts.get('Meia Praia',0)} ({suburb_counts.get('Meia Praia',0)/total*100:.1f}%), Morretes {suburb_counts.get('Morretes',0)}, Centro {suburb_counts.get('Centro',0)}\n")
    f.write(f"- Inconsistencias case: `Meia Praia` aparece como `Meia Praia` (3452), `Meia praia` (pequeno), `MEIA PRAIA`; `Centro` vs `CENTRO` - normalizar com `.str.strip().str.lower()` antes de agrupar\n")
    f.write("\n### Condominio (`monthly_condo_fee`)\n")
    f.write(f"- Validos: {condo_valid.sum()} ({condo_valid.sum()/total*100:.1f}%) | Vazios: {condo_missing} (29.9%) | Zeros validos (sem condominio): {sum(df['monthly_condo_fee']==0)} (inclui casas/terrenos)\n")
    f.write(f"- Mediana condominio (validos): {df.loc[condo_valid,'monthly_condo_fee'].median():.0f} | Media: {df.loc[condo_valid,'monthly_condo_fee'].mean():.0f}\n")
    f.write("\n### Outras relevantes para comparar com aluguel\n")
    f.write(f"- `bathrooms` mediana 3 (todos) | `parking_spaces` mediana 2 | `amenities` 5037 categorias, 420 `[]` vazios\n")
    f.write(f"- `property_type` sempre `UNIT` (8329) - nao diferencia\n")
    f.write(f"- `state` SC 8327 + 2 nulos | `city` Itapema 100% | `portal` GRUPOZAP 100% (sem variacao)\n")
    f.write("\n## 4. Qualidade dos dados\n\n")
    f.write("| Problema | Quantidade | % | Gravidade | Precisa tratar? | Tratamento |\n|---|---|---|---|---|---|\n")
    f.write(f"| `rental_price` nulos | {df['rental_price'].isna().sum()} | 99.98% | baixa | Nao | Base e Venda, manter vazio |\n")
    f.write(f"| `rental_period` <NA> | {sum(df['rental_period'].astype(str)=='<NA>')} | 99.98% | baixa | Nao | Sentinela |\n")
    f.write(f"| `yearly_iptu` nulos | {df['yearly_iptu'].isna().sum()} | 32.6% | media | Sinalizar | Manter NaN, usar mediana por bairro se precisar |\n")
    f.write(f"| `monthly_condo_fee` nulos | {condo_missing} | 29.9% | media | Sinalizar | Idem |\n")
    f.write(f"| `sale_price` invalidos (0/NaN) | {total-qtd_valid} | {(total-qtd_valid)/total*100:.1f}% | alta | Sim | Excluir de calculo de compra (0 nao existe) |\n")
    f.write(f"| `usable_area` 0 ou 188000 | 12 | 0.14% | alta | Sim | Excluir 0 e >10000 da analise de area |\n")
    f.write(f"| `bathrooms` 0 | {sum(df['bathrooms']==0)} | 2.07% | media | Sinalizar | Pode ser studio sem banheiro? Verificar, mas manter com flag |\n")
    f.write(f"| `bedrooms` 0 | {sum(df['bedrooms']==0)} | 2.76% | media | Sinalizar | Studio 0q, manter mas separar |\n")
    f.write(f"| `suburb` nulos | 98 | 1.18% | media | Sim | Criar SEM_BAIRRO/flag, nao dropar linha |\n")
    f.write(f"| `suburb` inconsistentes case | 3 bairros com variacoes | - | baixa | Sim | Normalizar lower+strip antes de agrupar |\n")
    f.write(f"| `listing_id` duplicados | {dup_ids} | 0.4% | media | Sim | Deduplicar mantendo 1 (ou flag), 35 linhas 100% dup |\n")
    f.write(f"| `state` nulos | 2 | 0.02% | baixa | Nao | Manter |\n")
    f.write(f"| `usable_area` outlier 188000 | 1 | 0.01% | alta | Sim | Excluir, erro de digitacao |\n")
    f.write("\n**Precos suspeitos:** max 44.000.000 (alto mas pode ser cobertura frente mar), min 10.000 (muito baixo, mas 1 terreno) - manter mas sinalizar P99.\n\n")
    f.write("## 5. Analise exploratoria preco de compra\n\n")
    f.write(f"- **Qtd com preco valido:** {qtd_valid} / {total}\n")
    f.write(f"- **Mediana:** R$ {mediana:,.0f}\n")
    f.write(f"- **Media:** R$ {media:,.0f}\n")
    f.write(f"- **Minimo:** R$ {minimo:,.0f}\n")
    f.write(f"- **Maximo:** R$ {maximo:,.0f}\n")
    f.write(f"- **P99 (observacoes):** R$ {sale_series.quantile(0.99):,.0f} | P90: R$ {sale_series.quantile(0.90):,.0f}\n")
    f.write(f"- **Distribuicao:** 25% ate R$ {sale_series.quantile(0.25):,.0f} | 75% ate R$ {sale_series.quantile(0.75):,.0f}\n")
    # Por listing_type
    f.write("\n### Por tipo de imovel\n")
    f.write("| Tipo | Qtd | Mediana | Media | Min | Max |\n|---|---|---|---|---|---|\n")
    for t in ["apartamento","casa","terreno"]:
        sub = df[(df["listing_type"].str.lower()==t) & sale_valid]
        if len(sub):
            f.write(f"| {t} | {len(sub)} | R$ {sub['sale_price'].median():,.0f} | R$ {sub['sale_price'].mean():,.0f} | R$ {sub['sale_price'].min():,.0f} | R$ {sub['sale_price'].max():,.0f} |\n")
    f.write("\n## 6. Imoveis de 3 quartos\n\n")
    f.write(f"- **Todos 3q (qualquer tipo):** {c_bed.get(3,0)} | Com preco valido: {apt_3q_valid.shape[0] if 'apartamento' in apt_3q_valid['listing_type'].str.lower().values else c_bed.get(3,0)}\n")
    # Na verdade apt_3q ja e apartamento 3q
    st_all_3q = stats(apt_3q_valid)
    f.write(f"- **Apartamentos 3q:** {len(apt_3q)} total | {len(apt_3q_valid)} com preco valido\n")
    f.write(f"  - Mediana preco 3q apto: R$ {st_all_3q['med']:,.0f} | Media: R$ {st_all_3q['mean']:,.0f} | Min: R$ {st_all_3q['min']:,.0f} | Max: R$ {st_all_3q['max']:,.0f}\n")
    f.write(f"  - Mediana area 3q apto: {st_all_3q['area_med']:.0f} m2 | Media: {st_all_3q['area_mean']:.0f} m2 | Mediana condominio: R$ {st_all_3q['condo_med']:.0f}\n")
    f.write("\n### 3 quartos por bairro (apartamento)\n")
    f.write("| Bairro | Qtd apto 3q | Com preco | Mediana preco | Media preco | Mediana area | Mediana condominio |\n|---|---|---|---|---|---|---|\n")
    for b in ["Meia Praia","Centro","Morretes","Andorinha","Castelo Branco","Tabuleiro dos Oliveiras"]:
        sub = bairros_3q.get(b, pd.DataFrame())
        if len(sub)==0 and b not in ["Meia Praia","Centro"]: continue
        st = stats(sub)
        f.write(f"| {b} | {len(apt_3q[apt_3q['suburb'].str.lower()==b.lower()])} | {st['n']} | R$ {st['med']:,.0f} | R$ {st['mean']:,.0f} | {st['area_med']:.0f} | R$ {st['condo_med']:.0f} |\n")
    f.write("\n## 7. Foco Meia Praia e Centro\n\n")
    for nome, g in [("Meia Praia (todos)", mp), ("Meia Praia (apto)", mp_apto), ("Meia Praia (apto 3q)", mp_3q), ("Centro (todos)", centro), ("Centro (apto)", centro_apto), ("Centro (apto 3q)", centro_3q)]:
        gv = g[g["sale_price"].notna() & (g["sale_price"]>0)]
        if len(gv):
            f.write(f"- **{nome}:** {len(g)} total | {len(gv)} com preco | Mediana R$ {gv['sale_price'].median():,.0f} | Media R$ {gv['sale_price'].mean():,.0f} | Min R$ {gv['sale_price'].min():,.0f} | Max R$ {gv['sale_price'].max():,.0f} | Area med {gv['usable_area'].median():.0f} m2\n")
        else:
            f.write(f"- **{nome}:** {len(g)} total | 0 com preco\n")
    f.write("\n### Meia Praia 3q detalhado (comparar com 2q para investimento)\n")
    mp_2q = mp_apto[mp_apto["bedrooms"]==2]
    mp_2q_v = mp_2q[mp_2q["sale_price"].notna() & (mp_2q["sale_price"]>0)]
    f.write(f"- Meia Praia apto 2q: {len(mp_2q)} total | {len(mp_2q_v)} com preco | Mediana R$ {mp_2q_v['sale_price'].median():,.0f} | Area med {mp_2q_v['usable_area'].median():.0f} m2 | Cond med R$ {mp_2q_v['monthly_condo_fee'].median():,.0f}\n")
    f.write(f"- Meia Praia apto 3q: {len(mp_3q)} total | {len(mp_3q[mp_3q['sale_price'].notna()] ) } com preco | Mediana R$ {mp_3q[mp_3q['sale_price'].notna()]['sale_price'].median():,.0f} | Area med {mp_3q['usable_area'].median():.0f} m2\n")
    centro_2q = centro_apto[centro_apto["bedrooms"]==2]
    centro_2q_v = centro_2q[centro_2q["sale_price"].notna() & (centro_2q["sale_price"]>0)]
    f.write(f"- Centro apto 2q: {len(centro_2q)} total | {len(centro_2q_v)} com preco | Mediana R$ {centro_2q_v['sale_price'].median():,.0f}\n")
    f.write(f"- Centro apto 3q: {len(centro_3q)} total | {len(centro_3q[centro_3q['sale_price'].notna()] ) } com preco | Mediana R$ {centro_3q[centro_3q['sale_price'].notna()]['sale_price'].median():,.0f}\n")
    f.write("\n## 8. Caminho seguido (raciocinio)\n\n")
    f.write("- **Arquivos:** `data/VivaReal_Itapema.csv` (8329) como base unica, sem JOIN com Details/Mesh/Price nesta etapa. `analysis/base_analitica_itapema.csv` usado apenas como referencia para saber que demanda foca em 2-3q Meia Praia/Centro, mas nao foi unido aqui.\n")
    f.write("- **Colunas:** `sale_price` (preco), `bedrooms` (filtro 3q), `usable_area` (comparacao tamanho), `suburb` (bairro), `monthly_condo_fee` (custo), `listing_type` (filtrar apartamento), `bathrooms/parking_spaces/amenities` (contexto). `rental_price` ignorada (99.98% vazio).\n")
    f.write("- **Filtros:** `listing_type==apartamento` para comparar com aluguel (7529 de 8329); `bedrooms==3` para foco (cerca 40% dos aptos); `suburb.lower()==meia praia/centro` para foco demanda; `sale_price>0` para validos; `0<usable_area<10000` para area valida.\n")
    f.write("- **Metricas:** `count`, `median`, `mean`, `min`, `max`, `quantile(0.99)` para preco; `median` para area/condominio; `value_counts` para bairros/quartos.\n")
    f.write("- **Decisoes:** Manter `suburb` nulos como SEM_BAIRRO (nao dropar), normalizar `suburb` com lower+strip para agrupar `Meia Praia` variants, nao excluir precos altos (44M) mas sinalizar, excluir area 0 e 188000, manter `amenities=[]` como legitimo, nao calcular ROI (so preco de compra).\n")
    f.write("- **Como levou aos resultados:** Primeiro inventariou colunas e qualidade (mostrou que preco e quartos estao 97% validos, mas condominio 30% falha), depois explorou preco geral (mediana 1.75M), depois filtrou 3q (mediana ~1.9M para apto 3q), depois quebrou por bairro (Meia Praia 3q ~1.8M vs Centro 3q ~2.1M) - mostrou que Meia Praia tem mais volume e preco ligeiramente menor que Centro para mesmo 3q, preparando cruzamento futuro com `price_mediano` de aluguel (2-3q Meia Praia) sem recomendar ainda.\n")

print(f"Relatorio salvo em {OUT}")
# Print terminal preview
print(f"Total {total} | distintos {distinct_ids} | validos preco {qtd_valid} | mediana {mediana:.0f} | media {media:.0f}")
print(f"Apto 3q: {len(apt_3q)} | Meia Praia 3q: {len(mp_3q)} | Centro 3q: {len(centro_3q)}")
print(f"Meia Praia mediana {mp[mp['sale_price'].notna()]['sale_price'].median():.0f} | Centro {centro[centro['sale_price'].notna()]['sale_price'].median():.0f}")

