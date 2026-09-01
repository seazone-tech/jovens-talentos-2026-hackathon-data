#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resumo de precos por anuncio - Price_AV_Itapema.csv
Modo: READ-ONLY em data/, sem receita/ROI, preco != receita
Uso: python analysis/resumir_precos.py  (a partir da raiz)
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "Price_AV_Itapema.csv"
OUT = ROOT / "reports" / "01_pergunta1_perfil/price_por_anuncio.csv"

def main():
    print(f"Carregando {DATA} ...")
    # Preservar airbnb_listing_id como string (tamanhos variados 6-19 digitos)
    df = pd.read_csv(DATA, encoding="utf-8", dtype={"airbnb_listing_id": str})
    print(f"  Linhas carregadas: {len(df)} | Colunas: {list(df.columns)}")
    # Converter datas sem alterar CSV original (em memoria)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["aquisition_date"] = pd.to_datetime(df["aquisition_date"], errors="coerce")
    # Ordenar por airbnb_listing_id + date + aquisition_date para primeiro/ultimo deterministico
    df_sorted = df.sort_values(["airbnb_listing_id", "date", "aquisition_date"]).reset_index(drop=True)

    # P99 sobre todas as 118839 observacoes de price (decisao confirmada)
    p99 = df["price"].quantile(0.99)
    print(f"P99 (sobre todas as observacoes de price): {p99:.2f}")

    # Agrupar por airbnb_listing_id
    grouped = df_sorted.groupby("airbnb_listing_id", sort=False)

    rows = []
    for listing_id, g in grouped:
        qtd_registros = len(g)
        qtd_datas_distintas = g["date"].nunique()
        price_min = g["price"].min()
        price_max = g["price"].max()
        price_medio = g["price"].mean()
        price_mediano = g["price"].median()
        # primeiro e ultimo por date (+ aquisition_date desempate ja ordenado)
        primeiro_preco = g.iloc[0]["price"]
        ultimo_preco = g.iloc[-1]["price"]
        # flag acima P99 (se price_max > p99)
        acima_p99 = price_max > p99
        rows.append({
            "airbnb_listing_id": listing_id,
            "qtd_registros": qtd_registros,
            "qtd_datas_distintas": qtd_datas_distintas,
            "price_min": price_min,
            "price_max": price_max,
            "price_medio": price_medio,
            "price_mediano": price_mediano,
            "primeiro_preco": primeiro_preco,
            "ultimo_preco": ultimo_preco,
            "acima_p99": acima_p99,
        })

    agg = pd.DataFrame(rows)
    # Garantir 1 linha por anuncio e ordenado por id
    agg = agg.sort_values("airbnb_listing_id").reset_index(drop=True)

    # Validacoes
    assert len(agg) == df["airbnb_listing_id"].nunique(), "Deve ter 1 linha por airbnb_listing_id"
    assert agg["qtd_registros"].sum() == len(df), "Soma qtd_registros deve bater com total de registros"

    # Salvar (nao altera data/)
    agg.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Tabela salva em {OUT} com {len(agg)} linhas (1 por anuncio)")

    # Verificacao de extremos R$ 29.000 (sem excluir)
    max_price = df["price"].max()
    min_price = df["price"].min()
    median_geral = df["price"].median()
    media_geral = df["price"].mean()
    qtd_acima_p99 = int((agg["price_max"] > p99).sum())
    anuncios_acima = agg.loc[agg["acima_p99"], "airbnb_listing_id"].tolist()

    print("\n--- TERMINAL OUTPUT ---")
    print(f"quantidade de anuncios resultantes: {len(agg)}")
    print(f"quantidade total de registros de preco utilizados: {len(df)}")
    print(f"mediana geral dos precos: {median_geral:.2f}")
    print(f"media geral dos precos: {media_geral:.2f}")
    print(f"minimo: {min_price:.2f}")
    print(f"maximo: {max_price:.2f}")
    print(f"P99: {p99:.2f}")
    print(f"quantidade de anuncios com preco acima do P99: {qtd_acima_p99}")
    if anuncios_acima:
        print(f"anuncios acima P99 (exemplos): {anuncios_acima[:10]}")
        # Detalhar os com 29000
        g29000 = df[df["price"] == 29000]
        if not g29000.empty:
            print(f"registros com price == 29000.0: {len(g29000)}")
            print(g29000[["airbnb_listing_id","date","price"]].head().to_string(index=False))
    print("\n10 primeiras linhas da tabela resultante:")
    print(agg.head(10).to_string(index=False))

    # Observacao interpretacao
    print("\nObservacao: resultado representa PRECOS observados no historico do Airbnb, e nao receita. Nenhuma multiplicacao por 365 ou taxa de ocupacao foi aplicada.")

if __name__ == "__main__":
    main()

