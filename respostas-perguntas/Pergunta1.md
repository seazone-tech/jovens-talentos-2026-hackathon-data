## Pergunta 1 — Melhor perfil de imóvel para investimento

## Recomendação

**Apartamento de 2 quartos em Meia Praia.**

Escolhi esse perfil por apresentar o melhor equilíbrio entre **capital necessário, retorno estimado, volume de oferta e robustez dos dados**.

### Principais indicadores

| Indicador | Resultado |
|---|---:|
| Preço de compra mediano | R$ 1.075.000 |
| Diária mediana observada | R$ 460 |
| Anúncios Airbnb | 723 |
| Anúncios com preço | 187 |
| Imóveis à venda | 244 |
| Receita bruta anual estimada* | R$ 99.360 |
| ROI estimado* | 6,20% |
| Payback estimado* | 16,1 anos |

\* Estimativas considerando o cenário-base de **60% de ocupação**.

## Comparação com os principais perfis

O apartamento de **2 quartos no Centro apresenta o maior ROI estimado (7,75%)**, porém possui uma amostra menor e menor volume de oferta.

Por isso, a recomendação não considera apenas o maior ROI. O **2 quartos em Meia Praia** apresenta uma combinação mais equilibrada entre retorno, capital investido e volume de mercado.

### Por que Meia Praia?

- **R$ 1,075 milhão** de preço mediano, abaixo do 2 quartos no Centro.
- **723 anúncios Airbnb**, proporcionando maior volume de oferta.
- **187 anúncios com preço**, permitindo estimar a diária com uma base razoável.
- **ROI estimado de 6,20%** no cenário-base.
- O ROI permanece positivo no cenário conservador de 40% de ocupação.

## Limitações

Os valores de ROI e receita são **estimativas**, não garantias de retorno.

A ocupação de 60%, comissão de 15% e permanência média de 5 noites são premissas utilizadas no modelo. Além disso, nem todos os imóveis possuem informações de preço, condomínio ou IPTU.

**Onde conferir / Evidências**

- **Preço de compra mediano R$ 1.075.000** e todos os 5 perfis (qtd, preço, área, condomínio, IPTU): `reports/01_pergunta1_perfil/cruzamento_perfil.csv` (linhas 2–6); também `reports/01_pergunta1_perfil/relatorio_roi.md:7–13`.
- **Diária mediana observada R$ 460** (2q Meia Praia) e demais perfis: `reports/01_pergunta1_perfil/relatorio_receita.md:21`; cálculo realizado em `analysis/analisar_receita.py`.
- **Anúncios Airbnb 723** e **187 com preço** (25,9%): `reports/01_pergunta1_perfil/cruzamento_perfil.csv:2`; `reports/01_pergunta1_perfil/relatorio_roi.md:9`.
- **Imóveis à venda 244** (VivaReal): `reports/01_pergunta1_perfil/cruzamento_perfil.csv:2`; dado origine em `data/VivaReal_Itapema.csv` (coluna `sale_price`).
- **Receita bruta anual estimada R$ 99.360**: cálculo `460 × 30 × 0,60 × 12` — detalhado em `analysis/analisar_receita.py`; premissa de ocupação 60% explicitada em `reports/01_pergunta1_perfil/relatorio_roi.md:29`.
- **ROI estimado 6,20%**: cálculo `receita/preço × 100` — tabelado em `reports/01_pergunta1_perfil/relatorio_roi.md:49` (cenário 60%); script gerador: `analysis/analisar_roi.py`.
- **Payback estimado 16,1 anos**: cálculo `preco_compra/lucro` — tabela completa em `reports/01_pergunta1_perfil/relatorio_roi.md:49`.
- **Premissa de ocupação 60% (18 dias/mês)**: `reports/01_pergunta1_perfil/relatorio_roi.md:29`; `reports/01_pergunta1_perfil/relatorio_receita.md:29`; `reports/01_pergunta1_perfil/relatorio_cruzamento_compra_aluguel.md`; não é dado observado, é hipótese.
- **Dado observado — Preço compra**: `data/VivaReal_Itapema.csv` — coluna `sale_price` median >0 por perfil (cobertura 100%).
- **Dado observado — Diária**: `data/Details_Itapema.csv` / `analysis/base_analitica_itapema.csv` — coluna `price_mediano` mediana por perfil onde `price_mediano.notna()` (cobertura 21–35% por perfil).
- **Script gerador de ROI**: `analysis/analisar_roi.py`.
- **Script gerador de receita/diária**: `analysis/analisar_receita.py`.