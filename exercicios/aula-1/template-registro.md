# Registro individual — AV1.1

**Limite: uma página, incluindo evidências essenciais.** Estudante: ___ — Data: 16/10/2026
Origem: tarefas T1–T3 fictícias do enunciado; modalidade: execução própria (T1, modo A); resposta simulada (T1, modo B, `apoio/respostas-simuladas/b1-cpf-completar.md`); T2 e T3 não preenchidos.

| Tarefa | Modo | Tempo até 1ª versão | Tempo até pronto e verificado | Idas e vindas | % corrigido à mão | O que a IA errou | Como verifiquei |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A: agente (Claude Code, edição direta de `cadastro.py`) | 48s  | < 2 minutos, o Claude já havia executado os testes para confirmar a correção | 2 ajustes após a 1ª versão (rodar verificações, corrigir regressão) | 0%; sem edição manual do código gerado | 1ª versão tornou `cpf` obrigatório e quebrou `test_cadastro_valido` da suíte existente (cadastro sem `cpf` esperava `201`); a IA também não adiantou que R3.1 conflita com esse teste | `python -B testes/test_miniloja.py --codigo caso` (v08 e v09 passam) e `--existentes` (26 OK) |
| T1 | B: completar no editor (**resposta simulada** pelo professor, não executei a tarefa; só analisei e testei a sugestão) | 2min (simulado) | não alcançado: a sugestão não passa em `v09`; sem correção, não há versão verificada | 0 na simulação | não se aplica (não corrigi a sugestão) | Não rejeita CPF com todos os dígitos iguais: `111.111.111-11` e `00000000000` passam nos dois dígitos verificadores (soma 54→1 e 65→1; soma 0→0), então devolve `201` em vez de `422` | Copiei o pacote para uma pasta de trabalho, apliquei a sugestão e rodei `--codigo` e `--existentes` |
| T2 | ___ |  |  |  |  |  |  |

**Trecho essencial de evidência (comando e saída que sustentam "verificado"):** T1, modo A. Antes: v08 e v09 falhavam com `AssertionError: 201 != 422`. Depois, `python -B testes/test_miniloja.py --codigo caso`: `Ran 11 tests`, `FAILED (failures=1)`, só `v10` (tarefa T2) falha. `--existentes`: `Ran 26 tests`, `OK`. Modo B (cópia de trabalho, sugestão simulada): `--codigo`: `FAILED (failures=2)`, `v09` com `AssertionError: 201 != 422` e `v10` (T2); `--existentes`: 26 `OK`. Versão final em `caso/miniloja/cadastro.py` (cobre também R3.1, R3.3 e R3.4, logo adianta T2): `--codigo`: `Ran 11 tests`, `OK`; `--existentes`: `Ran 26 tests`, `OK`. Limite: para isso alterei 2 testes de `caso/testes_existentes/test_cadastro.py`, pois o contrato mudou de `400` para `422` e o `cpf` passou a ser obrigatório (R3.1); `testes/` e `caso/regras.md` não foram alterados.

**T3 (hipotética): raio de impacto ___; oráculo disponível ___; permissões que concederia ___; modo e por quê ___.**

**Alternativa para ___:** ___ **Comparação com minha escolha (restrição e consequência):** ___ **Limite da comparação e condição para rever a escolha:** ___

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Sonnet 5.5; tarefa delegada e contexto: T1, validar CPF em `caso/miniloja/cadastro.py` com R3.2 e as verificações v08/v09; trecho aproveitado: função `_cpf_valido` e o retorno `422` com `erros`; minha verificação/intervenção: não informado. Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] dois modos em T1 (B simulado); [x] evidência localizada; [ ] T3 decidida; [ ] alternativa e limite; [ ] até uma página.
