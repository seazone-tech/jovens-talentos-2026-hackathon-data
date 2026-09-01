# 00 Auditoria e Validação

**Pergunta/conclusão que sustenta:** Confiabilidade de toda a análise - antes de qualquer limpeza, JOIN ou cálculo.

**Principais evidências:**
* `relatorio_auditoria.md` - 12 checks nos 5 CSVs (nulos, IDs, duplicatas, suspeitos, formato JOIN)
* `auditoria_universo_imoveis.md` - Valida que **apartamento (83,5%)** é universo correto vs casa/outros (n<30 com preço)
* `auditoria_independente_p1_p4.md` + `auditoria_pergunta3.md` + `auditoria_criterios_investimento.md` - Auditorias independentes de P1-P4 (receita, correlação, pesos)

**O que cada arquivo demonstra (1 frase):**
* `relatorio_auditoria.md`: 696 linhas com tabela final por gravidade, sem erro matemático, `data/` intacto.
* `auditoria_universo_imoveis.md`: Apartamento domina 83,5% Airbnb e 90,4% Viva, único com `≥30` com preço por perfil.
