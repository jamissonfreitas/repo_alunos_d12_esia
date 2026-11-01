# Rodada 2 — diff de `calcular_total` e comparação com o registro existente

Este arquivo é novo. `registro-refatoracao-calcular-total.md` (registro anterior) e `escopo-rodada2.md` não foram alterados.

## Diff desta rodada

- Arquivo alterado: somente `caso/miniloja/calculo.py` (`git diff --numstat`: 22 linhas adicionadas, 8 removidas; 74 → 88 linhas).
- Diff completo salvo em `artefatos/diff-rodada2-calculo.patch`.
- Helpers privados: `_somar_itens` (linha 8), `_aplicar_desconto` (18), `_calcular_frete` (43), `_calcular_taxa` (62); `calcular_total` (74) apenas coordena.
- Condições, literais, consulta à flag `NATAL`, limite `total > 200`, `pass` e assinatura pública foram movidos sem alteração. Os comentários de etapa foram trocados por nomes de função; os demais comentários foram mantidos.
- Não há dicionários nem constantes novas; `FRETE_POR_UF` e `TAXA_POR_UF` continuam como antes (sem uso).

## Verificação executada

- `python -B artefatos/golden_master.py --compare`: OK, 12 saídas exatamente iguais (SHA-256 do JSON confere com o `calculo.py` original antes da edição).
- `python -B testes/test_miniloja.py --codigo caso`: 8 passam, 3 falham (v08, v09, v10), igual ao material inicial.
- `--existentes`: 26 testes OK.

## Comparação com `registro-refatoracao-calcular-total.md`

| Aspecto | Registro existente | Esta rodada |
|---|---|---|
| Tamanho | 73 → 41 linhas (−32) | 74 → 88 linhas (+14) |
| Ramificações de cupom, frete e taxa | Trocadas por dicionários (`FATOR_DESCONTO`, `FRETE_POR_UF`, `TAXA_POR_UF`) | Mantidas literalmente dentro dos helpers |
| Helpers | `_subtotal`, `_aplicar_desconto`, `_calcular_frete` (taxa inline) | `_somar_itens`, `_aplicar_desconto`, `_calcular_frete`, `_calcular_taxa` |
| Comentários antigos | Removidos | Mantidos, exceto os de etapa |
| Risco de `TypeError` com cupom/UF não hashable | Sim, apontado no registro | Não: `==` continua ignorando valores não hashable |
| Tabelas mutáveis influenciando o resultado | Sim, apontado | Não |
| Golden master | Não executado (sem `python` no PATH); igualdade só por leitura | Executado: 12/12 iguais |

Conclusão: este diff evita as três mudanças comportamentais potenciais listadas no registro existente, ao custo de menor redução de código. O registro existente descreve outra versão do arquivo e não vale para o estado atual.

## Limites

- O golden master cobre 12 casos; entradas inválidas (cupom/UF não hashable, itens malformados) não são exercitadas, só preservadas por leitura do código.
- Divergências entre código e contrato (`caso/regras.md`) e as três falhas v08–v10 não foram tratadas nesta rodada.
- A validação da referência do golden master pelo estudante continua pendente de confirmação explícita.
## Os diffs mudaram igualmente nas duas rodadas?

Não. Os dois diffs são bem diferentes.

| | Registro existente | Esta rodada |
|---|---|---|
| Linhas | +28 / −61 | +22 / −8 |
| Tamanho do arquivo | 73 → 41 linhas | 74 → 88 linhas |
| Estrutura | Dicionários (`FATOR_DESCONTO`, `FRETE_POR_UF`, `TAXA_POR_UF`) no lugar dos `if/elif`; taxa calculada dentro de `calcular_total` | Os `if/elif` foram mantidos, só movidos para helpers, e a taxa ganhou o seu (`_calcular_taxa`) |
| Comentários | Antigos removidos | Mantidos, exceto os de etapa |
| Comportamento | Três mudanças possíveis, em entradas não hashable e tabelas mutáveis | Nenhuma conhecida |

**Limite da comparação:** foi feita só pelo texto do registro anterior. No início desta rodada, o `calculo.py` estava igual ao commit `2c2fc89` (o SHA-256 bate com o golden master), e a versão com dicionários não está mais no repositório. Os números do diff antigo não foram conferidos.
