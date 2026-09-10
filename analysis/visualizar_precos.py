"""Gera visualizacao HTML para price_por_anuncio.csv - SOMENTE Interface, sem alterar CSVs."""
import pandas as pd
from pathlib import Path
import webbrowser
import html
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CSV = BASE_DIR / "reports" / "01_pergunta1_perfil/price_por_anuncio.csv"
OUTPUT = BASE_DIR / "reports" / "06_visualizacoes/visualizacao_precos.html"

if not DATA_CSV.exists():
    DATA_CSV = Path("reports/01_pergunta1_perfil/price_por_anuncio.csv")
    OUTPUT = Path("reports/06_visualizacoes/visualizacao_precos.html")

TRADUCOES = {
    "airbnb_listing_id": "ID do anúncio (Airbnb)",
    "qtd_registros": "Qtd registros de preço",
    "qtd_datas_distintas": "Qtd datas distintas",
    "price_min": "Preço mínimo (R$)",
    "price_max": "Preço máximo (R$)",
    "price_medio": "Preço médio (R$)",
    "price_mediano": "Preço mediano (R$)",
    "primeiro_preco": "Primeiro preço (por date)",
    "ultimo_preco": "Último preço (por date)",
    "acima_p99": "Acima do P99? (flag)",
}

def gerar_tabela_html(df_preview, table_id):
    cols = list(df_preview.columns)
    ths = []
    for col in cols:
        trad = TRADUCOES.get(col, col)
        col_esc = html.escape(str(col))
        trad_esc = html.escape(str(trad))
        ths.append(f'<th><div class="th-orig">{col_esc}</div><div class="th-trad">{trad_esc}</div></th>')
    thead = "<thead><tr>" + "".join(ths) + "</tr></thead>"
    rows_html = []
    for _, row in df_preview.iterrows():
        # destacar linha se acima_p99 == True
        acima = str(row.get("acima_p99", "")).lower() == "true"
        tr_class = " class=\"destaque-p99\"" if acima else ""
        tds = []
        for col in cols:
            val = row[col]
            if pd.isna(val):
                txt = ""
            else:
                # formatar floats com 2 casas para legibilidade (sem alterar dado bruto no CSV)
                if isinstance(val, float):
                    txt = f"{val:.2f}"
                else:
                    txt = str(val)
                # bool traduzir
                if txt.lower() == "true":
                    txt = "Sim"
                elif txt.lower() == "false":
                    txt = "Não"
            tds.append(f"<td title=\"{html.escape(str(row[col]))}\">{html.escape(txt)}</td>")
        rows_html.append(f"<tr{tr_class}>" + "".join(tds) + "</tr>")
    tbody = "<tbody>" + "".join(rows_html) + "</tbody>"
    return f'<table id="{table_id}" class="dados">{thead}{tbody}</table>'

try:
    df = pd.read_csv(DATA_CSV, dtype={"airbnb_listing_id": str})
except FileNotFoundError:
    print(f"Arquivo não encontrado: {DATA_CSV}")
    raise SystemExit(1)

linhas, colunas = df.shape
# Estatísticas para legenda (preço != receita)
p99_info = ""
if "price_max" in df.columns:
    # P99 já calculado no resumir_precos.py = 2250, mas recalcular para exibir
    try:
        p99_val = df["price_max"].quantile(0.99)  # por anuncio, mas info geral é 2250 sobre observações
    except:
        p99_val = 2250
    qtd_acima = int((df["acima_p99"].astype(str).str.lower() == "true").sum()) if "acima_p99" in df.columns else 0
    p99_info = f"P99 (observações) = R$ 2.250,00 &middot; {qtd_acima} anúncios com price_max &gt; P99 &middot; R$ 29.000 mantido (31397917) sem exclusão"

preview = df.head(100)

