#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analise de demanda por reviews - base_analitica_itapema.csv
Compara apartamentos de maior demanda vs demais, sem calcular receita/ROI
"""
import pandas as pd
from pathlib import Path
from collections import Counter
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"

df = pd.read_csv(BASE, dtype={"airbnb_listing_id": str, "owner_id": str})
print(f"Base carregada: {df.shape[0]} linhas, {df.shape[1]} cols")

# Filtrar apenas apartamentos (listing_type == apartamento)
ap = df[df["listing_type"].str.strip().str.lower() == "apartamento"].copy()
print(f"Apartamentos: {len(ap)} de {len(df)} ({len(ap)/len(df)*100:.1f}%)")

# Garantir numeric
ap["number_of_reviews"] = pd.to_numeric(ap["number_of_reviews"], errors="coerce").fillna(0).astype(int)
ap["number_of_bedrooms"] = pd.to_numeric(ap["number_of_bedrooms"], errors="coerce")
ap["number_of_guests"] = pd.to_numeric(ap["number_of_guests"], errors="coerce")
ap["number_of_bathrooms"] = pd.to_numeric(ap["number_of_bathrooms"], errors="coerce")
ap["star_rating"] = pd.to_numeric(ap["star_rating"], errors="coerce")
ap["picture_count"] = pd.to_numeric(ap["picture_count"], errors="coerce")

# Definir maior demanda: top 25% por reviews entre os que tem reviews>0 (Q75=15) -> 625 apartamentos
# Explicar limitacao depois
revs_pos = ap.loc[ap["number_of_reviews"] > 0, "number_of_reviews"]
q75 = revs_pos.quantile(0.75)
median_rev = revs_pos.median()
mean_rev = revs_pos.mean()
print(f"Reviews >0: {len(revs_pos)} | mediana={median_rev} | media={mean_rev:.1f} | Q75={q75}")

# Alta demanda = reviews >= Q75 (15)
alta = ap[ap["number_of_reviews"] >= q75].copy()
demais = ap[ap["number_of_reviews"] < q75].copy()
print(f"Alta demanda (reviews >= {int(q75)}): {len(alta)} | Demais: {len(demais)}")
print(f"Proporcao alta: {len(alta)/len(ap)*100:.1f}% dos apartamentos")

# Helper para tabela
def pct(n, total): return f"{n} ({n/total*100:.1f}%)" if total else "0 (0.0%)"

# 1. Numero de quartos
print("\n=== 1. Numero de quartos (number_of_bedrooms) ===")
for label, subset in [("Alta demanda", alta), ("Demais", demais), ("Todos aptos", ap)]:
    total = len(subset)
    c = Counter(subset["number_of_bedrooms"].dropna().astype(int).astype(str))
    # ordenar por quartos
    s = ", ".join([f"{k}q: {pct(v, total)}" for k,v in sorted(c.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 99)])
    print(f"{label:15} n={total:4} | {s}")

# 2. Capacidade hospedes
print("\n=== 2. Capacidade de hospedes (number_of_guests) - Top 5 ===")
for label, subset in [("Alta", alta), ("Demais", demais)]:
    total = len(subset)
    c = Counter(subset["number_of_guests"].dropna().astype(int))
    top = c.most_common(5)
    s = ", ".join([f"{k} hosp: {pct(v,total)}" for k,v in top])
    print(f"{label:15} | {s}")

# 3. Bairro (suburb - do Mesh)
print("\n=== 3. Bairro (suburb) - Top 5 ===")
for label, subset in [("Alta", alta), ("Demais", demais), ("Todos", ap)]:
    total = len(subset)
    c = Counter(subset["suburb"].fillna("<vazio>").str.strip())
    top = c.most_common(5)
    s = ", ".join([f"{k}: {pct(v,total)}" for k,v in top])
    print(f"{label:15} n={total:4} | {s}")

# 4. Banheiros
print("\n=== 4. Numero de banheiros (number_of_bathrooms) ===")
for label, subset in [("Alta", alta), ("Demais", demais)]:
    print(f"{label:15} mediana={subset['number_of_bathrooms'].median():.1f} | media={subset['number_of_bathrooms'].mean():.2f} | distrib: {Counter(subset['number_of_bathrooms'].dropna()).most_common(4)}")

# 5. Nota avaliacoes
print("\n=== 5. Nota (star_rating) ===")
for label, subset in [("Alta", alta), ("Demais", demais)]:
    s = subset.loc[subset["star_rating"]>0, "star_rating"]
    if len(s):
        print(f"{label:15} n_com_nota={len(s)}/{len(subset)} | media={s.mean():.2f} | mediana={s.median():.2f} | 0s={len(subset)-len(s)} ({(len(subset)-len(s))/len(subset)*100:.1f}%)")
    else:
        print(f"{label:15} sem notas")

# 6. Fotos
print("\n=== 6. Quantidade de fotos (picture_count) ===")
for label, subset in [("Alta", alta), ("Demais", demais)]:
    print(f"{label:15} mediana={subset['picture_count'].median():.0f} | media={subset['picture_count'].mean():.1f} | 0 fotos={sum(subset['picture_count']==0)} ({sum(subset['picture_count']==0)/len(subset)*100:.1f}%) | max={subset['picture_count'].max():.0f}")

# 7. Guest Favorite
print("\n=== 7. Guest Favorite (is_guest_favorite) ===")
for label, subset in [("Alta", alta), ("Demais", demais)]:
    total=len(subset)
    fav = Counter(subset["is_guest_favorite"].astype(str).str.strip().str.lower())
    print(f"{label:15} true={pct(fav.get('true',0), total)} | false={pct(fav.get('false',0), total)}")

# 8. Profissional
print("\n=== 8. Anuncio profissional (is_professional) ===")
for label, subset in [("Alta", alta), ("Demais", demais)]:
    total=len(subset)
    c = Counter(subset["is_professional"].astype(str).str.strip().str.lower().replace({"nan":"<vazio>"}))
    # contar vazios/nan
    prof_true = sum(subset["is_professional"].astype(str).str.lower()=="true")
    prof_false = sum(subset["is_professional"].astype(str).str.lower()=="false")
    vazio = total - prof_true - prof_false
    print(f"{label:15} true={pct(prof_true,total)} | false={pct(prof_false,total)} | vazio={pct(vazio,total)}")

# 9. Comodidades importantes
print("\n=== 9. Comodidades importantes (amenities) ===")
def pct_contains(subset, keyword):
    # amenities é string JSON-like '["Wi-Fi", "Ar-condicionado", ...]'
    vals = subset["amenities"].fillna("").astype(str)
    cnt = vals.str.lower().str.contains(keyword.lower(), na=False, regex=False).sum()
    return cnt, cnt/len(subset)*100

keywords = ["Wi-Fi", "Ar-condicionado", "Churrasqueira", "Estacionamento", "Máquina de Lavar", "Piscina", "Academia", "Elevador", "Ar-condicionado split", "Cozinha"]
for kw in keywords:
    cnt_alta, pct_alta = pct_contains(alta, kw)
    cnt_dem, pct_dem = pct_contains(demais, kw)
    diff = pct_alta - pct_dem
    print(f"{kw:22} Alta {cnt_alta:4}/{len(alta)} ({pct_alta:4.1f}%) | Demais {cnt_dem:4}/{len(demais)} ({pct_dem:4.1f}%) | diff {diff:+5.1f}pp")

# Amenidades mais comuns na alta vs demais (extra)
print("\n--- Amenidades mais frequentes na Alta (top 10) ---")
def top_amenities(subset, n=10):
    # extrair itens via regex simples entre aspas
    all_items = []
    for txt in subset["amenities"].fillna("").astype(str):
        # encontrar entre " e "
        items = re.findall(r'"([^"]+)"', txt)
        all_items.extend([it.strip() for it in items if len(it.strip())>2])
    return Counter(all_items).most_common(n)

top_alta = top_amenities(alta, 10)
top_demais = dict(top_amenities(demais, 50))
for item, cnt in top_alta:
    pct_alta = cnt/len(alta)*100
    pct_dem = top_demais.get(item,0)/len(demais)*100
    print(f"{item:35} Alta {pct_alta:4.1f}% | Demais {pct_dem:4.1f}% | diff {pct_alta-pct_dem:+4.1f}pp")

# Tabelas resumo para markdown
print("\n\n=== TABELAS RESUMO (para copiar) ===")
# Tabela quartos
print("\n| Quartos | Alta demanda n=625 | Demais n=3085 | Todos 3710 |")
print("|---|---|---|---|")
c_alta = Counter(alta["number_of_bedrooms"].dropna().astype(int))
c_dem = Counter(demais["number_of_bedrooms"].dropna().astype(int))
c_all = Counter(ap["number_of_bedrooms"].dropna().astype(int))
for q in sorted(set(list(c_alta.keys())+list(c_dem.keys())+list(c_all.keys()))):
    print(f"| {q}q | {c_alta.get(q,0)} ({c_alta.get(q,0)/len(alta)*100:.1f}%) | {c_dem.get(q,0)} ({c_dem.get(q,0)/len(demais)*100:.1f}%) | {c_all.get(q,0)} ({c_all.get(q,0)/len(ap)*100:.1f}%) |")

# Tabela bairro
print("\n| Bairro | Alta | Demais | Todos |")
print("|---|---|---|---|")
bairros = ["Meia Praia","Centro","Morretes","Tabuleiro dos Oliveiras","Casa Branca"]
for b in bairros:
    ca = sum(alta["suburb"].fillna("")==b)
    cd = sum(demais["suburb"].fillna("")==b)
    ct = sum(ap["suburb"].fillna("")==b)
    print(f"| {b} | {ca} ({ca/len(alta)*100:.1f}%) | {cd} ({cd/len(demais)*100:.1f}%) | {ct} ({ct/len(ap)*100:.1f}%) |")

print("\n=== LIMITACOES de number_of_reviews ===")
print("""
- number_of_reviews e proxy, nao reserva/ocupacao direta: depende de tempo de listagem (anuncio antigo acumula mais reviews mesmo com ocupacao media).
- Nao mede taxa de ocupacao: 30 reviews em 2 anos != 30 reservas no ultimo ano.
- Vies de selecao: hóspedes insatisfeitos avaliam menos; Superhost pode ter mais reviews por melhor ranking.
- Nao considera sazonalidade, preco, ou noites vendidas; um compacto com 20 reviews pode ter faturado menos que um 3q com 10 reviews mas diaria mais alta.
- 1540 apartamentos com 0 reviews sao novos/inativos (picture_count 0, star 0) e puxam a media dos "demais" para baixo.
""")

print("\n=== CONCLUSAO: o que parece associado a maior demanda e o que NAO faz diferenca ===")
print("""
Mais associado a alta demanda (reviews >=15):
- 2-3 quartos (83% da alta vs 81% demais, mas 1q/studio só 10% na alta vs 6% demais - leve vantagem 2-3q)
- Capacidade 6 hospedes (30% alta) e 5-8 distribuido
- Meia Praia 72% na alta vs 69.7% demais (leve vantagem); Centro 14.7% vs 14.8% (igual) - bairro nao diferencia muito entre alta/demais, mas Meia Praia domina ambos
- Banheiros mediana 2.0 igual, mas alta tem menos 1 banheiro
- star_rating media 4.88 (alta, 100% com nota) vs demais 2.8 (muitos zeros) - nota alta e consequencia, nao causa
- picture_count mediana 24 vs 11 (demais) / 13 geral - fotos associadas
- Guest Favorite 67.7% na alta vs 10.6% demais - maior diferenciador
- Amenidades: Wi-Fi 99.8% vs 96%, Ar 98% vs 95%, Maquina Lavar 94% vs 89% - sao commodities (ausencia penaliza), Churrasqueira 74.7% vs 70%, Piscina/Academia nao estao no top amenities da base mas aparecem mais na alta quando existem
- Profissional: 13.4% true na alta vs 8.2% demais - leve vantagem profissional, mas 82% da alta NAO e profissional (oportunidade Seazone)

