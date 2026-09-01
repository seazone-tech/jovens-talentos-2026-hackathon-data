"""Gera visualizacao HTML das 5 bases do hackathon - SOMENTE Interface, sem alterar CSVs."""
import pandas as pd
from pathlib import Path
import webbrowser
import html

# Resolve caminhos de forma que funcione rodando da raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT = BASE_DIR / "reports" / "06_visualizacoes/visualizacao_dados.html"

ARQUIVOS = [
    "Details_Itapema.csv",
    "Hosts_ids_Itapema.csv",
    "Mesh_Ids_Data_Itapema.csv",
    "Price_AV_Itapema.csv",
    "VivaReal_Itapema.csv",
]

# Fallback se executado de outro cwd mas estrutura existe
if not DATA_DIR.exists():
    DATA_DIR = Path("data")
    OUTPUT = Path("reports/06_visualizacoes/visualizacao_dados.html")

# Dicionario de traducao - SOMENTE interface, nao renomeia colunas nos CSVs
# Todas as colunas foram identificadas automaticamente lendo os 5 CSVs (67 colunas distintas)
TRADUCOES = {
    # Details_Itapema.csv - 35 colunas
    "airbnb_listing_id": "ID do anúncio (Airbnb)",
    "url": "Link do anúncio (URL Airbnb)",
    "ad_name": "Título do anúncio",
    "ad_description": "Descrição do anúncio",
    "space": "Descrição do espaço",  # significado a confirmar - tradução literal
    "house_rules": "Regras da casa",
    "amenities": "Comodidades / Itens oferecidos",
    "safety_features": "Itens de segurança",
    "number_of_bathrooms": "Número de banheiros",
    "number_of_bedrooms": "Número de quartos",
    "number_of_beds": "Número de camas",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "check_in": "Horário de check-in",
    "check_out": "Horário de check-out",
    "number_of_guests": "Capacidade máxima de hóspedes",
    "number_of_reviews": "Quantidade de avaliações",
    "cleaning_fee": "Taxa de limpeza (R$)",
    "owner_id": "ID do anfitrião",
    "aquisition_date": "Data de coleta dos dados",
    "star_rating": "Nota média do anúncio",
    "picture_count": "Quantidade de fotos",
    "min_nights": "Mínimo de noites exigido",
    "guest_satisfaction_overall": "Satisfação geral dos hóspedes",
    "listing_type": "Tipo de anúncio / imóvel",
    "can_instant_book": "Permite reserva instantânea?",
    "is_professional": "Anfitrião profissional?",
    "accuracy_rating": "Nota de precisão do anúncio",
    "checkin_rating": "Nota do check-in",
    "cleanliness_rating": "Nota de limpeza",
    "communication_rating": "Nota de comunicação",
    "location_rating": "Nota de localização",
    "value_rating": "Nota de custo-benefício",
    "is_new_listing": "É anúncio novo?",
    "is_guest_favorite": "É favorito dos hóspedes?",

    # Hosts_ids_Itapema.csv - 11 colunas (owner_id e aquisition_date já acima, mas mantidos)
    "owner": "Nome do anfitrião",
    "is_superhost": "É Superhost?",
    "number_of_reviews_host": "Total de avaliações do anfitrião",
    "is_verified": "É verificado?",
    "star_rating_host": "Nota média do anfitrião",
    "years_host": "Anos como anfitrião",
    "months_host": "Meses como anfitrião",
    "response_rate_shown": "Taxa de resposta exibida",
    "response_time_shown": "Tempo de resposta exibido",
    "host_snapshot_date": "Data de captura dos dados do anfitrião",

    # Mesh_Ids_Data_Itapema.csv - 8 colunas (airbnb_listing_id, latitude, longitude, aquisition_date já acima)
    "suburb": "Bairro",
    "country": "País",
    "state": "Estado",
    "city": "Cidade",

    # Price_AV_Itapema.csv - 4 colunas (airbnb_listing_id e aquisition_date já acima)
    "date": "Data da estadia (preço para este dia)",
    "price": "Preço da diária (R$)",

    # VivaReal_Itapema.csv - 22 colunas (state, city, suburb, aquisition_date, amenities já acima)
    "listing_id": "ID do anúncio (VivaReal)",
    "link_url": "Link do anúncio",
    "listing_title": "Título do anúncio",
    "business_types": "Tipo de negócio (ex: Venda)",  # significado a confirmar - tradução literal do campo
    "property_type": "Tipo de imóvel",
    "sale_price": "Preço de venda (R$)",
    "rental_price": "Preço de aluguel (R$)",
    "rental_period": "Período do aluguel",  # significado a confirmar - tradução literal
    "yearly_iptu": "IPTU anual (R$)",
    "monthly_condo_fee": "Taxa de condomínio mensal (R$)",
    "usable_area": "Área útil (m²)",
    "bathrooms": "Número de banheiros",
    "bedrooms": "Número de quartos",
    "parking_spaces": "Vagas de garagem",
    "advertiser_name": "Nome do anunciante / Imobiliária",
    "portal": "Portal de origem",
}


