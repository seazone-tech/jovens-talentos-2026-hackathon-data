"""Visualização inicial dos dados do hackathon - apenas leitura e preview."""
import pandas as pd

# Caminhos relativos à raiz do projeto
ARQUIVOS = {
    "Details_Itapema": "data/Details_Itapema.csv",
    "Hosts_ids_Itapema": "data/Hosts_ids_Itapema.csv",
    "Mesh_Ids_Data_Itapema": "data/Mesh_Ids_Data_Itapema.csv",
    "Price_AV_Itapema": "data/Price_AV_Itapema.csv",
    "VivaReal_Itapema": "data/VivaReal_Itapema.csv",
}

for nome, caminho in ARQUIVOS.items():
    print("=" * 80)
    print(f"BASE: {nome}")
    print(f"Arquivo: {caminho}")
    print("=" * 80)

    try:
        df = pd.read_csv(caminho)
    except FileNotFoundError:
        print(f"ERRO: arquivo não encontrado -> {caminho}\n")
        continue
    except Exception as e:
        print(f"ERRO ao ler {caminho}: {e}\n")
        continue

    print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")
    print(f"Colunas: {list(df.columns)}")
    print("\nPrimeiras 10 linhas:")
    print(df.head(10).to_string())
    print("\n")
