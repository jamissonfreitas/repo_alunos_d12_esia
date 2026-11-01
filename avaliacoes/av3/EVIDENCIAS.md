# Evidências de execução — AV3 B3

Execução pelo assistente em 01/11/2026, Python 3.13.14, na branch `av3-b3-reserva-estoque`, base `1a12ad2`. Saídas abaixo são excertos observados, não simulações. Executar da raiz do repositório.

| Comando | Antes da correção | Depois da correção |
| --- | --- | --- |
| `python -B -m unittest avaliacoes/av3/test_reserva_estoque.py -v` | `Ran 2 tests`; `FAILED (failures=3)` | `Ran 2 tests`; `OK` |
| `python -B testes/test_miniloja.py --codigo caso --existentes` | `Ran 26 tests`; `OK` | `Ran 26 tests`; `OK` |
| `python -B testes/test_miniloja.py --codigo caso` | `Ran 11 tests`; `FAILED (failures=3)` | `Ran 11 tests`; `FAILED (failures=3)` |
| `python -B artefatos/golden_master.py --compare` | `OK: 12` saídas iguais exatamente | `OK: 12` saídas iguais exatamente |
| `python -B avaliacoes/av2/golden.py --compare` | Não executado nesta fase | `IGUAL: 2882 casos, 268203 bytes (calculo.py)` |

SHA-256 observado no golden da AV2: `D3E172FA187BFC2770AE2E8A387CB1191C8B1D447CF339215D66725551727670`.

As falhas gerais antes e depois são as mesmas: v08 CPF com dígito errado (`201 != 422`), v09 CPF com dígitos iguais (`201 != 422`) e v10 lista de erros (`400 != 422`). Cada um desses comandos retorna 1; os comandos verdes retornam 0. A execução conjunta de vários comandos no shell não deve ser interpretada como aprovação de todos pelo código do último processo.

## Prova vermelha, antes de editar o caso

O teste novo já existia, mas `estoque.py` e `pedidos.py` ainda eram os da main. A asserção de igualdade completa dos saldos detectou:

```text
subtest intermediario: {'A': 3, 'B': 3} != {'A': 4, 'B': 3}
subtest ultimo:        {'A': 3, 'B': 2} != {'A': 4, 'B': 3}
subtest sku_repetido:  {'A': 2, 'B': 3} != {'A': 4, 'B': 3}
Ran 2 tests
FAILED (failures=3)
```

O cenário de falha no primeiro item e o fluxo aprovado já passavam. Após a correção, todos os cenários passaram, incluindo a comparação completa de reservas e a ausência de cobrança/pedido salvo nos cenários recusados. O teste substitui somente `handlers._service` por um serviço isolado, restaurado ao sair de `patch.object`; os colaboradores de negócio são reais.

Para repetir a fase vermelha sem tocar na branch da entrega, aplique somente o arquivo novo `test_reserva_estoque.py` a uma cópia da base `1a12ad2` e execute o mesmo comando de unittest. Não é necessário modificar `testes/` nem a referência golden.

## Revisão do diff

`python -B avaliacoes/av3/gerar_diff.py` verifica a lista permitida de mudanças rastreadas e novos arquivos; aceita separadamente os nove arquivos da AV2 fornecidos pelo estudante como insumos locais, sem incluí-los no patch. Exige `git diff --check` e gera `avaliacoes/av3/AV3-B3.patch`. Esse patch inclui código, teste de regressão e documentos novos da AV3. Não inclui a própria cópia do patch. Os arquivos da AV2 seguem não rastreados, preservados para tratamento em sua própria entrega.
