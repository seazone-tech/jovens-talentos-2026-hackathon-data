# 01 Pergunta 1 - Melhor Perfil de Imóvel

**Pergunta:** Qual o melhor perfil de imóvel para investir? (tipologia, quartos)

**Principais evidências:**
* `price_por_anuncio.csv` (1005) + `base_analitica_itapema.csv` (4441) - Base intermediária LEFT JOIN
* `relatorio_demanda.md` - Alta = `reviews≥15` (625, 2-3q 82,8% da alta)
* `relatorio_demanda_preco.md` - Alta 550 vs demais 600
* `relatorio_vivareal.md` - Compra 3q MP 1,88M (1704)
* `relatorio_cruzamento_compra_aluguel.md` + `cruzamento_perfil.csv` - 5 perfis lado a lado
* `relatorio_receita.md` - Receita 2q MP 99k, 3q MP 151k (60%)
* `relatorio_roi.md` + `roi_perfil.csv` - ROI 2q Centro 7,75% >2q MP 6,20%

**O que cada arquivo demonstra:**
* `price_por_anuncio.csv`: 1005 medianas por anúncio, P99 2250, R$29.000 mantido.
* `base_analitica_itapema.csv`: 4441 LEFT JOIN, 999 com preço, `suburb` do Mesh.
* `relatorio_demanda.md`: 2-3q domina alta demanda, Meia Praia 72%.
* `relatorio_roi.md`: Ranking ROI com custos (condo/IPTU/cleaning/comissão 15%).
