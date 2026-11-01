# Registro individual — AV1.5

**Lucas Costa Neves Macena — 24/10/2026.** PR fictício do bloco 5; execução própria em Python 3.13.14, patch aplicado em `.tmp-pr-bloco5-repro`. Nos passos abaixo, use esse diretório como raiz e `PYTHONPATH=caso`; `_repo` é substituído por `patch.object(handlers, "_repo")`.

| # | Achado (local, impacto, severidade) | Correção e teste que falha sem ela |
|---|---|---|
| 1 | `miniloja/exportacao.py:15,23`: `usuario_id` é ignorado; `_repo.todos()` inclui pedidos de terceiros, violando R4. **Bloqueia.** | Filtrar por `p["usuario_id"] == usuario_id`. Com pedidos `(id=1, usuário=1)` e `(id=2, usuário=2)`, chame `exportar_vendas(1,"v.csv")` e leia `exports/v.csv`: atual contém ambos; teste deve exigir somente id 1. |
| 2 | `testes_existentes/test_exportacao.py`: só verifica 200 e `linhas == 2`; passa apesar do vazamento do achado 1. **Bloqueia** (teste ineficaz; dependente do 1). | Substituir por teste com `tempfile.TemporaryDirectory()`, ler o CSV e afirmar que só há pedido do usuário 1; sem filtro, falha. |
| 3 | `exportacao.py:16,24–26`: `except Exception: pass` oculta falha de escrita e retorna 200; `makedirs` nem está no `try`. **Bloqueia.** | Com `_repo.todos.return_value=[]` e `patch("builtins.open", side_effect=OSError("disco cheio"))`, chame `exportar_vendas(1,"v.csv")`: atual retorna `(200, {"arquivo":"exports/v.csv","linhas":0})`. Tratar `OSError` com 500; teste deve exigir status diferente de 200. |
| 4 | `exportacao.py:17`: nome sem validação permite `../fora.csv` e caminho absoluto escreverem fora de `exports/`. **Bloqueia.** | Em diretório temporário, testar ambos nomes; atuais retornam 200 e criam arquivo fora de `exports/`. Rejeitar nomes não simples ou sem `.csv` com 400; teste exige 400 e ausência dos arquivos. |
| 5 | `caso/requirements.txt`: dependência desnecessária, contra o comentário “somente biblioteca padrão”. **Comenta** (bloqueia se mantida). | Código já importa `csv` padrão. `rg -n -i "csv-export-helper" caso` encontra só `caso/requirements.txt`; remover a linha e rodar a suíte sem instalar pacote. PyPI `GET https://pypi.org/pypi/csv-export-helper/json` respondeu `{"message":"Not Found"}` (24/10/2026); sem projeto, não há mantenedor identificável. |

| Alegação do PR | Veredito e evidência |
|---|---|
| “Todos os testes passam (27)” | Confirmada, mas enganosa: `python -B testes/test_miniloja.py --codigo caso --existentes` → 27 testes, OK; passa com R4 violada (achados 1–2). |
| “Sem mudanças de comportamento no código existente” | Parcial: handler novo; requirements muda de sem dependências para dependência externa. `--codigo caso` mantém 8 ok/3 falhas, como no material inicial. |
| “Código revisado e seguro” | Refutada: R4 (1), erro de escrita ocultado (3), path traversal (4). |

**Merge:** solicitar mudanças. Aprovar após corrigir 1, 3 e 4 com testes descritos, remover dependência e repetir a suíte. Quem aprova responde pelo código. **Limites:** conferi diff, R4, suíte e reproduções acima; sem análise estática nem testes sistemáticos de abuso; `_br`, concorrência e `get_pedido` pré-existente fora do escopo.

**IA:** Claude Code, Claude Sonnet 5.5; deleguei rascunho do parecer e template com patch, descrição e R4. Aproveitei estrutura dos achados/tabela; conferi patch e contrato, executei suíte e reproduções. Raciocínio e decisão são meus.

**Checklist:** [x] quatro achados; [x] alegações; [x] dependência; [x] decisão; [x] uma página.