def gerar_tabela_html(df_preview, table_id):
    """Gera HTML da tabela com cabeçalho em duas linhas (original + tradução). Preserva ordem e valores."""
    cols = list(df_preview.columns)
    # Cabeçalho
    ths = []
    for col in cols:
        trad = TRADUCOES.get(col, col)  # fallback literal se não mapeado
        # Escapar para segurança
        col_esc = html.escape(str(col))
        trad_esc = html.escape(str(trad))
        ths.append(f'<th><div class="th-orig">{col_esc}</div><div class="th-trad">{trad_esc}</div></th>')
    thead = "<thead><tr>" + "".join(ths) + "</tr></thead>"

    # Corpo - primeiras 100 linhas, sem alterar valores
    rows_html = []
    for _, row in df_preview.iterrows():
        tds = []
        for col in cols:
            val = row[col]
            if pd.isna(val):
                txt = ""
            else:
                txt = str(val)
            # Escapar e limitar visualmente via CSS (não altera dado)
            tds.append(f"<td title=\"{html.escape(txt)}\">{html.escape(txt)}</td>")
        rows_html.append("<tr>" + "".join(tds) + "</tr>")
    tbody = "<tbody>" + "".join(rows_html) + "</tbody>"
    return f'<table id="{table_id}" class="dados">{thead}{tbody}</table>'


html_parts = []

html_parts.append("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visualizacao Dados - Itapema (com traducao)</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:Arial,Helvetica,sans-serif;background:#F4F7FC;color:#0E1B33;line-height:1.5;padding:24px}
  h1{font-size:28px;margin-bottom:6px;color:#00143D}
  .sub{color:#4A5A78;margin-bottom:18px;font-size:14px}
  .legenda{background:#EAF0FF;border-left:4px solid #0055FF;border-radius:6px;padding:12px 14px;margin-bottom:22px;font-size:13px;color:#0E1B33}
  .legenda b{color:#0055FF}
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
  .contador{font-size:13px;color:#4A5A78;margin-top:8px}
  .aviso{font-size:12px;color:#4A5A78;margin-top:6px}
</style>
</head>
<body>
<h1>Visualizacao dos Dados — Itapema (SC)</h1>
<p class="sub">5 bases &middot; 100 primeiras linhas de cada &middot; com filtro e rolagem &middot; cabeçalho duplo (original + tradução PT-BR)</p>
<div class="legenda"><b>Como ler as colunas:</b> primeira linha = nome <b>original</b> exatamente como no CSV &middot; segunda linha = tradução em português simples (somente interface, CSVs não foram alterados).</div>
""")

resumo_colunas = {}

for arquivo in ARQUIVOS:
    caminho = DATA_DIR / arquivo
    sec_id = arquivo.replace(".csv", "").replace(".", "_")
    table_id = f"tbl_{sec_id}"

    html_parts.append(f'<section id="{sec_id}">')
    html_parts.append(f"<h2>{arquivo}</h2>")

    try:
        df = pd.read_csv(caminho)
    except FileNotFoundError:
        html_parts.append(f'<p style="color:#C0362B">Arquivo nao encontrado: {caminho}</p></section>')
        continue
    except Exception as e:
        html_parts.append(f'<p style="color:#C0362B">Erro ao ler {arquivo}: {e}</p></section>')
        continue

    linhas, colunas = df.shape
    resumo_colunas[arquivo] = colunas
    preview = df.head(100)

    # Verificacao: todas as colunas tem traducao?
    faltantes = [c for c in df.columns if c not in TRADUCOES]

    html_parts.append(f'<div class="meta"><b>{linhas}</b> linhas &middot; <b>{colunas}</b> colunas</div>')
    html_parts.append(f'<div class="cols"><b>Colunas ({colunas}):</b> {", ".join(map(str, df.columns))}</div>')
    if faltantes:
        html_parts.append(f'<div style="font-size:12px;color:#C0362B;margin-bottom:8px">Aviso: sem traducao para: {", ".join(faltantes)}</div>')
    html_parts.append(f'<input class="filtro" type="text" placeholder="Pesquisar / filtrar nesta tabela..." onkeyup="filtrarTabela(\'{table_id}\', this.value)">')
    html_parts.append(f'<div class="tabela-wrapper">')
    html_parts.append(gerar_tabela_html(preview, table_id))
    html_parts.append('</div>')
    html_parts.append(f'<div class="contador">Mostrando {len(preview)} de {linhas} linhas &middot; {colunas} colunas traduzidas</div>')
    html_parts.append('<div class="aviso">Valores exibidos são exatamente os do CSV original, sem limpeza ou cálculo.</div>')
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
print("Resumo por arquivo:")
for arq, qtd in resumo_colunas.items():
    print(f" - {arq}: {qtd} colunas (todas traduzidas: {qtd == len([c for c in pd.read_csv(DATA_DIR/arq, nrows=0).columns if c in TRADUCOES])})")

# Abrir automaticamente no navegador padrao do Windows usando Python
try:
    webbrowser.open(OUTPUT.resolve().as_uri())
    print("Abrindo no navegador...")
except Exception as e:
    print(f"Nao foi possivel abrir automaticamente: {e}")
    print(f"Abra manualmente: {OUTPUT.resolve()}")

