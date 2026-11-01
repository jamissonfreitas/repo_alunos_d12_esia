# Registro individual — AV1.3

**Estudante:** Lucas Macena · **Data:** 17/10/2026 · **Modalidade:** execução própria, assistida por IA, em **cópia de trabalho** de `caso/` e `testes/` (nenhum arquivo do pacote foi alterado). Python 3.13.14 (referência do material: 3.12.3). Fontes: `caso/regras.md` (R1, R2), `caso/miniloja/`, `caso/testes_existentes/`.

Linha de base: `python -B testes/test_miniloja.py --codigo caso --existentes` → `Ran 26 tests ... OK`. Comando por teste: `python -B -m unittest testes_existentes.<módulo>.<Classe>.<teste>` (dentro de `caso/`).

| Teste suspeito | Tipo e sabotagem aplicada | Continuou verde? |
| --- | --- | --- |
| `test_cupom_desconhecido_e_ignorado` (`test_calculo.py`) | **Espelho**: compara a função com ela mesma. `return round(total, 2)` → `return 0.0` em `calcular_total`. | **Sim**: `OK`. Controle: `test_total_simples_pe` (valor fixo) com a mesma sabotagem → `FAILED (failures=1)`. |
| `test_criar_pedido` (`test_pedidos.py`) | **Afirma o mock**: `"total": total` → `"total": 0` em `pedidos.py`. | **Sim**: `OK`. |
| `test_formatar_moeda_nao_quebra` (`test_formatacao.py`) | **Sem asserção**: `return "R$ " + s` → `return "quebrado"` em `formatacao.py`. | **Sim**: `OK`. Controle: `test_formatar_moeda_milhar` → `FAILED (failures=1)`. |

Mutação (`python -B testes/mutacao_manual.py`, na cópia): `Mutantes: 31 | mortos: 23 | sobreviventes: 8 | escore: 74%`, os mesmos 8 de `apoio/resultado-textual.md`.

| Mutante sobrevivente | Por que sobreviveu; teste que o mata (rodado) |
| --- | --- |
| `descontos.py`: `"VIP15": 15` → `5` | A suíte só testa `PROMO10` em `aplicar_desconto`. Teste novo: `assertEqual(aplicar_desconto(200.0, "VIP15"), 170.0)`. Sem mutação: `OK`. Com o mutante (devolve 190.0): `FAILED (failures=1)`. Suíte existente com o mesmo mutante: `OK`. |
| `estoque.py`: `disponivel < qtd` → `<=` | Não há teste de reserva igual ao saldo. Teste novo: `Estoque({"A": 2}).reservar("A", 2, "p1")` é `True` e `saldo("A") == 0`. Sem mutação: `OK`. Com o mutante: `FAILED (errors=1)` (`EstoqueInsuficiente`). Suíte existente com o mesmo mutante: `OK`. |

**Equivalente:** `calculo.py`, `desconto_aplicado = True` → `False`. A variável só alimenta `if desconto_aplicado: pass`. Os dois testes novos continuam em `OK` com o mutante, e nenhum teste comportamental o distingue.

| Caso (entrada) | Esperado (R1/R2, à mão) | Observado (executado) | Decisão |
| --- | --- | --- | --- |
| 1 × R$ 200,00, PE, sem cupom | Subtotal 200 ≥ 200: frete grátis; 200 × 1,05 = **210,00** | `calcular_total(...)` = **223.55**: com `total > 200` cobra frete 12,90 e (200 + 12,90) × 1,05 = 223.545 | Erro no código (`>` deveria ser `>=`) |
| 1 × R$ 2,50, PE, `FRETEGRATIS` | 2,50 × 1,05 = 2,625 → meio para cima: **2,63** | `calcular_total(...)` = **2.62**; `2.5 * 1.05` = `2.625` e `round(2.625, 2)` = `2.62` | Erro no código (R1.5; `round` arredonda meio para par) |
| A (saldo 1, pede 1) + B (saldo 0, pede 1) | HTTP **409**; saldo de A volta a 1; nenhuma reserva | `post_pedidos` → `(409, {'erro': 'estoque insuficiente', 'sku': 'B'})`, mas `saldo("A") == 0` e `reservas == {('tmp-1', 'A'): 1}` | Erro no código (R2.2: reserva de A não é desfeita) |

**ADR:** Contexto: R1.3 exige frete grátis com subtotal ≥ 200, R1.5 exige meio para cima e R2.2 exige nenhuma reserva após 409; as três execuções acima divergem. Decisão: tratar as três como defeitos do código e manter os esperados do contrato. Consequências: corrigir limite, arredondamento e reversão das reservas; `test_cenarios_gravados` (`limite_200: 223.55`) é snapshot do defeito e deverá ser revisado. Alternativa descartada: ajustar os esperados ao código; rever se o contrato for alterado de forma explícita.

**Limite:** os 2 testes novos matam 2 dos 8 sobreviventes; restam NATAL 21%, frete RJ, e-mail obrigatório, `total_fmt` zero e formatação do relatório (não tratados), mais o equivalente. Os 31 mutantes são falhas pequenas e predefinidas, e as sabotagens valem para o teste isolado. Os 3 casos mostram os defeitos, mas ainda não há teste automatizado para eles nem correção aplicada. A mutação rodou na cópia com `MINILOJA_TEST_CMD="python -B testes/test_miniloja.py --existentes --codigo caso -x"`, pois `sys.executable` falhou no shell usado.

**Procedência/IA:** Claude Code (Claude Sonnet 5.5). Tarefa delegada: aplicar as sabotagens e os mutantes na cópia, propor e rodar os dois testes novos e executar os três casos; as saídas acima são dessas execuções. Revisão pelo estudante: [x] concluída.

**Revisão:** [x] três testes; [x] dois mutantes; [x] três casos do contrato; [x] ADR; [x] até uma página (conferir na impressão).
