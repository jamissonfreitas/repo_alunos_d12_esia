# Registro individual — AV1.6

**Lucas Costa Neves Macena — 24/10/2026.** Origem: meus registros AV1.1 (`exercicios/aula-1/registro-av1.md`), AV1.2 (`exercicios/aula-2/entrega-av1-2-registro.md`), AV1.3 (`exercicios/aula-3/registro-av1.3.md`), AV1.4 (`exercicios/aula-4/registro-av1-4-lucas-macena.md`), cada um em seu PR; estes caminhos valem após o merge deles. Time hipotético: produto, 5 a 8 pessoas, um serviço web.

| Campo | Meu desenho |
| --- | --- |
| Pergunta | Exigir escopo e plano revisados antes do diff do agente reduz o tempo até "verificado" sem piorar a qualidade? |
| Decisão | Manter ou retirar essa regra para tarefas delegadas ao agente (refatorações, atualização de dependências). |
| Métrica primária | Mediana, por tarefa, de minutos até "verificado" (testes, golden master e mutação sem queda, diff revisado, com esperas) e de idas e vindas. |
| Guardrail | Escore de mutação do conjunto fixo (piso 74%) e mudança no golden master (esperado 0). "Sugestões aceitas" mede uso, não valor. |
| Baseline | AV1.1 (17/10): até "pronto" 6 min com Plan, 13 manual (T1), 10 AcceptEdits (T2), sem suíte completa aprovada, idas e vindas 0 autodeclarado. AV1.2 (17/10): +28/−61 sem escopo, +22/−8 com, golden 12/12 só na rodada 2, revisão 4 min. AV1.3 (17/10): mutação 23/31 = 74%, rodada pelo Claude Code na minha cópia e revisada por mim, os mesmos 8 vivos de `apoio/resultado-textual.md`. AV1.4 (23/10): 1 de 5 refutada. Vêm de refatoração e legado, **não comparáveis** com "verificado" (AV1.1 mede "pronto"): o baseline real será coletado. |
| Período e método | 8 semanas, 2 tarefas parecidas por semana, com e sem escopo por sorteio, medianas pareadas. |
| Confundidores | Dificuldade, aprendizado, revisor, troca de modelo, testes instáveis, amostra pequena. |
| Gamificação | Pular a verificação ou aceitar testes tautológicos (AV1.3: 3 de 3 verdes sob sabotagem); fatiar tarefas. |

**Contramedida:** "verificado" usa a mesma mutação do baseline (`testes/mutacao_manual.py`); amostra semanal revisada por outra pessoa; tempo nunca isolado nem usado para avaliar pessoas.

| Tarefa candidata | Frequência e custo | Verificação determinística | Permissões e orçamento | Responsável |
| --- | --- | --- | --- | --- |
| Atualizar dependências de baixo risco; agente **propõe** PR em rascunho | Semanal; ~30 min, suposição minha | Suíte e golden iguais; diff só em manifestos; mutação não cai | Só branch própria, sem segredos, nunca PR de fork; 20 min e teto de tokens (escolha minha) | Mantenedor da semana |

Filtro: frequente, testável, pouca variação, raio contido. **Alternativa:** bot determinístico sem agente; se cobrir ≥80% dos casos (limiar meu), não adoto o agente.

**Limite e condição para interromper ou rever:** baseline de uma pessoa, uma rodada por modo, sem isolamento nem grupo de comparação: hoje é impressão, não ganho; a automação só é checada pelo que a suíte já testa. **Mantenho a regra** se a mediana cair ≥20% em ≥10 pares (limiares meus) sem a mutação ficar abaixo de 74%; senão ela sai. **Interrompo** se a mutação cair abaixo de 74%, o golden mudar ou houver reversão atribuível ao agente.

**Procedência/IA:** Claude Code, Claude Sonnet 5.5. Delegado: localizar meus registros, rascunhar e submeter a agentes (rubrica, checklist, fatos). Aproveitado: estrutura e rascunho; limiares e tarefa são escolhas minhas. Erro da IA: deu o AV1.1 como inexistente; agente de fatos o refutou e conferi no arquivo. Três rodadas de agentes apontaram falhas, já tratadas. Raciocínio e decisão são meus.

**Revisão:** [x] medição completa; [x] risco de manipulação; [x] automação com verificação; [x] limite; [ ] até uma página (a conferir).
