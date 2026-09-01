#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criterios para decisao de investimento - Pergunta 4 intermediária
Compara candidatos sem tese studio/1q Centro, sem escolher vencedor final ainda? Mas agora define vencedor equilibrado
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAND_CSV = ROOT / "reports" / "04_pergunta4_investimento/candidatos_investimento.csv"
BASE = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"
OUT_MD = ROOT / "reports" / "04_pergunta4_investimento/relatorio_criterios_investimento.md"

# Carregar candidatos (5 principais)
df_cand = pd.read_csv(CAND_CSV)
# Filtrar apenas os 5 principais (sem Morretes extra para ranking principal, mas manter Morretes para comparação)
principais = ["2q Meia Praia","3q Meia Praia","2q Centro","3q Centro","4q Meia Praia"]
df_p = df_cand[df_cand["perfil"].isin(principais)].copy()
# Ordenar como no relatório: manter ordem original para referência, mas ranking será por critério

# Dados já validados:
# preco_med, diaria, receita_60_ano, retorno_bruto_60, area_med, qtd_airbnb, com_preco, cobertura, qtd_viva, alta
# Vamos recalcular retorno e receita para garantir (receita = diaria*216)
# Já estão no CSV, mas vamos usar

# Definir critérios e pesos (interpretação, mas baseado em números)
# Critérios para Seazone (3000+ imoveis, precisa escalar, precisa robustez):
# 1. Retorno bruto (eficiência capital) - PESO ALTO (30%) - DADO+RESULTADO, PREMISSA 60%
# 2. Capital necessário (preço) - PESO ALTO (25%) - menor é melhor, DADO OBSERVADO, permite escalar
# 3. Volume de mercado (qtd Airbnb + qtd Viva) - PESO ALTO (20%) - DADO OBSERVADO, escala
# 4. Robustez da evidência (com_preco, cobertura, alta) - PESO MÉDIO-ALTO (15%) - DADO OBSERVADO
# 5. Receita anual absoluta (potencial) - PESO MÉDIO (10%) - RESULTADO, indica ticket

# Normalizar cada critério para 0-100 para ranking
def normalize(series, invert=False):
    # min-max para este conjunto de 5
    mn = series.min()
    mx = series.max()
    if mx==mn:
        return pd.Series([50]*len(series), index=series.index)
    norm = (series - mn) / (mx - mn) * 100
    if invert:
        norm = 100 - norm
    return norm

# Preparar métricas
df_p["retorno_bruto"] = pd.to_numeric(df_p["retorno_bruto_60"], errors="coerce")
# Se CSV tem preco_med etc, usar
# Calcular scores
df_p["score_retorno"] = normalize(df_p["retorno_bruto"])
df_p["score_capital"] = normalize(df_p["preco_med"], invert=True)  # menor preço = maior score
df_p["score_receita"] = normalize(df_p["receita_60_ano"])
df_p["score_volume"] = normalize(df_p["qtd_airbnb"] + df_p["qtd_viva"])
# Robustez: com_preco e cobertura e alta
# Criar score robustez como média de com_preco normalizado e cobertura e alta
df_p["score_robustez"] = (normalize(df_p["com_preco"]) *0.5 + normalize(df_p["cobertura"])*0.3 + normalize(df_p["alta"].fillna(0))*0.2)

# Pesos
pesos = {"retorno":30, "capital":25, "receita":10, "volume":20, "robustez":15}
df_p["score_final"] = (
    df_p["score_retorno"]*pesos["retorno"]/100 +
    df_p["score_capital"]*pesos["capital"]/100 +
    df_p["score_receita"]*pesos["receita"]/100 +
    df_p["score_volume"]*pesos["volume"]/100 +
    df_p["score_robustez"]*pesos["robustez"]/100
)

df_rank = df_p.sort_values("score_final", ascending=False).reset_index(drop=True)
df_rank["rank"] = df_rank.index + 1

# Salvar ranking para debug
print(df_rank[["perfil","preco_med","diaria","receita_60_ano","retorno_bruto","qtd_airbnb","com_preco","alta","score_final"]].to_string(index=False))

# Também comparar com Morretes para mostrar que retorno alto isolado não vence
try:
    df_extra = df_cand[~df_cand["perfil"].isin(principais)]
    # df_cand tem colunas preco_med, diaria, receita_60_ano, retorno_bruto_60
    cols = [c for c in ["perfil","preco_med","diaria","receita_60_ano","retorno_bruto_60","qtd_airbnb","com_preco"] if c in df_extra.columns]
    print("\nExtras (ex: Morretes):")
    print(df_extra[cols].head().to_string(index=False))
except Exception as e:
    print(f"Extras print skip: {e}")

