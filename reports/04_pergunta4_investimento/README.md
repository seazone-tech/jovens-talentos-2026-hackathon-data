# 04 Pergunta 4 - Decisão de Investimento

**Pergunta:** O que você compraria e por quê? (estimativa de retorno, sem tese compactos)

**Principais evidências:**
* `relatorio_candidatos_investimento.md` + `candidatos_investimento.csv` (7 perfis) - Compara 2q/3q/4q MP +2q/3q Centro + Morretes por preço/diária/receita/retorno bruto (sem custos)
* `relatorio_criterios_investimento.md` - Define pesos 30/25/20/15/10 (retorno 30, capital 25, volume 20, robustez 15, receita 10) - **arbitrários**, vencedor muda com pesos (3q MP 62 vs 2q Centro 61 com 30/25 vs 75 com 40/35)

**O que cada arquivo demonstra:**
* `relatorio_candidatos_investimento.md`: 2q Centro 10,89% retorno bruto (maior entre os 5) vs 2q MP 9,24% vs 3q MP 8,02%; 2q Morretes 13,62% é extra com retorno maior mas fora do eixo.
* `relatorio_criterios_investimento.md`: Ranking ponderado é sensível a pesos - 3q MP vence com 30/25, 2q Centro vence com 40/35, empate técnico (1,08 ponto).
