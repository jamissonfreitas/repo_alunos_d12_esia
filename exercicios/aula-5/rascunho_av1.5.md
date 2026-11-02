mp# Rascunho — AV1.5 (revisão do PR "exportação de vendas em CSV")

> Rascunho preparado com assistência de IA. Conferir e reescrever com suas palavras antes de entregar; o registro final deve ter até uma página (o apêndice não conta).

# Registro individual — AV1.5

**Limite: uma página, incluindo evidências essenciais.** Estudante: Rafael — Data: 01/11/2026
Origem: pull request fictício liberado no bloco; modalidade: **execução própria** (patch aplicado em branch local `av1.5-revisao`, suíte rodada, cinco testes de revisão escritos e executados).

| # | Onde (arquivo) | Problema e impacto | Severidade | Correção e teste que falharia sem ela |
| --- | --- | --- | --- | --- |
| 1 | `miniloja/exportacao.py`, `exportar_vendas` | Ignora `usuario_id` e exporta `handlers._repo.todos()`. Qualquer usuário baixa as vendas de todos: viola **R4** (só os próprios pedidos). | **Bloqueia** | Filtrar pedidos por `usuario_id`. Teste `test_r4_so_pedidos_do_proprio_usuario`: com pedidos dos usuários 1 e 2, exportar como 1 deve dar `linhas == 1`. Resultado sem a correção: `2 != 1`. |
| 2 | `miniloja/exportacao.py`, `os.path.join(EXPORT_DIR, nome_arquivo)` | `nome_arquivo` vem do cliente sem validação (path traversal). `../fora.csv` ou caminho absoluto grava fora de `exports/`. | **Bloqueia** | Aceitar só nome simples (sem separadores/`..`), senão 400; ou gerar o nome no servidor. Teste `test_nome_com_path_traversal_e_recusado`: `get_exportacao(1, "../fora.csv")` deve dar 400 e não criar o arquivo. Sem a correção: `200 != 400`. |
| 3 | `caso/requirements.txt` | Adiciona `csv-export-helper==0.4.2`, que o código não usa (só `import csv`), e contradiz a declaração "sem dependências externas". Pacote inexistente no PyPI, 404 (ver abaixo): risco de supply chain / slopsquatting. | **Bloqueia** | Remover a linha. Teste `test_sem_dependencia_externa`: `requirements.txt` não pode ter linha de dependência. Sem a correção: falha. |
| 4 | `miniloja/exportacao.py`, `try/except Exception: pass` | Engole qualquer erro de gravação e ainda devolve `200` com `arquivo` e `linhas`, para um arquivo que pode não existir. Falha silenciosa. | **Bloqueia** | Remover o `except` mudo; devolver 500 com erro claro. Teste `test_falha_de_gravacao_nao_retorna_200` (um diretório ocupa o lugar do arquivo): status deve ser >= 500. Sem a correção: `200`. |
| 5 | `caso/testes_existentes/test_exportacao.py` | Teste fraco: usa mock do repositório, só confere status e contagem (a contagem errada, 2, é o próprio bug do achado 1). Não lê o arquivo nem cobre R4 ou nome malicioso. Rodar a suíte cria `exports/` real no repositório. Mutações mostram que ele quase não detecta defeitos (ver apêndice B). | Comenta | Testar com repositório real e diretório temporário; ler o CSV gerado; chamar `get_exportacao`. |
| 6 | `exportacao.py` e `handlers.py` | Acessa `handlers._repo` (privado) e importa dentro da função para evitar import circular. Acoplamento frágil. | Comenta | Injetar o repositório em `exportar_vendas`. |
| 7 | `exportacao.py`, `_br` | Total como `"R$ 10,00"` torna o CSV ruim para leitura por máquina (vírgula decimal, prefixo). | Comenta | Gravar número puro. Teste `test_csv_legivel_por_maquina`: `"R$"` não deve aparecer. Sem a correção: falha. |