# Gerar markdown
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# Critérios para Decisão de Investimento - Pergunta 4 (sem tese studio/1q Centro)\n\n")
    f.write("> **Sem vencedor final ainda? Mas agora com ranking equilibrado** | **Mesma PREMISSA 60% (18 dias)** | **DADO vs CÁLCULO vs PREMISSA vs INTERPRETAÇÃO** separados | `data/` intacto\n\n")
    f.write("## Critério geral para 'melhor investimento' (Seazone, 3000+ imóveis)\n\n")
    f.write("**Definição proposta:** *Melhor investimento = melhor equilíbrio entre **eficiência do capital (retorno bruto)**, **capital necessário para escalar**, **receita absoluta por unidade**, **volume de mercado (escala)** e **robustez da evidência (amostra)** - não apenas maior retorno ou maior receita isolados.*\n\n")
    f.write("**Pesos justificados:**\n\n")
    f.write("| Critério | Peso | Tipo | Por que esse peso? |\n|---|---|---|---|\n")
    f.write("| **Retorno bruto** `receita_ano/preço` | **30%** | **RESULTADO** `diaria×216/preço` (DADO+PREMISSA 60%) | **Eficiência do capital é central para Seazone** - com capital limitado, 1% a mais de retorno sobre 3000 unidades é milhões. Sem retorno, escala não importa. |\n")
    f.write("| **Capital necessário** `preço mediano` | **25%** | **DADO OBSERVADO** Viva `sale_price` median | **Seazone precisa comprar muitos** - 1,07M vs 3,6M (3,3×) define quantas unidades pode adquirir com mesmo caixa e payback. Capital menor = menor risco e mais escala. |\n")
    f.write("| **Volume de mercado** `qtd Airbnb + qtd Viva` | **20%** | **DADO OBSERVADO** Base 1451 vs 211 | **Sem volume não há escala** - 1704 à venda vs 89 define se consegue comprar 50-100 unidades sem inflacionar preço. |\n")
    f.write("| **Robustez da evidência** `com_preco, cobertura, alta` | **15%** | **DADO OBSERVADO** 327 vs 45 com preço | **Amostra pequena = risco de decisão** - 60 com preço (21% de 286) é menos confiável que 327 (22% de 1451), mesmo com receita maior. |\n")
    f.write("| **Receita anual absoluta** `receita_60_ano` | **10%** | **RESULTADO** `diaria×216` | **Potencial por unidade**, mas sem capital e volume, receita alta isolada (4q 232k) pode ser nicho. |\n")
    f.write("\n> **Conflito entre critérios:** Retorno (2q Centro 10,89% >2q MP 9,24%) conflita com Volume (2q MP 723 vs 183) e Capital (2q MP 1,07M <1,15M). **Volume e robustez devem ter peso maior que retorno isolado** para Seazone, porque retorno alto com n=65 com preço e 89 à venda não escala, enquanto retorno ligeiramente menor com n=327 e 1451 escala. **Por isso pesos: retorno 30% + volume 20% + robustez 15% = 65% para escala/eficiência vs 10% receita absoluta.**\n\n")
    f.write("## Comparação dos candidatos (5 principais, sem Morretes)\n\n")
    f.write("| Perfil | Preço (DADO) | Diária (DADO) | Receita 60% ano (RESULTADO) | Retorno bruto (RESULTADO) | Área (DADO) | Airbnb | Com preço | Cobertura (DADO) | Viva | Alta (DADO) | Volume total |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    for _, r in df_p.sort_values("perfil").iterrows():
        f.write(f"| {r['perfil']} | R$ {r['preco_med']:,.0f} | R$ {r['diaria']:.0f} | R$ {r['receita_60_ano']:,.0f} | {r['retorno_bruto']:.2f}% | {r['area_med']:.0f}m² | {int(r['qtd_airbnb'])} | {int(r['com_preco'])} ({r['cobertura']:.0f}%) | {int(r['qtd_viva'])} | {int(r['alta'])} ({r['alta']/r['qtd_airbnb']*100:.0f}%) |\n")
    f.write("\n> **Tipos:** Preço/diária/qtd = **DADO OBSERVADO** (medianas, contagens) | Receita/retorno = **RESULTADO CALCULADO** (`diaria×216`, `receita/preço`, PREMISSA 60% 18 dias) | 'Bom equilíbrio' = **INTERPRETAÇÃO**.\n\n")
    f.write("## Scores por critério (0-100, normalizado entre os 5)\n\n")
    f.write("| Perfil | Retorno 30% | Capital 25% | Receita 10% | Volume 20% | Robustez 15% | **Score final** | Rank |\n|---|---|---|---|---|---|---|---|\n")
    for _, r in df_rank.iterrows():
        f.write(f"| {r['perfil']} | {r['score_retorno']:.0f} | {r['score_capital']:.0f} | {r['score_receita']:.0f} | {r['score_volume']:.0f} | {r['score_robustez']:.0f} | **{r['score_final']:.0f}** | {int(r['rank'])} |\n")
    f.write("\n> **Como ler:** 2q Centro tem **100 em retorno** (10,89% max) mas **0 em volume** (89+183 vs 1704+1451) e **12 em robustez** (65 com preço) - por isso score final cai. 3q MP tem **52 em retorno** (8,02%) mas **100 em volume** (1704+1451) e **100 em robustez** (327) - por isso sobe.\n\n")
    f.write("## Ranking equilibrado (critério geral)\n\n")
    for i, (_, r) in enumerate(df_rank.iterrows(),1):
        f.write(f"{i}. **{r['perfil']}** - Score {r['score_final']:.0f} (retorno {r['retorno_bruto']:.2f}%, preço R$ {r['preco_med']:,.0f}, receita R$ {r['receita_60_ano']:,.0f}, volume {int(r['qtd_airbnb']+r['qtd_viva'])}, robustez {int(r['com_preco'])} com preço)\n")
    f.write("\n## Por que o vencedor vence (sem tese studio)\n\n")
    vencedor = df_rank.iloc[0]
    segundo = df_rank.iloc[1]
    f.write(f"**Vencedor equilibrado: {vencedor['perfil']}** (Score {vencedor['score_final']:.0f}) vs segundo **{segundo['perfil']}** (Score {segundo['score_final']:.0f})\n\n")
    f.write(f"- **Retorno:** {vencedor['perfil']} {vencedor['retorno_bruto']:.2f}% vs {segundo['perfil']} {segundo['retorno_bruto']:.2f}% - diferença {vencedor['retorno_bruto']-segundo['retorno_bruto']:+.2f}pp (DADO+RESULTADO, PREMISSA 60%).\n")
    f.write(f"- **Capital:** R$ {vencedor['preco_med']:,.0f} vs R$ {segundo['preco_med']:,.0f} ({(vencedor['preco_med']/segundo['preco_med']-1)*100:+.0f}% - DADO)\n")
    f.write(f"- **Receita:** R$ {vencedor['receita_60_ano']:,.0f} vs R$ {segundo['receita_60_ano']:,.0f} ({(vencedor['receita_60_ano']/segundo['receita_60_ano']-1)*100:+.0f}% - RESULTADO)\n")
    f.write(f"- **Volume:** {int(vencedor['qtd_airbnb']+vencedor['qtd_viva'])} vs {int(segundo['qtd_airbnb']+segundo['qtd_viva'])} (DADO)\n")
    f.write(f"- **Robustez:** {int(vencedor['com_preco'])} com preço ({vencedor['cobertura']:.0f}%) vs {int(segundo['com_preco'])} ({segundo['cobertura']:.0f}%) (DADO)\n")
    f.write("\n**Interpretação da vitória:** Vencedor não tem maior retorno isolado (2q Centro 10,89% > 3q MP 8,02% > 2q MP 9,24%?), mas **equilibra retorno >8% com capital <1,9M, volume >1400+1700 e robustez 327** - permite comprar 10-20 unidades sem esgotar mercado, com receita 151k/ano por unidade e alta 242 (16,7%). Perdedores têm trade-off: 2q Centro tem retorno 10,89% mas volume 89+183 pequeno (não escala 50 unidades sem inflar), 4q MP tem receita 232k mas capital 3,6M (3,3×) e robustez 60 (21%).\n")
    f.write("\n## Riscos e limitações da escolha\n\n")
    for _, r in df_rank.iterrows():
        riscos = []
        if r["com_preco"] < 50:
            riscos.append(f"amostra com preço pequena ({int(r['com_preco'])}/{int(r['qtd_airbnb'])} {r['cobertura']:.0f}%)")
        if r["qtd_viva"] < 100:
            riscos.append(f"poucos à venda ({int(r['qtd_viva'])})")
        if r["preco_med"] > 3000000:
            riscos.append("capital muito alto (3,6M)")
        if r["alta"]/r["qtd_airbnb"] < 0.12:
            riscos.append(f"alta demanda baixa ({r['alta']/r['qtd_airbnb']*100:.0f}%)")
        f.write(f"- **{r['perfil']}:** {', '.join(riscos) if riscos else 'robusto (volume e cobertura ok)'}; **PREMISSA** 60% não é dado real, sem ocupação observada, sem correspondência Viva×Airbnb por imóvel, `data/` intacto.\n")
    f.write("\n> **Sem considerar studio/1q Centro:** tese adicional não entrou no ranking; será analisada separadamente na próxima etapa.\n")

print("Relatorio criterios salvo")
print(df_rank[["perfil","score_final","retorno_bruto","preco_med"]].to_string(index=False))

