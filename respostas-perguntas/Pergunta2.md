## Pergunta 2 — Qual a melhor localização em termos de receita?

**Meia Praia apresenta a maior receita anual estimada entre os bairros analisados**, com **R$ 129.600/ano**, contra **R$ 126.720/ano no Centro**, uma diferença de aproximadamente **2,3%**.

Apesar da diferença pequena, **Meia Praia apresenta uma vantagem importante em volume e robustez da amostra**, com **2.602 anúncios Airbnb**, sendo **607 com histórico de preço**, enquanto o Centro possui **548 anúncios**, sendo **193 com preço**.

Dentro de Meia Praia, o segmento de **3 quartos apresenta a melhor combinação entre receita e volume de dados**: diária mediana de **R$ 700** e receita anual estimada de **R$ 151.200**, considerando uma ocupação hipotética de 60%.

O segmento de 4 quartos apresenta receita estimada ainda maior (**R$ 232.200/ano**), porém possui apenas **60 imóveis com preço**, contra **327 nos imóveis de 3 quartos**, tornando a estimativa menos robusta.

> **Conclusão:** Meia Praia é a localização recomendada, mas a diferença para o Centro caracteriza um **empate técnico com leve vantagem para Meia Praia**. A escolha é reforçada principalmente pelo maior volume de imóveis e pela maior robustez da amostra.

**Observação:** as receitas são **estimativas**, calculadas a partir da diária mediana e de uma premissa de ocupação de 60% (18 dias/mês). Não representam receita efetivamente observada.

## Onde conferir / Evidências

- **Meia Praia R$ 129.600/ano e Centro R$ 126.720/ano**: cálculo `diária × 30 × 0,60 × 12` — tabelado em `reports/02_pergunta2_localizacao/relatorio_localizacao_receita.md:29–33`; ranking em `:29–33` (Meia Praia 1ª, Centro 2ª).
- **Diária Medina observada**: Meia Praia R$ 600, Centro R$ 587 — dados de `price_mediano` mediana por bairro/segmento em `reports/02_pergunta2_localizacao/relatorio_localizacao_receita.md:11,13`; origem `analysis/base_analitica_itapema.csv` (coluna `price_mediano`, 999/3710 com preço = 26,8% cobertura).
- **2.602 Airbnb em Meia Praia e 548 no Centro**: contagens `listing_type==apartamento & suburb_norm=='meia praia'` e `==centro` — `reports/02_pergunta2_localizacao/localizacao_receita.csv:1–2`; origem `data/Details_Itapema.csv` via LEFT JOIN para base analítica.
- **607 com preço em Meia Praia e 193 no Centro**: `com_preco` count por bairro — `reports/02_pergunta2_localizacao/localizacao_receita.csv:1–2`; cobertura 23,3% (MP) e 35,2% (Centro) sobre 3710 apto da base.
- **Segmento 3q Meia Praia R$ 151.200**: diária R$ 700, 1451 Airbnb, 327 com preço — detalhado em `reports/02_pergunta2_localizacao/relatorio_localizacao_receita.md:39–45` (linha 42).
- **Segmento 4q Meia Praia R$ 232.200**: apenas 60 com preço (21% de 286 Airbnb) — sinalizado como amostra pequena em `:33` e linha 93 do relatório.
- **Empate técnico 2,3%**: diferença de R$ 2.880/ano entre Meia Praia e Centro — `:81` do relatório.
- **Bairros <30 com preço excluídos**: Tabuleiro 99/17, Ilhota 22/5, Casa Branca 63/13, Andorinha — amostra insuficiente para vencer Meia Praia/Centro/Morretes — `:85` do relatório.
- **Script gerador**: `analysis/analisar_localizacao_receita.py` — gera o relatório `relatorio_localizacao_receita.md` e a tabela `localizacao_receita.csv`.
- **Premissa de ocupação 60% (18 dias/mês)**: `reports/02_pergunta2_localizacao/relatorio_localizacao_receita.md:25`; `:83`; `reports/01_pergunta1_perfil/relatorio_roi.md:29`; hipótese, não dado observado.
