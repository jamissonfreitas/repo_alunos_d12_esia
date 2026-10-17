# Registro individual — AV1.3

**Limite: uma página, incluindo evidências essenciais.** Estudante: Márcio Belarmino de Arruda — Data: 17/10/2026
Origem: `caso/testes_existentes/` e `caso/regras.md` fictícios; modalidade: execução própria (Python 3.12.10; sabotagens numa cópia de `caso/`, código refatorado da AV1.2; mutação sobre o código original `2c2fc89`).

| Teste suspeito | Tipo de tautologia | Sabotagem que apliquei (ou raciocínio) | Continuou verde? |
| --- | --- | --- | --- |
| `test_calculo.test_cupom_natal_com_flag` | Sem asserção real (só `assertIsNotNone`) | `total * 0.8` → `total * 0.79` no ramo do `NATAL` | Sim (26 OK) |
| `test_pedidos.test_fluxo_chama_colaboradores` (e `test_criar_pedido`) | Super-mockado / afirma o mock (só `.called`) | `self.gateway.cobrar(total, token)` → `cobrar(0, token)`: cobra R$ 0,00 | Sim (26 OK) |
| `test_calculo.test_cenarios_gravados` | Snapshot do próprio código (`limite_200: 223.55` é a saída atual, não R1.3) | `total > 200` → `total >= 200` (correção pedida pelo contrato) | Não: **falhou por defender o erro** |

| Mutante sobrevivente | Por que sobreviveu | Teste que o mataria (ou "equivalente", com justificativa) |
| --- | --- | --- |
| `calculo.py`: NATAL 20% → 21% | O único teste do `NATAL` não compara valor | `test_m1`: R$ 100, `NATAL`, flag 1, UF XX → 80 + 29,90 = 109,90 × 1,08 = 118,692 → **118,69** (mutante dá 117,61) |
| `estoque.py`: `<` → `<=` (limite exato) | Nenhum teste pede exatamente o saldo | `test_m2`: saldo 3, reservar 3 → `True` e saldo 0 (mutante levanta `EstoqueInsuficiente`) |

| Caso derivado do contrato (entrada) | Esperado (cálculo à mão) | Observado no código | Decisão |
| --- | --- | --- | --- |
| C1 fronteira: 2 × R$ 100, sem cupom, PE | 200,00 ≥ 200 → frete 0 (R1.3); 200,00 × 1,05 = **210,00** | 223,55 | Código errado (`> 200` em vez de `>=`) |
| C2 arredondamento: 1 × R$ 220, `PROMO10`, PE | 220 × 0,90 = 198,00 < 200 → frete 12,90 (R1.6); 210,90 × 1,05 = 221,445 → **221,45** (R1.5) | 221,44 | Código errado (`round()` de float: 210,9 + 10,545000000000002 fica abaixo de ,445) |
| C3 frete RJ: 1 × R$ 40, sem cupom, RJ | (40,00 + 21,50) × 1,06 = **65,19** | 65,19 | Concorda; vira teste (também mata o mutante "frete RJ") |

**ADR curto:** contexto: C1 e C2 divergem do contrato (R1.3 diz "maior ou igual a R$ 200,00"; R1.5 diz "meio para cima") e `test_cenarios_gravados` congela o 223,55, então a suíte reprova justamente a correção; decisão: o lado errado é o código, porque o texto do contrato é explícito e o contrato vale mais que o código; o esperado fica 210,00/221,45 e a correção (`>=` e arredondamento `Decimal` com `ROUND_HALF_UP`) vai numa mudança separada com escopo declarado; consequências: `limite_200` e o golden master da AV1.2 (40 divergências com `>=`) precisam ser regravados de forma declarada, e os totais de pedidos na faixa de 200 mudam; alternativa descartada: trocar o esperado por 223,55 (teste espelho) ou ler R1.3 como "maior que".

**Trecho essencial de evidência:** `python -B testes/test_miniloja.py --codigo caso --existentes` → `Ran 26 tests … OK`; com cada sabotagem acima na cópia: NATAL `OK`, `cobrar(0)` `OK`, `>= 200` → `FAIL: test_cenarios_gravados`. `MINILOJA_TEST_CMD="python -B testes/test_miniloja.py --existentes --codigo caso -x" python -B testes/mutacao_manual.py` (no original) → `Mutantes: 31 | mortos: 23 | sobreviventes: 8 | escore: 74%`. `python -B exercicios/aula-3/test_av13.py` → m1, m2, c3 `ok`; c1 `223.55 != 210.0`, c2 `221.44 != 221.45` (falham de propósito); m1 contra o mutante → `117.61 != 118.69`, m2 → `EstoqueInsuficiente`. **Limite do que a suíte garante e condição para rever a decisão:** mesmo com os 5 testes, a suíte só cobre os pontos escolhidos: não verifica R2.2 (por leitura, `PedidoService.criar` reserva item a item e não desfaz a reserva se um item seguinte faltar), nem VIP15 em `descontos.py`, `total_fmt` e e-mail obrigatório (sobreviventes restantes). O mutante "variável sem efeito" é **equivalente**: `desconto_aplicado` só alimentava `if desconto_aplicado: pass`, sem efeito observável (e saiu do código na AV1.2). No código refatorado a ferramenta de mutação aborta (`trecho não encontrado: 'if total > 200:'`), por isso o escore é do original. Reviso o ADR se o dono do contrato publicar uma versão que mude R1.3/R1.5 ou se outra parte (relatório, pagamento) depender do valor atual.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Claude Opus 5.5 (`claude-opus-5-5`); tarefa delegada e contexto: executar a linha de base, as sabotagens numa cópia, a mutação e os cálculos em `Decimal`, escrever `test_av13.py` e o rascunho deste registro, com o repositório, `regras.md` e o `CLAUDE.md` como contexto; trecho aproveitado: comandos, saídas, testes e rascunho do texto; minha verificação/intervenção: refiz à mão os cálculos de C1, C2, C3 e m1, conferi que a sabotagem do NATAL alterou só o `0.8` (a primeira tentativa, sem fim de linha, pegou o `0.85` do VIP15 e foi descartada) e decidi pelo código errado no ADR. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] três testes; [x] dois mutantes; [x] três casos do contrato; [x] ADR; [x] até uma página.