html_parts = []
html_parts.append("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visualizacao Precos por Anuncio - Itapema</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:Arial,Helvetica,sans-serif;background:#F4F7FC;color:#0E1B33;line-height:1.5;padding:24px}
  h1{font-size:28px;margin-bottom:6px;color:#00143D}
  .sub{color:#4A5A78;margin-bottom:18px;font-size:14px}
  .legenda{background:#EAF0FF;border-left:4px solid #0055FF;border-radius:6px;padding:12px 14px;margin-bottom:22px;font-size:13px;color:#0E1B33}
  .legenda b{color:#0055FF}
  .alerta{background:#FFF0EF;border-left:4px solid #FC6058;border-radius:6px;padding:12px 14px;margin-bottom:22px;font-size:13px}
  .alerta b{color:#C0362B}
  section{background:#fff;border:1px solid #DCE3EF;border-radius:10px;padding:20px;margin-bottom:24px}
  section h2{font-size:18px;color:#0055FF;margin-bottom:8px}
  .meta{font-size:14px;color:#4A5A78;margin-bottom:12px}
  .meta b{color:#0E1B33}
  .cols{font-size:12px;background:#F4F7FC;border:1px solid #DCE3EF;border-radius:6px;padding:10px;margin-bottom:12px;word-break:break-all}
  .filtro{width:100%;padding:10px 12px;border:1px solid #DCE3EF;border-radius:6px;margin-bottom:12px;font-size:14px}
  .tabela-wrapper{overflow:auto;max-height:520px;max-width:100%;border:1px solid #DCE3EF;border-radius:6px}
  table{border-collapse:collapse;width:max-content;min-width:100%;font-size:13px}
  th{position:sticky;top:0;background:#00143D;color:#fff;text-align:left;padding:8px 10px;white-space:nowrap;z-index:1;vertical-align:bottom;border-right:1px solid #1A2E5A}
  th:last-child{border-right:none}
  .th-orig{font-weight:700;font-size:12px;line-height:1.2;white-space:nowrap}
  .th-trad{font-weight:400;font-size:11px;line-height:1.2;color:#A9BCDD;white-space:nowrap;margin-top:2px}
  td{padding:7px 10px;border-bottom:1px solid #E8EEF7;white-space:nowrap;max-width:420px;overflow:hidden;text-overflow:ellipsis;border-right:1px solid #EDF2FB}
  td:last-child{border-right:none}
  tr:nth-child(even) td{background:#FAFCFF}
  tr.destaque-p99 td{background:#FFF0EF !important; font-weight:600}
  tr.destaque-p99 td:last-child{color:#C0362B}
  .contador{font-size:13px;color:#4A5A78;margin-top:8px}
  .aviso{font-size:12px;color:#4A5A78;margin-top:6px}
</style>
</head>
<body>
<h1>Visualizacao Preços por Anúncio — Itapema (SC)</h1>
<p class="sub">price_por_anuncio.csv &middot; 1 linha por airbnb_listing_id &middot; 100 primeiras linhas &middot; cabeçalho duplo (original + tradução PT-BR) &middot; preço ≠ receita</p>
<div class="legenda"><b>Como ler as colunas:</b> primeira linha = nome <b>original</b> exatamente como no CSV &middot; segunda linha = tradução em português simples (somente interface, CSV não alterado). Ordenação original por airbnb_listing_id.</div>
""")
html_parts.append(f'<div class="alerta"><b>Atenção - Preço ≠ Receita:</b> valores são <b>preços observados</b> no histórico (min/médio/mediano), não receita. Nenhuma multiplicação por 365 ou taxa de ocupação. {p99_info}</div>')

html_parts.append(f'<section id="price_por_anuncio">')
html_parts.append(f"<h2>price_por_anuncio.csv</h2>")
html_parts.append(f'<div class="meta"><b>{linhas}</b> anúncios (1 linha por airbnb_listing_id) &middot; <b>{colunas}</b> colunas &middot; total registros originais 118.839</div>')
html_parts.append(f'<div class="cols"><b>Colunas ({colunas}):</b> {", ".join(map(str, df.columns))}</div>')
html_parts.append(f'<input class="filtro" type="text" placeholder="Pesquisar / filtrar nesta tabela (ex: 29000 ou True)..." onkeyup="filtrarTabela(\'tbl_price_por_anuncio\', this.value)">')
html_parts.append(f'<div class="tabela-wrapper">')
html_parts.append(gerar_tabela_html(preview, "tbl_price_por_anuncio"))
html_parts.append('</div>')
html_parts.append(f'<div class="contador">Mostrando {len(preview)} de {linhas} anúncios &middot; {colunas} colunas traduzidas &middot; destaque em vermelho = acima_p99 (price_max &gt; P99)</div>')
html_parts.append('<div class="aviso">Valores exibidos são exatamente os do CSV resumido, sem limpeza destrutiva. Primeiro/último preço por date (+ aquisition_date desempate). R$ 29.000 mantido.</div>')
html_parts.append('</section>')
html_parts.append("""
<script>
function filtrarTabela(tableId, termo){
  termo = termo.toLowerCase();
  var tabela = document.getElementById(tableId);
  if(!tabela) return;
  var tbody = tabela.getElementsByTagName("tbody")[0];
  if(!tbody) return;
  var linhas = tbody.getElementsByTagName("tr");
  for(var i=0;i<linhas.length;i++){
    var txt = linhas[i].textContent.toLowerCase();
    linhas[i].style.display = txt.indexOf(termo) > -1 ? "" : "none";
  }
}
</script>
</body>
</html>
""")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(html_parts), encoding="utf-8")
print(f"HTML gerado em: {OUTPUT.resolve()}")
print(f"Anúncios: {linhas} | Colunas: {colunas}")

try:
    webbrowser.open(OUTPUT.resolve().as_uri())
    print("Abrindo no navegador...")
except Exception as e:
    print(f"Nao foi possivel abrir automaticamente: {e}")
    print(f"Abra manualmente: {OUTPUT.resolve()}")