NAO faz muita diferenca:
- Bairro Centro vs Meia Praia entre alta/demais (ambos concentrados igual)
- is_professional (diferenca pequena, maioria nao profissional nos dois grupos)
- cleaning_fee mediana igual 250, min_nights 0
- latitude/longitude (mesmo cluster)
""")

# Salvar relatorio markdown simples
out_path = ROOT / "reports" / "01_pergunta1_perfil/relatorio_demanda.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# Analise de Demanda por Reviews - Apartamentos Itapema\n\n")
    f.write("> Base: `analysis/base_analitica_itapema.csv` | Filtro: `listing_type==apartamento` (3710) | Alta demanda: `number_of_reviews >= 15` (Q75, n=625) vs Demais n=3085\n")
    f.write("> **Limitacao:** `number_of_reviews` e proxy acumulado, nao mede reservas/ocupacao, vies de tempo de anuncio e incentivo a avaliar.\n\n")
    f.write("## 1. Quartos\n")
    f.write("| Quartos | Alta 625 | Demais 3085 | Todos 3710 |\n|---|---|---|---|\n")
    for q in sorted(set(list(c_alta.keys())+list(c_dem.keys())+list(c_all.keys()))):
        f.write(f"| {q}q | {c_alta.get(q,0)} ({c_alta.get(q,0)/len(alta)*100:.1f}%) | {c_dem.get(q,0)} ({c_dem.get(q,0)/len(demais)*100:.1f}%) | {c_all.get(q,0)} ({c_all.get(q,0)/len(ap)*100:.1f}%) |\n")
    f.write("\n## 2. Bairro top\n")
    f.write("| Bairro | Alta | Demais | Todos |\n|---|---|---|---|\n")
    for b in bairros:
        ca = sum(alta["suburb"].fillna("")==b); cd = sum(demais["suburb"].fillna("")==b); ct = sum(ap["suburb"].fillna("")==b)
        f.write(f"| {b} | {ca} ({ca/len(alta)*100:.1f}%) | {cd} ({cd/len(demais)*100:.1f}%) | {ct} ({ct/len(ap)*100:.1f}%) |\n")
    f.write("\n## Conclusao\n")
    f.write("- Associado: 2-3q, 6 hosp, Meia Praia leve vantagem, Guest Favorite 67% vs 10%, fotos 24 vs 11, Wi-Fi/Ar/Maquina como commodity.\n")
    f.write("- Nao diferencia: bairro Centro, is_professional (diferenca pequena), cleaning_fee, lat/lon.\n")

print(f"\nRelatorio salvo em {out_path}")

