# Registro individual — AV1.2

**Limite: uma página, incluindo evidências essenciais.** Estudante: Lucas Macena — Data: 17/10/2026
Origem: `../../caso/miniloja/calculo.py` fictício; base deste registro: artefatos de revisão e execução do repositório.

**Golden master:** 12 entradas, capturador `../../artefatos/golden_master.py`, saídas em `../../artefatos/golden_master_original.json` (Python 3.13.14; SHA-256 original `8ec2555b…180e5`). Comparação exata por igualdade dos valores, sem tolerância: `python -B artefatos/golden_master.py --compare`. O relatório de rodada 2 registra `OK: 12` saídas iguais. Exemplos conferíveis no JSON: caso 7 = 223.55; caso 10 (`NATAL` ligado) = 122.75. O roteiro e o limite da captura estão em `../../artefatos/golden-master.md`.

| Medida | Rodada 1 (sem escopo) | Rodada 2 (com escopo) |
| --- | --- | --- |
| Linhas adicionadas/removidas | +28/−61 (`calculo.py`) | +22/−8 (`calculo.py`) |
| Arquivos alterados (e quais estavam fora do esperado) | 1 (`calculo.py`) | 1 (`calculo.py`); nenhum fora do escopo |
| Mudou comportamento? (golden master) | Igualdade dos 12 casos não executada; análise apontou risco em cupons/UFs não hashable e tabelas mutáveis | `--compare`: 12/12 iguais; sem diferença conhecida nesses casos. Reportado, sem correção, `> 200` vs. contrato `>= 200` |
| Tempo de revisão | 4 min | 4 min |

**Escopo da rodada 2 (antes da mudança):** objetivo: explicitar etapas de `calcular_total`; pode tocar só `calculo.py`; não pode tocar outros arquivos, assinatura ou comportamento; invariantes: saídas exatas, erros e ordem atuais; pronto quando diff, verificações e golden forem revisados; pare se plano ou divergência exigir mudança comportamental. **Revisão do plano:** cortei troca de condicionais por dicionários/tabelas e simplificações, pois poderiam alterar tratamento de valores não hashable, exceções e mutabilidade; mantive as condições originais nos helpers. A divergência `> 200`/`>= 200` foi reportada, sem correção.
**Algo que parecia bug e eu apenas reportei:** frete grátis usa `> 200`, enquanto R1.3 especifica `>= 200`; não corrigido para preservar comportamento nesta refatoração.
**`../../AGENTS.md` mínimo:** presente na raiz, 7 linhas; inclui comandos de testes, limites (não tocar testes/contrato), opção de diretório de código e convenção sobre divergência código/contrato.

**Evidência:** `../../artefatos/registro-refatoracao-calcular-total.md` (rodada 1: +28/−61; golden pendente) e `../../artefatos/registro-rodada2-diff-e-comparacao.md` (rodada 2: +22/−8; comparação 12/12). **Limite e condição para rever o escopo:** os 12 casos não cobrem entradas malformadas/não hashable nem provam conformidade com R1; ampliar em tarefa separada após decisão sobre o limite do frete e inclusão desses casos.

**Procedência/IA:** Claude Code; modelo: Claude Sonnet 5.5; tarefa: apoiar a análise e consolidação do registro; trecho aproveitado: dados dos relatórios de diff e golden master; minha verificação/intervenção: conferi os números, o JSON, o escopo e a declaração de comparação nos artefatos. Rodada 1: revisão por análise, sem comparação executada; rodada 2: o relatório registra execução do diff, testes e comparação.

**Revisão:** [x] golden master; [x] duas rodadas com números; [x] seis campos; [x] AGENTS.md; [x] até uma página.
