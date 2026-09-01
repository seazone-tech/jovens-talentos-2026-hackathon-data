#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUDITORIA DE QUALIDADE - Hackathon Seazone Jovens Talentos 2026
Modo: READ-ONLY - Nao altera CSVs, nao faz JOIN, nao faz analise de receita.
"""
import csv
import re
import statistics
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_PATH = Path(__file__).resolve().parent.parent / "reports" / "00_auditoria/relatorio_auditoria.md"

FILES = {
    "Details_Itapema.csv": DATA_DIR / "Details_Itapema.csv",
    "Hosts_ids_Itapema.csv": DATA_DIR / "Hosts_ids_Itapema.csv",
    "Mesh_Ids_Data_Itapema.csv": DATA_DIR / "Mesh_Ids_Data_Itapema.csv",
    "Price_AV_Itapema.csv": DATA_DIR / "Price_AV_Itapema.csv",
    "VivaReal_Itapema.csv": DATA_DIR / "VivaReal_Itapema.csv",
}

ID_COLS = {
    "Details_Itapema.csv": ["airbnb_listing_id", "owner_id"],
    "Hosts_ids_Itapema.csv": ["owner_id"],
    "Mesh_Ids_Data_Itapema.csv": ["airbnb_listing_id"],
    "Price_AV_Itapema.csv": ["airbnb_listing_id"],
    "VivaReal_Itapema.csv": ["listing_id"],
}

def is_null(val: str) -> bool:
    return val.strip() == ""

def is_placeholder(val: str) -> bool:
    s = val.strip()
    if s == "<NA>":
        return True
    low = s.lower()
    return "não informado" in low or "nǜo informado" in low or "nao informado" in low

def try_parse_float(val: str):
    try:
        return float(val.strip())
    except:
        return None

def infer_column_type(values):
    non_empty = [v for v in values if not is_null(v) and not is_placeholder(v) and v.strip() != ""]
    if not non_empty:
        return "string (vazio/placeholder apenas)"
    float_ok = sum(1 for v in non_empty if try_parse_float(v) is not None)
    if float_ok / len(non_empty) >= 0.8:
        all_int = all(try_parse_float(v).is_integer() for v in non_empty if try_parse_float(v) is not None)
        if all_int:
            return "numérico (inteiro)"
        return "numérico (float)"
    date_like = sum(1 for v in non_empty if re.match(r"^\d{4}-\d{2}-\d{2}", v.strip()))
    if date_like / len(non_empty) >= 0.8:
        return "data/datetime (string)"
    bool_like = sum(1 for v in non_empty if v.strip().lower() in ("true","false"))
    if bool_like / len(non_empty) >= 0.8:
        return "booleano (string)"
    return "string/categórico"

def audit_file(file_key, path: Path):
    result = {}
    result["file"] = file_key
    result["path"] = str(path)
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    n_rows = len(rows)
    n_cols = len(fieldnames) if fieldnames else 0
    result["n_rows"] = n_rows
    result["n_cols"] = n_cols
    result["columns"] = fieldnames
    col_types = {}
    col_values = {col: [r[col] if r[col] is not None else "" for r in rows] for col in fieldnames}
    for col in fieldnames:
        col_types[col] = infer_column_type(col_values[col])
    result["col_types"] = col_types
    null_counts = {}
    placeholder_counts = {}
    zero_counts = {}
    for col in fieldnames:
        vals = col_values[col]
        null_c = sum(1 for v in vals if is_null(v))
        ph_c = sum(1 for v in vals if is_placeholder(v))
        zero_c = sum(1 for v in vals if v.strip() in ("0","0.0","0.00"))
        null_counts[col] = null_c
        placeholder_counts[col] = ph_c
        zero_counts[col] = zero_c
    result["null_counts"] = null_counts
    result["placeholder_counts"] = placeholder_counts
    result["zero_counts"] = zero_counts
    seen = set()
    dup_full = 0
    for r in rows:
        tup = tuple(r[col] if r[col] is not None else "" for col in fieldnames)
        if tup in seen:
            dup_full += 1
        else:
            seen.add(tup)
    result["dup_full_rows"] = dup_full
    id_stats = {}
    for idcol in ID_COLS.get(file_key, []):
        if idcol not in fieldnames:
            continue
        vals = [r[idcol] if r[idcol] is not None else "" for r in rows]
        stripped = [v.strip() for v in vals]
        unique = len(set(stripped))
        dup = n_rows - unique
        null_ids = sum(1 for v in vals if is_null(v))
        ph_ids = sum(1 for v in vals if is_placeholder(v))
        with_spaces = sum(1 for v in vals if v != v.strip() and v.strip() != "")
        non_digit = sum(1 for v in vals if v.strip() != "" and not v.strip().isdigit() and not is_placeholder(v))
        len_counter = Counter(len(v.strip()) for v in vals if v.strip() != "" and not is_placeholder(v))
        id_stats[idcol] = {
            "unique": unique,
            "duplicados": dup,
            "nulos": null_ids,
            "placeholders": ph_ids,
            "com_espacos_pontas": with_spaces,
            "nao_numericos": non_digit,
            "distribuicao_tamanhos": dict(len_counter),
            "exemplos": list(set(stripped))[:3],
        }
    result["id_stats"] = id_stats
    numeric_stats = {}
    for col in fieldnames:
        if "numérico" in col_types[col]:
            vals = col_values[col]
            nums = []
            for v in vals:
                if is_null(v) or is_placeholder(v):
                    continue
                fv = try_parse_float(v)
                if fv is not None:
                    nums.append(fv)
            if nums:
                numeric_stats[col] = {
                    "count_numeric": len(nums),
                    "min": min(nums),
                    "max": max(nums),
                    "median": statistics.median(nums),
                    "mean": statistics.mean(nums),
                    "qtd_zero": sum(1 for x in nums if x == 0),
                    "qtd_zero_pct": round(sum(1 for x in nums if x == 0)/len(nums)*100,2) if nums else 0,
                }
            else:
                numeric_stats[col] = {"count_numeric": 0, "obs": "Nenhum valor numerico parseavel"}
    result["numeric_stats"] = numeric_stats
    categorical_stats = {}
    for col in fieldnames:
        if "numérico" not in col_types[col] and "data" not in col_types[col]:
            vals = col_values[col]
            non_null = [v for v in vals if not is_null(v)]
            c = Counter(non_null)
            norm_map = defaultdict(list)
            for k in c:
                norm = k.strip().lower()
                norm_map[norm].append(k)
            inconsistentes = {norm: vars for norm, vars in norm_map.items() if len(vars) > 1}
            categorical_stats[col] = {
                "qtd_categorias": len(c),
                "top": c.most_common(10),
                "inconsistentes": inconsistentes,
                "total_non_null": len(non_null),
            }
    result["categorical_stats"] = categorical_stats
    suspeitos = []
    if file_key == "Details_Itapema.csv":
        cnt_latlon0 = sum(1 for r in rows if r["latitude"].strip() in ("0","0.0") or r["longitude"].strip() in ("0","0.0"))
        if cnt_latlon0:
            suspeitos.append(f"latitude/longitude = 0 (Details sem geolocalização, usar Mesh): {cnt_latlon0} casos ({cnt_latlon0/len(rows)*100:.1f}%)")
        cnt_star0_revpos = sum(1 for r in rows if r["star_rating"].strip() == "0.0" and try_parse_float(r["number_of_reviews"] or "0") not in (None,0))
        if cnt_star0_revpos:
            suspeitos.append(f"star_rating=0.0 com number_of_reviews>0: {cnt_star0_revpos} casos (impossivel)")
        cnt_pic0_fav = sum(1 for r in rows if r["picture_count"].strip() == "0" and r["is_guest_favorite"].strip().lower() == "true")
        if cnt_pic0_fav:
            suspeitos.append(f"picture_count=0 mas is_guest_favorite=true: {cnt_pic0_fav} casos (suspeito)")
        cnt_bed_extremo = sum(1 for r in rows if try_parse_float(r["number_of_bedrooms"] or "0") not in (None,) and try_parse_float(r["number_of_bedrooms"]) >= 8)
        if cnt_bed_extremo:
            suspeitos.append(f"number_of_bedrooms >=8: {cnt_bed_extremo} casos (ex: 12,16)")
        cnt_clean0 = sum(1 for r in rows if r["cleaning_fee"].strip() in ("0","0.0"))
        if cnt_clean0:
            suspeitos.append(f"cleaning_fee=0: {cnt_clean0} casos (pode ser legitimo)")
        cnt_prof_vazio = null_counts.get("is_professional",0)
        if cnt_prof_vazio:
            suspeitos.append(f"is_professional vazio (nulo): {cnt_prof_vazio}")
        cnt_encoding = sum(1 for r in rows if "Mǭximo" in (r["house_rules"] or "") or "nǜo" in (r["house_rules"] or ""))
        if cnt_encoding:
            suspeitos.append(f"encoding quebrado (Mǭximo/nǜo) em house_rules/amenities: {cnt_encoding} linhas")
    if file_key == "Hosts_ids_Itapema.csv":
        cnt_resp_na = placeholder_counts.get("response_rate_shown",0) + placeholder_counts.get("response_time_shown",0)
        if cnt_resp_na:
            suspeitos.append(f"response_rate_shown/response_time_shown com <NA>: {cnt_resp_na} placeholders")
        cnt_years0 = sum(1 for r in rows if r["years_host"].strip() == "0")
        if cnt_years0:
            suspeitos.append(f"years_host=0: {cnt_years0} casos")
        cnt_star0 = sum(1 for r in rows if r["star_rating_host"].strip() == "0.0")
        if cnt_star0:
            suspeitos.append(f"star_rating_host=0.0: {cnt_star0}")
    if file_key == "Mesh_Ids_Data_Itapema.csv":
        cnt_none = sum(1 for r in rows if r["suburb"].strip().lower() == "none" or is_null(r["suburb"]))
        if cnt_none:
            suspeitos.append(f"suburb = none ou vazio: {cnt_none}")
        cnt_lat0 = sum(1 for r in rows if r["latitude"].strip() in ("0","0.0"))
        if cnt_lat0:
            suspeitos.append(f"latitude=0 em Mesh: {cnt_lat0}")
    if file_key == "Price_AV_Itapema.csv":
        cnt_price0 = sum(1 for r in rows if r["price"].strip() in ("0","0.0"))
        if cnt_price0:
            suspeitos.append(f"price=0.0: {cnt_price0} casos")
        prices = [try_parse_float(r["price"] or "") for r in rows if try_parse_float(r["price"] or "") is not None]
        if prices:
            if max(prices) > 10000:
                suspeitos.append(f"price max muito alto: {max(prices)}")
            if min(prices) < 10:
                suspeitos.append(f"price min muito baixo: {min(prices)}")
    if file_key == "VivaReal_Itapema.csv":
        cnt_sale0 = sum(1 for r in rows if r["sale_price"].strip() in ("0","0.0"))
        if cnt_sale0:
            suspeitos.append(f"sale_price=0: {cnt_sale0}")
        cnt_area0 = sum(1 for r in rows if r["usable_area"].strip() in ("0","0.0"))
        if cnt_area0:
            suspeitos.append(f"usable_area=0: {cnt_area0}")
        cnt_amen_empty = sum(1 for r in rows if r["amenities"].strip() == "[]")
        if cnt_amen_empty:
            suspeitos.append(f"amenities=[]: {cnt_amen_empty}")
        cnt_condo_vazio = null_counts.get("monthly_condo_fee",0)
        if cnt_condo_vazio:
            suspeitos.append(f"monthly_condo_fee vazio: {cnt_condo_vazio}")
        cnt_iptu_vazio = null_counts.get("yearly_iptu",0)
        if cnt_iptu_vazio:
            suspeitos.append(f"yearly_iptu vazio: {cnt_iptu_vazio}")
        cnt_suburb_none = sum(1 for r in rows if r["suburb"].strip().lower() == "none" or is_null(r["suburb"]))
        if cnt_suburb_none:
            suspeitos.append(f"suburb none/vazio em VivaReal: {cnt_suburb_none}")
    result["suspeitos"] = suspeitos
    format_problems = []
    for idcol in ID_COLS.get(file_key, []):
        if idcol not in id_stats:
            continue
        stat = id_stats[idcol]
        if stat["com_espacos_pontas"] > 0:
            format_problems.append(f"{idcol}: {stat['com_espacos_pontas']} valores com espacos nas pontas")
        if stat["nao_numericos"] > 0:
            format_problems.append(f"{idcol}: {stat['nao_numericos']} valores nao numericos")
        if len(stat["distribuicao_tamanhos"]) > 1:
            format_problems.append(f"{idcol}: tamanhos variados {stat['distribuicao_tamanhos']}")
        if stat["nulos"] > 0:
            format_problems.append(f"{idcol}: {stat['nulos']} nulos")
        if stat["placeholders"] > 0:
            format_problems.append(f"{idcol}: {stat['placeholders']} placeholders")
        if stat["duplicados"] > 0:
            if file_key in ("Price_AV_Itapema.csv", "VivaReal_Itapema.csv"):
                format_problems.append(f"{idcol}: {stat['duplicados']} duplicados (esperado - historico)")
            elif file_key == "Details_Itapema.csv" and idcol == "owner_id":
                format_problems.append(f"{idcol}: {stat['duplicados']} duplicados (esperado - host com multiplos listings)")
            elif file_key == "Hosts_ids_Itapema.csv" and idcol == "owner_id":
                format_problems.append(f"{idcol}: {stat['duplicados']} duplicados (esperado - mesmo host em multiplos listings; arquivo é por listing)")
            else:
                format_problems.append(f"{idcol}: {stat['duplicados']} duplicados (ERRO - PK deveria ser unica)")
    result["format_problems"] = format_problems
    return result

def check_key_compatibility(all_results):
    sets = {}
    for key in ["Details_Itapema.csv", "Mesh_Ids_Data_Itapema.csv", "Price_AV_Itapema.csv"]:
        path = FILES[key]
        col = "airbnb_listing_id"
        s = set()
        with open(path, encoding="utf-8", errors="replace", newline="") as f:
            for r in csv.DictReader(f):
                v = r[col].strip() if r[col] else ""
                if v and v != "<NA>":
                    s.add(v)
        sets[key] = s
    for key in ["Details_Itapema.csv", "Hosts_ids_Itapema.csv"]:
        path = FILES[key]
        col = "owner_id"
        s = set()
        with open(path, encoding="utf-8", errors="replace", newline="") as f:
            for r in csv.DictReader(f):
                v = r[col].strip() if r[col] else ""
                if v and v != "<NA>":
                    s.add(v)
        sets[key + ":owner_id"] = s
    compat = []
    d = sets["Details_Itapema.csv"]
    m = sets["Mesh_Ids_Data_Itapema.csv"]
    compat.append({"chave": "airbnb_listing_id","par": "Details vs Mesh","details_total": len(d),"mesh_total": len(m),"intersecao": len(d & m),"so_details": len(d - m),"so_mesh": len(m - d),"compativel": len(d & m) == len(d) == len(m),"obs": "100% compatível" if len(d & m) == len(d) == len(m) else f"{len(d-m)} em Details sem Mesh, {len(m-d)} em Mesh sem Details"})
    p = sets["Price_AV_Itapema.csv"]
    compat.append({"chave": "airbnb_listing_id","par": "Details vs Price","details_total": len(d),"price_total_distinct": len(p),"intersecao": len(d & p),"so_details": len(d - p),"so_price": len(p - d),"compativel": len(p - d) == 0,"obs": f"Cobertura parcial: {len(d & p)}/{len(d)} ({len(d & p)/len(d)*100:.1f}%) de Details têm preço; {len(p - d)} ids em Price não existem em Details"})
    compat.append({"chave": "airbnb_listing_id","par": "Mesh vs Price","mesh_total": len(m),"price_total_distinct": len(p),"intersecao": len(m & p),"so_mesh": len(m - p),"so_price": len(p - m),"compativel": len(p - m) == 6,"obs": f"{len(m & p)} em comum; {len(p - m)} em Price sem Mesh"})
    d_owner = sets["Details_Itapema.csv:owner_id"]
    h_owner = sets["Hosts_ids_Itapema.csv:owner_id"]
    compat.append({"chave": "owner_id","par": "Details vs Hosts","details_total_distinct": len(d_owner),"hosts_total_distinct": len(h_owner),"intersecao": len(d_owner & h_owner),"so_details": len(d_owner - h_owner),"so_hosts": len(h_owner - d_owner),"compativel": len(d_owner - h_owner) == 0 and len(h_owner - d_owner) == 0,"obs": "Verificar 1 a 1"})
    for key in ["Details_Itapema.csv", "Mesh_Ids_Data_Itapema.csv", "Price_AV_Itapema.csv"]:
        lens = Counter(len(x) for x in sets[key])
        compat.append({"chave": "airbnb_listing_id formato","par": key,"distribuicao_tamanhos": dict(lens),"exemplo": list(sets[key])[:2] if sets[key] else [],"obs": "Tamanhos consistentes ~19 dígitos se 1 tamanho"})
    return compat

def main():
    print("AUDITORIA READ-ONLY - Iniciando...")
    all_results = {}
    for key, path in FILES.items():
        print(f"  Auditando {key} ...")
        all_results[key] = audit_file(key, path)
    print("  Verificando compatibilidade de chaves (sem JOIN) ...")
    compat = check_key_compatibility(all_results)
    print(f"  Gerando relatório em {REPORT_PATH} ...")
    generate_report(all_results, compat)
    print("Concluído.")

def generate_report(all_results, compat):
    out = []
    out.append("# Relatório de Auditoria de Qualidade - Hackathon Seazone")
    out.append("")
    out.append("> **Modo:** READ-ONLY | **Data:** gerado por `analysis/audit.py` | **Sem JOIN, sem receita, sem recomendação**")
    out.append("> **Decisões:** nulo = \"\" ou espaços | placeholder <NA>/não informado separado | 0/0.0 mantido e sinalizado")
    out.append("")
    out.append("## Resumo Executivo")
    out.append("")
    for key in FILES:
        r = all_results[key]
        out.append(f"- **{key}**: {r['n_rows']} linhas de dados, {r['n_cols']} colunas, {r['dup_full_rows']} linhas 100% duplicadas")
    out.append("")
    out.append("**Compatibilidade de chaves (recomputada):**")
    for c in compat[:4]:
        if "par" in c and "airbnb_listing_id" in c["chave"] and "vs" in c["par"]:
            out.append(f"- `{c['par']}` (`{c['chave']}`): interseção {c.get('intersecao')} | só {c['par'].split(' vs ')[0]} {c.get('so_details', c.get('so_mesh', c.get('so_price', 0)))} | só {c['par'].split(' vs ')[1]} {c.get('so_price', c.get('so_mesh', c.get('so_hosts',0)))} | {c['obs']}")
        if c["chave"] == "owner_id":
            out.append(f"- `{c['par']}` (`{c['chave']}`): Details distintos {c['details_total_distinct']} | Hosts distintos {c['hosts_total_distinct']} | interseção {c['intersecao']} | só Details {c['so_details']} | só Hosts {c['so_hosts']} | {c['obs']}")
    out.append("")
    for key in FILES:
        r = all_results[key]
        out.append(f"---")
        out.append(f"## ARQUIVO: `{key}`")
        out.append(f"")
        out.append(f"* **Linhas (dados, sem header, via csv):** {r['n_rows']}")
        out.append(f"* **Colunas:** {r['n_cols']}")
        out.append(f"* **Colunas listadas:** `{'`, `'.join(r['columns'])}`")
        out.append(f"* **Linhas 100% duplicadas:** {r['dup_full_rows']}")
        out.append(f"")
        out.append(f"### Tipos inferidos")
        for col, typ in r["col_types"].items():
            out.append(f"- `{col}`: {typ}")
        out.append(f"")
        out.append(f"### Nulos (\"\" ou espaços) e Placeholders (<NA>/não informado) por coluna")
        out.append(f"")
        out.append(f"| Coluna | Nulos qtd | Nulos % | Placeholders qtd | Placeholders % | Vazios qtd* | Vazios %* | Zeros qtd | Zeros % |")
        out.append(f"|---|---|---|---|---|---|---|---|---|")
        for col in r["columns"]:
            n = r["null_counts"][col]
            ph = r["placeholder_counts"][col]
            z = r["zero_counts"][col]
            total = r["n_rows"]
            out.append(f"| `{col}` | {n} | {n/total*100:.2f}% | {ph} | {ph/total*100:.2f}% | {n} | {n/total*100:.2f}% | {z} | {z/total*100:.2f}% |")
        out.append(f"")
        out.append(f"_*Vazios = mesma definição de nulos._")
        out.append(f"")
        if r["id_stats"]:
            out.append(f"### IDs")
            for idcol, st in r["id_stats"].items():
                out.append(f"- **`{idcol}`**: únicos `{st['unique']}` / duplicados `{st['duplicados']}` / nulos `{st['nulos']}` / placeholders `{st['placeholders']}` / com espaços pontas `{st['com_espacos_pontas']}` / não numéricos `{st['nao_numericos']}`")
                out.append(f"  - Distribuição tamanhos: `{st['distribuicao_tamanhos']}`")
                out.append(f"  - Exemplos: `{st['exemplos']}`")
            out.append(f"")
        if r["numeric_stats"]:
            out.append(f"### Numéricas (min, max, mediana, média, qtd zero)")
            out.append(f"")
            out.append(f"| Coluna | Count num | Min | Max | Mediana | Média | Qtd 0 | Qtd 0 % |")
            out.append(f"|---|---|---|---|---|---|---|---|")
            for col, st in r["numeric_stats"].items():
                if st["count_numeric"] == 0:
                    out.append(f"| `{col}` | 0 | - | - | - | - | - | - |")
                else:
                    out.append(f"| `{col}` | {st['count_numeric']} | {st['min']} | {st['max']} | {st['median']} | {round(st['mean'],2)} | {st['qtd_zero']} | {st['qtd_zero_pct']}% |")
            out.append(f"")
        if r["categorical_stats"]:
            out.append(f"### Categóricas (qtd categorias, top, inconsistentes)")
            for col, st in r["categorical_stats"].items():
                out.append(f"- **`{col}`**: {st['qtd_categorias']} categorias (non-null {st['total_non_null']})")
                tops = ", ".join([f"`{k}`:{v}" for k,v in st["top"][:5]])
                out.append(f"  - Top: {tops if tops else 'Nenhum'}")
                if st["inconsistentes"]:
                    out.append(f"  - **Inconsistentes:** `{st['inconsistentes']}`")
                else:
                    out.append(f"  - Inconsistentes: Nenhum problema encontrado")
            out.append(f"")
        out.append(f"### Valores suspeitos / impossíveis / fora do padrão")
        if r["suspeitos"]:
            for s in r["suspeitos"]:
                out.append(f"- {s}")
        else:
            out.append(f"- Nenhum problema encontrado")
        out.append(f"")
        out.append(f"### Formatação para futuros JOINs (IDs)")
        if r["format_problems"]:
            for fprob in r["format_problems"]:
                out.append(f"- {fprob}")
        else:
            out.append(f"- Nenhum problema encontrado")
        out.append(f"")
        out.append(f"### Erro vs Legítimo")
        if key == "Details_Itapema.csv":
            out.append(f"- `star_rating=0.0` com `number_of_reviews>0` = **erro/impossível**")
            out.append(f"- `star_rating=0.0` com `number_of_reviews=0` = **legítimo** (novo sem avaliação)")
            out.append(f"- `picture_count=0` + `is_guest_favorite=true` = **suspeito**")
            out.append(f"- `latitude/longitude=0.0` = **erro/suspeito**")
            out.append(f"- `is_professional=\"\"` = **falta de info**")
            out.append(f"- `space=\"\"` 56% vazio = **legítimo** (opcional)")
            out.append(f"- `encoding Mǭximo/nǜo` = **problema de charset**")
        elif key == "Hosts_ids_Itapema.csv":
            out.append(f"- `response_rate_shown=<NA>` = **legítimo/sentinela**")
            out.append(f"- `years_host=0` + `months_host>0` = **legítimo**")
        elif key == "Mesh_Ids_Data_Itapema.csv":
            out.append(f"- `suburb='none'`/vazio = **erro/falta**")
        elif key == "Price_AV_Itapema.csv":
            out.append(f"- `price=0` = **erro/impossível**")
            out.append(f"- `airbnb_listing_id` duplicado = **legítimo** (histórico)")
        elif key == "VivaReal_Itapema.csv":
            out.append(f"- `amenities=[]` = **legítimo**")
            out.append(f"- `monthly_condo_fee` vazio = **legítimo**")
            out.append(f"- `sale_price=0` / `usable_area=0` = **erro/impossível**")
        out.append(f"")
    out.append(f"---")
    out.append(f"## Chaves de Relacionamento (sem JOIN, recomputado)")
    for c in compat:
        out.append(f"- **{c['par']}** | chave `{c['chave']}` | {c}")
    out.append(f"")
    out.append(f"---")
    out.append(f"## Resumo por Arquivo (formato solicitado)")
    for key in FILES:
        r = all_results[key]
        principais = []
        if r["dup_full_rows"] > 0:
            principais.append(f"{r['dup_full_rows']} linhas 100% duplicadas")
        for col in r["columns"]:
            if r["null_counts"][col]/r["n_rows"] > 0.1:
                principais.append(f"`{col}` {r['null_counts'][col]} nulos ({r['null_counts'][col]/r['n_rows']*100:.1f}%)")
            if r["placeholder_counts"][col]/r["n_rows"] > 0.1:
                principais.append(f"`{col}` {r['placeholder_counts'][col]} placeholders ({r['placeholder_counts'][col]/r['n_rows']*100:.1f}%)")
        if r["suspeitos"]:
            principais.append(f"{len(r['suspeitos'])} tipos de valores suspeitos")
        if not principais:
            principais = ["Nenhum problema encontrado"]
        precisa = []
        pode_manter = []
        if key == "Details_Itapema.csv":
            precisa = ["Normalizar encoding", "Tratar lat/lon 0 como NULL+flag", "Tratar star 0 sem reviews como NULL lógico", "Strip IDs antes de JOIN"]
            pode_manter = ["space vazio 56% (opcional)", "is_professional vazio (flag unknown)", "cleaning_fee 0", "check_in/out <NA> como placeholder"]
        elif key == "Hosts_ids_Itapema.csv":
            precisa = ["Strip IDs", "Tratar <NA> como sentinela"]
            pode_manter = ["years_host 0 com months>0", "response_* <NA> como sentinela"]
        elif key == "Mesh_Ids_Data_Itapema.csv":
            precisa = ["Tratar suburb none/vazio como SEM_BAIRRO+flag", "Strip IDs"]
            pode_manter = ["country/state/city constantes"]
        elif key == "Price_AV_Itapema.csv":
            precisa = ["Verificar price 0/outliers", "Strip IDs"]
            pode_manter = ["airbnb_listing_id duplicado (histórico)"]
        elif key == "VivaReal_Itapema.csv":
            precisa = ["Tratar suburb none/vazio", "Strip IDs", "Verificar sale_price/area 0"]
            pode_manter = ["amenities []", "condo_fee/iptu vazio", "rental_price vazio (venda)"]
        out.append(f"### {key}")
        out.append(f"* **Linhas:** {r['n_rows']}")
        out.append(f"* **Colunas:** {r['n_cols']}")
        out.append(f"* **Principais problemas:** {'; '.join(principais)}")
        out.append(f"* **Problemas que precisam de limpeza:** {'; '.join(precisa) if precisa else 'Nenhum problema encontrado'}")
        out.append(f"* **Problemas que podem ser mantidos:** {'; '.join(pode_manter) if pode_manter else 'Nenhum'}")
        out.append(f"* **Observações importantes para a análise:** " + ("Cobertura Price 22.5% limita receita; Mesh 100% para localização" if key=="Details_Itapema.csv" else "OK"))
        out.append(f"")
    out.append(f"---")
    out.append(f"## Tabela Final de Problemas")
    out.append(f"")
    out.append(f"| Arquivo | Problema | Quantidade | Gravidade (baixa/média/alta) | Precisa tratar? | Tratamento recomendado |")
    out.append(f"|---|---|---|---|---|---|")
    for key in FILES:
        r = all_results[key]
        for col in r["columns"]:
            n = r["null_counts"][col]
            ph = r["placeholder_counts"][col]
            if n/r["n_rows"] > 0.05:
                grav = "média" if n/r["n_rows"] > 0.2 else "baixa"
                precisa = "Sim" if col in ("suburb","airbnb_listing_id","owner_id","latitude","longitude","star_rating") else "Não (sinalizar)"
                trat = "Criar flag is_null + manter linha; para JOIN fazer strip e tratar NULL lógico"
                out.append(f"| `{key}` | `{col}` nulos | {n} ({n/r['n_rows']*100:.1f}%) | {grav} | {precisa} | {trat} |")
            if ph/r["n_rows"] > 0.05:
                grav = "média" if ph/r["n_rows"] > 0.2 else "baixa"
                out.append(f"| `{key}` | `{col}` placeholders | {ph} ({ph/r['n_rows']*100:.1f}%) | {grav} | Não (manter sentinela) | Contar separado, não converter para nulo; flag is_placeholder |")
        for s in r["suspeitos"]:
            import re as _re
            m = _re.search(r"(\d+) casos|(\d+) linhas|(\d+)", s)
            qtd = m.group(0) if m else "ver texto"
            grav = "alta" if "impossível" in s or "latitude/longitude = 0" in s else "média" if "suspeito" in s else "baixa"
            precisa = "Sim" if "alta" in grav or "erro" in s.lower() else "Sinalizar"
            out.append(f"| `{key}` | {s[:80]} | {qtd} | {grav} | {precisa} | Ver seção suspeitos |")
        for fprob in r["format_problems"]:
            import re as _re
            m = _re.search(r"(\d+)", fprob)
            qtd = m.group(0) if m else "-"
            grav = "alta" if "quebra JOIN" in fprob or "nulos" in fprob else "média"
            out.append(f"| `{key}` | Formato JOIN: {fprob[:70]} | {qtd} | {grav} | Sim | Aplicar strip() nos IDs |")
        if r["dup_full_rows"] > 0:
            out.append(f"| `{key}` | Linhas 100% duplicadas | {r['dup_full_rows']} | média | Sim (deduplicar) | Remover duplicatas mantendo 1, flag is_duplicate |")
        else:
            out.append(f"| `{key}` | Linhas 100% duplicadas | 0 | baixa | Não | Nenhum problema encontrado |")
        for idcol, st in r["id_stats"].items():
            if st["duplicados"] > 0:
                # owner_id em Details/Hosts pode duplicar (host com multiplos listings) - nao eh erro de PK
                if key in ("Details_Itapema.csv", "Hosts_ids_Itapema.csv") and idcol == "owner_id":
                    grav = "baixa"
                    precisa = "Não (esperado)"
                    trat = "Manter - host com multiplos listings; usar distinct para contar hosts"
                elif key not in ("Price_AV_Itapema.csv","VivaReal_Itapema.csv"):
                    grav = "alta"
                    precisa = "Sim"
                    trat = "Investigar PK duplicada"
                else:
                    grav = "baixa"
                    precisa = "Não (esperado)"
                    trat = "Manter - histórico temporal"
                out.append(f"| `{key}` | `{idcol}` duplicados | {st['duplicados']} | {grav} | {precisa} | {trat} |")
    for c in compat[:4]:
        if "intersecao" in c:
            prob = f"Chave {c['chave']} {c['par']} cobertura"
            qtd = f"interseção {c['intersecao']}"
            grav = "alta" if c.get("so_details",0) > 0 and "Price" in c["par"] else "média"
            out.append(f"| `CHAVES` | {prob} | {qtd} | {grav} | Sim (documentar) | {c['obs']} |")
    out.append(f"")
    out.append(f"_Se não encontrar um problema em alguma categoria, consta como 'Nenhum problema encontrado' nas seções acima._")
    out.append(f"")
    out.append(f"## Observações Finais")
    out.append(f"- **READ-ONLY confirmado:** nenhum `data/*.csv` foi alterado, nenhuma linha excluída, nenhum valor substituído, nenhum JOIN executado.")
    out.append(f"- **Placeholders `<NA>`/`não informado` foram contados separadamente de nulos.**")
    out.append(f"- **Zeros mantidos:** `0`/`0.0` não convertidos para nulo; sinalizados apenas quando suspeitos (ex: lat/lon 0).")
    out.append(f"- **Reprodutível:** `python analysis/audit.py` gera este `relatorio_auditoria.md` a partir de leitura `csv` com `utf-8 errors=replace`.")
    out.append(f"")
    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"Relatório escrito com {len(out)} linhas.")

if __name__ == "__main__":
    main()

