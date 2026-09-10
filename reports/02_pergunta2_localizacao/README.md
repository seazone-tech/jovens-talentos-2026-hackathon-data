# 02 Pergunta 2 - Melhor Localização em Receita

**Pergunta:** Qual a melhor localização em termos de receita?

**Principais evidências:**
* `relatorio_localizacao_receita.md` + `localizacao_receita.csv` (46 linhas, bairro e bairro×quartos)

**O que cada arquivo demonstra:**
* `relatorio_localizacao_receita.md`: **Meia Praia 129,6k (600, 2602) > Centro 126,7k (587, 548) +2,3% - empate técnico**, 3q MP (151k, 1451) mais robusto que 4q MP (232k, 60). Ranking filtrado `≥100 Airbnb & ≥30 com preço`.
* `localizacao_receita.csv`: `bairro` isolado e `bairro×quartos` com receita 40/60/80%, sem JOIN por imóvel.