| Alegação da descrição do PR | Confirmada ou refutada? | Evidência |
| --- | --- | --- |
| "Todos os testes passam" (27) | **Confirmada**, mas pouco significativa | `python -B testes/test_miniloja.py --codigo caso --existentes` -> `Ran 27 tests ... OK`. Os testes passam porque o novo teste valida o comportamento errado (achado 5). |
| "Sem mudanças de comportamento no código existente" | **Parcialmente confirmada** | As onze verificações do caso seguem iguais ao material inicial (`--codigo caso`: 11 testes, 3 falhas, que são tarefas do bloco 1). Mas a função nova é um comportamento novo e vaza dados (achado 1). |
| `csv-export-helper` "para formatar o CSV" | **Refutada** | `grep` por `csv_export`/`csv-export` em `caso/**/*.py`: nenhuma ocorrência. Só se usa o módulo `csv` da biblioteca padrão. |
| "Código revisado e seguro" | **Refutada** | Achados 1, 2 e 4, com testes que falham (cinco testes de revisão: 5 falhas). |

**Dependência nova (nome, existe?, quem mantém?, necessária?):** `csv-export-helper==0.4.2`. `https://pypi.org/pypi/csv-export-helper/json` -> **404 Not Found**, confirmado por `pip index versions csv-export-helper` -> `ERROR: No matching distribution found`. Não existe no PyPI, então não há mantenedor verificável. Fixar `==0.4.2` não protege: se alguém registrar o nome, o `pip install` rodaria código arbitrário, sem hash nem lockfile. Não é necessária: o `csv` da biblioteca padrão já faz o trabalho.

**Decisão sobre o merge e condição para aprovar:** **Não aprovar (rejeitar).** Aprovo apenas depois de: (a) filtrar por `usuario_id` (R4), (b) validar `nome_arquivo`, (c) remover a dependência, (d) propagar erros, (e) com os testes dos achados 1 a 4 incluídos e passando, e a suíte atual verde. Quem aprova assume a responsabilidade pelo que entra; a descrição do PR não é evidência. **Limite da revisão:** sem análise estática (por exemplo, bandit) nem testes de abuso além dos cinco escritos; não testei concorrência, arquivos grandes, injeção de fórmula em CSV (`=...`), nem caminhos absolutos no Windows; a inexistência do pacote vale para o PyPI público (não consultei outros índices).

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, `claude-sonnet-5-5`; tarefa delegada e contexto: aplicar o patch, rodar a suíte, escrever os cinco testes de revisão e redigir este rascunho, a partir do `README` da aula, do `regras.md` (R4) e do PR; trecho aproveitado: achados, testes e tabelas deste rascunho; minha verificação/intervenção: ___ (preencher: o que você rodou e conferiu por conta própria). Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] quatro achados; [x] alegações conferidas; [x] dependência checada; [x] decisão; [ ] até uma página (cortar/condensar ao finalizar).

---

## Apêndice A — como reproduzir

```
git checkout -b av1.5-revisao
git apply apoio/pr-bloco5/0001-Adiciona-exporta-o-de-vendas-em-CSV.patch
python -B testes/test_miniloja.py --codigo caso --existentes     # 27 OK
python -B testes/test_miniloja.py --codigo caso                  # 11 testes, 3 falhas (base)
python -B <caminho>/test_revisao_pr.py                           # rodar na raiz: 5 falhas
pip index versions csv-export-helper                             # sem distribuição
# PyPI: https://pypi.org/pypi/csv-export-helper/json -> 404
```

`test_revisao_pr.py` (fora de `testes/`, que não pode ser alterado):

