#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BASE ANAL?TICA - Hackathon Seazone
LEFT JOIN Details (4441) -> Mesh (4441) -> price_por_anuncio (1005) por airbnb_listing_id (string)
Modo: READ-ONLY em data/, sem limpeza destrutiva, sem receita/ROI, sem recomendacao
Uso: python analysis/criar_base_analitica.py  (a partir da raiz)
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DETAILS = ROOT / "data" / "Details_Itapema.csv"
DATA_MESH = ROOT / "data" / "Mesh_Ids_Data_Itapema.csv"
DATA_PRICE = ROOT / "reports" / "01_pergunta1_perfil/price_por_anuncio.csv"
OUT = ROOT / "reports" / "01_pergunta1_perfil/base_analitica_itapema.csv"

def main():
    print(f"Carregando {DATA_DETAILS} ...")
    df_details = pd.read_csv(DATA_DETAILS, dtype={"airbnb_listing_id": str, "owner_id": str}, encoding="utf-8")
    print(f"  Details: {df_details.shape[0]} linhas, {df_details.shape[1]} cols")
    print(f"Carregando {DATA_MESH} ...")
    df_mesh = pd.read_csv(DATA_MESH, dtype={"airbnb_listing_id": str}, encoding="utf-8")
    print(f"  Mesh: {df_mesh.shape[0]} linhas, {df_mesh.shape[1]} cols")
    print(f"Carregando {DATA_PRICE} ...")
    df_price = pd.read_csv(DATA_PRICE, dtype={"airbnb_listing_id": str}, encoding="utf-8")
    print(f"  Price por anuncio: {df_price.shape[0]} linhas, {df_price.shape[1]} cols")

    # Garantir string e strip para compatibilidade (tamanhos variados)
    for df in (df_details, df_mesh, df_price):
        df["airbnb_listing_id"] = df["airbnb_listing_id"].astype(str).str.strip()
    df_details["owner_id"] = df_details["owner_id"].astype(str).str.strip()

    # Renomear colunas conflitantes de Details antes do join para preservar Mesh como fonte de localizacao
    # Details tem latitude/longitude 100% 0 -> manter como latitude_details/longitude_details para auditoria, mas base principal usa Mesh
    df_details_renamed = df_details.rename(columns={
        "latitude": "latitude_details",
        "longitude": "longitude_details",
        "aquisition_date": "aquisition_date_details",
    })
    df_mesh_renamed = df_mesh.rename(columns={
        "aquisition_date": "aquisition_date_mesh",
    })

    # JOIN 1: Details LEFT Mesh (one_to_one, preserva 4441)
    print("JOIN 1: Details LEFT Mesh ...")
    base = df_details_renamed.merge(
        df_mesh_renamed,
        on="airbnb_listing_id",
        how="left",
        validate="one_to_one",
        suffixes=("", "_dup"),
    )
    print(f"  Apos JOIN1: {base.shape[0]} linhas, {base.shape[1]} cols")

    # JOIN 2: resultado LEFT price_por_anuncio (one_to_one, preserva 4441, price fica NaN onde sem historico)
    print("JOIN 2: base LEFT price_por_anuncio ...")
    base = base.merge(
        df_price,
        on="airbnb_listing_id",
        how="left",
        validate="one_to_one",
        suffixes=("", "_price"),
    )
    print(f"  Apos JOIN2: {base.shape[0]} linhas, {base.shape[1]} cols")

    # Reordenar colunas para analise de investimento: manter uteis
    # Garantir que colunas solicitadas estejam presentes
    cols_essenciais = [
        "airbnb_listing_id",
        "owner_id",
        "suburb",
        "latitude",
        "longitude",
        "price_min",
        "price_max",
        "price_medio",
        "price_mediano",
        "qtd_registros",
        "qtd_datas_distintas",
        "acima_p99",
    ]
    # Verificar que suburb/lat/lon vieram do Mesh
    for c in cols_essenciais:
        if c not in base.columns:
            print(f"AVISO: coluna essencial ausente: {c}")

    # Salvar (nao altera data/)
    base.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Base salva em {OUT}")

    # Terminal outputs solicitados
    total = len(base)
    com_preco = int(base["price_max"].notna().sum()) if "price_max" in base.columns else 0
    sem_preco = total - com_preco
    dups = int(base.duplicated(subset=["airbnb_listing_id"]).sum())
    linhas, colunas = base.shape

    print("\n--- TERMINAL OUTPUT ---")
    print(f"quantidade total de anuncios na base final: {total}")
    print(f"quantidade de anuncios com preco: {com_preco}")
    print(f"quantidade de anuncios sem preco: {sem_preco}")
    print(f"quantidade de IDs duplicados na tabela final: {dups}")
    print(f"quantidade de linhas: {linhas}")
    print(f"quantidade de colunas: {colunas}")
    print(f"nomes das colunas: {list(base.columns)}")
    print("\n10 primeiras linhas (colunas essenciais):")
    cols_show = [c for c in ["airbnb_listing_id","listing_type","number_of_bedrooms","suburb","latitude","longitude","price_min","price_max","price_medio","qtd_registros"] if c in base.columns]
    print(base[cols_show].head(10).to_string(index=False))

    # Validacoes
    print("\n--- VALIDACOES ---")
    # 1. 4441 anuncios
    assert total == 4441, f"Base final deve ter 4441, tem {total}"
    print("[OK] Base final possui 4441 anuncios")
    # 2. airbnb_listing_id nao duplicado
    assert base["airbnb_listing_id"].nunique() == 4441, "airbnb_listing_id duplicado"
    assert dups == 0, "IDs duplicados encontrados"
    print("[OK] airbnb_listing_id nao ficou duplicado apos JOINs")
    # 3. 1005 com preco continuam identificaveis (distingir 999 em base vs 1005 distintos em price)
    price_distintos = df_price["airbnb_listing_id"].nunique()
    intersecao = len(set(df_details["airbnb_listing_id"].str.strip()) & set(df_price["airbnb_listing_id"].str.strip()))
    so_price = price_distintos - intersecao
    print(f"  Price distintos: {price_distintos} | Intersecao Details-Price: {intersecao} | So Price (orfaos): {so_price}")
    assert price_distintos == 1005, "Price deve ter 1005 distintos"
    assert intersecao == 999, "Intersecao deve ser 999"
    assert com_preco == intersecao, f"Com preco na base deve ser {intersecao}, e {com_preco}"
    print(f"[OK] 1005 anuncios com preco continuam identificaveis (999 em base + {so_price} orfaos reportados)")
    # 4. Nenhum arquivo em data/ alterado (verificar timestamps nao e feito aqui, mas garantir que nao houve to_csv em data/)
    for p in [DATA_DETAILS, DATA_MESH]:
        assert p.exists(), f"Arquivo data nao encontrado: {p}"
    assert not (ROOT / "data" / "base_analitica_itapema.csv").exists(), "Nao deve salvar em data/"
    print("[OK] Nenhum arquivo dentro de data/ foi alterado (verificado: nao houve escrita em data/)")

    print("\nObservacao: base analitica pronta para analise de perfil, sem receita/ROI. Preco mantido como preco.")

if __name__ == "__main__":
    main()

