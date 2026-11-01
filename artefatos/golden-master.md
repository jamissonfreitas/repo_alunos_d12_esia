# Golden master — `calcular_total`

O objetivo é preservar as saídas da implementação original antes da rodada 1. O arquivo de referência é `golden_master_original.json`; `golden_master.py` captura e compara resultados pela igualdade exata do valor retornado (sem tolerância numérica). A aprovação só demonstra preservação para estes casos; não demonstra conformidade com `caso/regras.md`.

## Estado da captura

A implementação em `caso/miniloja/calculo.py` não foi alterada nesta preparação. O checkout estava no branch `aula-2`, commit `2c2fc89c8c1d2f03423ed30d31f790b8601e6c2d`; `git diff -- caso/miniloja/calculo.py caso/miniloja/flags.py` não mostrou alterações. A sessão de preparação não tinha `python`, `py` nem `uv` disponível no `PATH`. Por isso, não foi possível executar o oráculo e gravar saídas reais neste ambiente; **não invente nem aprove uma captura vazia**. Execute a captura abaixo em Python 3.11+ antes da rodada 1 e preserve o JSON gerado. O script grava versão completa do Python, plataforma e SHA-256 do `calculo.py` junto das saídas.

## Entradas documentadas

Os itens correspondem aos três carrinhos de `caso/dados/carrinhos.json`; os casos 7 e 8 usam um item sintético de R$ 200,00 para verificar a fronteira. Cada caso define `MINILOJA_PROMO_NATAL` individualmente (`0` ou `1`), sem depender do valor herdado pelo processo.

| Nº | Entrada |
|---:|---|
| 1 | `C1_camisa_e_bola`, sem cupom, PE, flag `0` |
| 2 | `C1_camisa_e_bola`, `PROMO10`, SP, flag `0` |
| 3 | `C1_camisa_e_bola`, `VIP15`, RJ, flag `0` |
| 4 | `C2_chuteira` (R$ 250,00), sem cupom, PE, flag `0` |
| 5 | `C2_chuteira`, `FRETEGRATIS`, SP, flag `0` |
| 6 | `C3_varias_bolas`, cupom inválido `INVALIDO`, RJ, flag `0` |
| 7 | Item de R$ 200,00 exatos, sem cupom, PE, flag `0` |
| 8 | Item de R$ 200,00 exatos, `PROMO10`, MG (outra UF), flag `0` |
| 9 | `C1_camisa_e_bola`, `NATAL`, PE, flag desligada (`0`) |
| 10 | `C1_camisa_e_bola`, `NATAL`, PE, flag ligada (`1`) |
| 11 | `C3_varias_bolas`, sem cupom, MG (outra UF), flag `0` |
| 12 | Carrinho vazio, sem cupom, SP, flag `0` |

## Ambiente e reprodução

- Raiz de execução: raiz do repositório; o capturador acrescenta `caso/` ao caminho de importação.
- Runtime: Python 3.11 ou superior, sem dependências externas.
- Flag do processo pai recomendada: não definida. O capturador define `MINILOJA_PROMO_NATAL` antes de cada chamada, inclusive para os casos sem `NATAL`.
- A captura registra o commit-base e o hash do módulo original para identificar a origem.

No PowerShell, da raiz do repositório:

```powershell
$env:MINILOJA_PROMO_NATAL = '0'
python -B artefatos/golden_master.py --capture
python -B artefatos/golden_master.py --compare
```

A primeira linha de execução cria/sobrescreve `artefatos/golden_master_original.json`, imprime os 12 resultados e preserva entradas e saídas. Faça isso antes de qualquer edição da rodada 1. Depois de cada rodada, mantenha o JSON original e execute apenas `--compare`; código de saída `0` significa igualdade exata para todos os casos, `1` indica divergência. Para recapturar em outro ambiente, guarde a versão anterior antes de usar `--capture`.