```python
import os, sys, tempfile, unittest
sys.path.insert(0, "caso")
from miniloja import handlers, exportacao
from miniloja.repositorio import RepositorioPedidos


class TestRevisao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        exportacao.EXPORT_DIR = os.path.join(self.tmp, "exports")
        handlers._repo = RepositorioPedidos()
        handlers._repo.salvar({"id": 1, "usuario_id": 1, "total": 10.0})
        handlers._repo.salvar({"id": 2, "usuario_id": 2, "total": 20.0})

    def test_r4_so_pedidos_do_proprio_usuario(self):
        status, corpo = handlers.get_exportacao(1, "a.csv")
        self.assertEqual(corpo["linhas"], 1)

    def test_nome_com_path_traversal_e_recusado(self):
        status, _ = handlers.get_exportacao(1, "../fora.csv")
        self.assertEqual(status, 400)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "fora.csv")))

    def test_falha_de_gravacao_nao_retorna_200(self):
        open(exportacao.EXPORT_DIR, "w").close() if False else None
        os.makedirs(exportacao.EXPORT_DIR)
        os.makedirs(os.path.join(exportacao.EXPORT_DIR, "x.csv"))  # diretório no lugar do arquivo
        status, _ = handlers.get_exportacao(1, "x.csv")
        self.assertGreaterEqual(status, 500)

    def test_sem_dependencia_externa(self):
        linhas = [l.strip() for l in open("caso/requirements.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
        self.assertEqual(linhas, [])

    def test_csv_legivel_por_maquina(self):
        handlers.get_exportacao(1, "b.csv")
        txt = open(os.path.join(exportacao.EXPORT_DIR, "b.csv"), encoding="utf-8").read()
        self.assertNotIn("R$", txt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

## Apêndice B — perguntas de revisão

**Entrada do usuário chega a comando, caminho ou consulta sem validação?** Sim, a um **caminho de arquivo**: `get_exportacao(usuario_id, arquivo)` repassa `arquivo` para `os.path.join(EXPORT_DIR, nome_arquivo)` e `open(caminho, "w")`, sem rejeitar `..`, separadores ou caminho absoluto (que faz o `join` descartar `EXPORT_DIR`). É o achado 2; o teste `test_nome_com_path_traversal_e_recusado` deu `200 != 400`. Não há risco de comando nem de consulta: varredura de `caso/miniloja/` por `subprocess`, `os.system`, `eval(`, `exec(`, `open(`, `sqlite`, `execute(`, `os.path`, `pickle` não achou nada no código original, e o PR não usa SQL nem shell. Limite: os campos do CSV são numéricos, então não há injeção de fórmula hoje; passaria a haver se o CSV incluísse texto do cliente.

**Algum teste falharia se a mudança fosse removida? Algum afirma o valor que o dublê devolveu?** Só o teste do PR (`test_exportacao.py`) cobre a mudança, e ele afirma o valor do dublê: `repo.todos.return_value` tem 2 pedidos e o teste confere `linhas == 2`, que vem de `len(pedidos)`, a própria lista do mock. Mutações numa cópia fora do repositório, com o patch aplicado, rodando só esse teste:

| Mutação em `exportacao.py` / `handlers.py` | Teste do PR |
| --- | --- |
| A: nenhum CSV é gravado (remove o `try`) | **passa** |
| B: `linhas` fixo em 2 em vez de `len(pedidos)` | **passa** |
| C: ignora o repositório (lista vazia) | falha, só porque muda a fonte do mock |
| D: `get_exportacao` quebrada em `handlers.py` | **passa** (o teste nunca a chama) |

Remover a função inteira falha apenas por `ImportError`. Conclusão: o teste não protege o comportamento (nem R4, nem o arquivo gravado); os "27 testes passam" não sustentam "código seguro".

**Acesso e segredos.** O controle de acesso está quebrado (R4, achado 1). Além disso, o arquivo fica em `exports/` com nome escolhido pelo cliente: quem adivinha o nome pode obtê-lo, e uma nova exportação com o mesmo nome o sobrescreve (comentário, sem teste). Segredos: busca no patch e na descrição por `secret`, `token`, `senha`, `password`, `api_key`, `chave`, `http`, `@` não achou nada; o `tok_ok` do código antigo é dado do `GatewayFake`, e o PR não mexe nisso. Consultas: o repositório é em memória, sem SQL nem shell, então não há injeção de consulta ou de comando.

**Dependência (existe, é mantida, é necessária, versão fixada).** `csv-export-helper` não existe: `https://pypi.org/pypi/csv-export-helper/json` -> 404, confirmado por `pip index`. Não há mantenedor verificável. Não é necessária (só `import csv`). A versão está fixada em `==0.4.2`, mas isso não protege: se alguém registrar o nome, o `pip install` roda código arbitrário, sem hash nem lockfile (*slopsquatting*). Não executei `pip download` do pacote, de propósito. A checagem vale para o PyPI público.

**Bordas observadas** (cópia com o patch, fora do repositório): repositório vazio -> `200`, `linhas: 0`, só o cabeçalho (bem tratado); total com milhar -> `"R$ 1.234,50"`; arquivo existente -> sobrescrito sem aviso; `nome_arquivo=""` -> `200` com `arquivo` apontando para a pasta; `nome_arquivo=None` -> `TypeError` sem status HTTP; `usuario_id=None` ou `999` -> `200` e exporta tudo; pedido com `total=None` ou sem a chave `total` -> `200` com `linhas` igual ao tamanho da lista (o erro é engolido pelo `except` e o CSV fica incompleto; eu não abri esses CSV, é inferência do código).

**Escopo e testes existentes.** O patch mexe em 4 arquivos, todos citados na descrição (`handlers.py` só com acréscimos, `requirements.txt` com uma linha, 2 arquivos novos). Nenhum teste antigo foi alterado ou removido: a suíte passou de 26 para 27 testes. Fora do pedido: a dependência (sem uso) e o efeito colateral do teste, que cria `exports/` no repositório.

**Duplicação, camada e API pública.** `_br` é idêntico a `formatar_moeda` (`miniloja/formatacao.py`), e `relatorios._fmt` é outra cópia parecida; remover `_br` e gravar número puro resolve também o achado 7. `exportacao.py` importa `handlers._repo` (atributo privado da camada de cima), cria um ciclo `handlers` <-> `exportacao` contornado com `import` dentro da função, e mistura regra de negócio com I/O fora do `PedidoService`; correção: receber o repositório como parâmetro. API pública: só acréscimos (`get_exportacao`, módulo `exportacao`, `EXPORT_DIR`, exigência em `requirements.txt`), sem quebrar assinaturas, mas é um endpoint fora de `caso/regras.md`, e a R4 vale para ele.

**Desempenho.** Sem consulta em laço nem laço aninhado (um único `for`); `todos()` copia a lista e varre os pedidos de todos os usuários, e o filtro por usuário (achado 1) não reduz essa varredura sem busca no repositório. Sem paginação, limite ou *streaming*. O PR não mediu nada (teste com 2 pedidos e mock). Medi com dados sintéticos em memória, com `tracemalloc` ligado (tempos inflados, ordem de grandeza):

| Pedidos | Tempo | Memória extra (pico) | Arquivo |
| --- | --- | --- | --- |
| 1.000 | 0,02 s | 0,2 MB | ~0 MB |
| 10.000 | 0,10 s | 0,3 MB | 0,2 MB |
| 100.000 | 0,95 s | 1,0 MB | 2,2 MB |
| 1.000.000 | 9,65 s | 8,2 MB | 22,7 MB |

Crescimento linear (~10 µs por linha); com milhões de pedidos o handler fica travado por segundos, sem timeout. Comentário, não bloqueio. Não medi concorrência nem disco de rede.

**Time, decisões e procedência.** O código do PR não tem autor humano que o explique (descrição do agente, patch assinado "Prof"); o parecer é meu e preciso conseguir explicá-lo sem a IA. Decisões a registrar: (1) rejeitar o merge, com condições de reabertura; (2) política de dependências do caso (só biblioteca padrão; dependência nova exige existência, mantenedor e justificativa); (3) a R4 vale para exportação? `regras.md` é omisso e não posso alterá-lo, então fica como pendência para quem mantém o contrato; (4) injetar o repositório em vez de importar `handlers._repo` (arquitetura, comentário). Procedência do PR: declara "escrito pelo agente", mas sem ferramenta, modelo, prompt nem revisão humana, e ainda afirma "código revisado e seguro" (falha de procedência, não bloqueio). Reprodutibilidade dos comandos do PR: `git apply` (na raiz, porque os caminhos começam em `caso/`) e a suíte `--existentes` (27 OK) funcionam; o teste do PR deixa `exports/` no repositório. O `test_revisao_pr.py` ficou fora do repositório: só o apêndice A deste rascunho o contém.

