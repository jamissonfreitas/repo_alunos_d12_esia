# Escopo rodada 2
- Objetivo: reduzir aninhamento e duplicação em calcular_total sem mudar nenhum resultado.
- Pode tocar: só caso/miniloja/calculo.py.
- Não pode tocar: testes/, golden/, caso/regras.md, flags.py, golden_master.*, assinatura calcular_total(itens, cupom=None, uf="PE").
- Invariantes: ordem desconto → frete → taxa; `> 200` e `round()` como estão (divergem do R1, só reportar); laço explícito na soma (sem sum()/Decimal).
- Critério de pronto: `python golden_master.py comparar` dá 288/288 e git diff --stat mostra só calculo.py.
- Critério de parada: se qualquer entrada divergir ou for preciso tocar outro arquivo, parar e reportar.