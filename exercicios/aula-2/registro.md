# Registro individual — AV1.2

**Limite: uma página, incluindo evidências essenciais.** Estudante: Márcio Belarmino de Arruda — Data: 17/10/2026
Origem: `caso/miniloja/calculo.py` fictício; modalidade: execução própria.

**Golden master:** 630 entradas; gerado por `exercicios/aula-2/golden_master.py --gravar` a partir do código original (9 carrinhos × 7 cupons × 5 UFs × flag NATAL 0/1, incluindo subtotal 200 exato, cupom inválido, `promo10` e `pe` minúsculos); comparação exata por tipo + `repr()` do retorno comparados como texto, sem tolerância. Resultado: 0 divergências no original, na rodada 1 e na rodada 2. Teste de sensibilidade: trocar `> 200` por `>= 200` numa cópia gerou 40 divergências (exit 1).

| Medida | Rodada 1 (sem escopo) | Rodada 2 (com escopo) |
| --- | --- | --- |
| Linhas adicionadas/removidas | +27 / −61 | +11 / −32 |
| Arquivos alterados (e quais estavam fora do esperado) | 1 (`calculo.py`); criou 4 funções e 4 constantes não pedidas | 1 (`calculo.py`); nenhum extra fora do arquivo |
| Mudou comportamento? (golden master) | Não (0/630) | Não (0/630) |
| Tempo de revisão | ~10 min | 6 min |
| Idas e vindas | 200 virou constante (`>` separado do valor); fatores divididos entre dicionário e `0.8` solto; `if` aninhado virou `and`; `None` tratado implicitamente | papel de `desconto_aplicado`; equivalência do `and` no NATAL |

**Escopo da rodada 2:** objetivo deixar `calcular_total` mais legível sem mudar o comportamento; pode tocar só `calcular_total` em `calculo.py`; não pode tocar outros arquivos, assinatura, `> 200` e `round()`; invariantes golden master 0 divergências e verificações iguais às atuais (8 passam); pronto quando golden master exit 0 e diff menor que o da rodada 1; pare e pergunte se precisar mudar comportamento ou tocar outro arquivo.
**Plano do agente: o que eu cortei ou corrigi antes de executar:** pedi uma nova versão do plano e escolhi a de diff mínimo. Ficaram fora: troca do laço por `sum()` (estilo, não legibilidade), uso de `FRETE_POR_UF`/`TAXA_POR_UF` com `.get()` (aumenta o diff e o risco no valor padrão) e remoção do comentário de 2023 (histórico). Mantidos: remover `desconto_aplicado` e o `if ...: pass` (código morto) e unir as condições do frete. Desvio na execução: o agente também juntou `NATAL` e a flag num `and`, o que não estava no plano (equivalente, confirmado pelo golden master).
**Algo que parecia bug e eu apenas reportei:** R1.3 pede frete grátis com subtotal ≥ 200, mas o código usa `> 200`; R1.5 pede arredondamento meio para cima, mas o código usa `round()` de float; `FRETE_POR_UF`/`TAXA_POR_UF` definidas e sem uso; cupom e UF diferenciam maiúsculas (o contrato não fala disso).
**`AGENTS.md` mínimo:** ver `exercicios/aula-2/AGENTS.md` (comandos de verificação, limites de escopo, "reporte, não corrija", plano antes de executar)

**Trecho essencial de evidência:** `python -B exercicios/aula-2/golden_master.py` → `630 casos comparados, 0 divergência(s).`; `git diff --numstat` → rodada 1 `27 61`, rodada 2 `11 32`; `testes/test_miniloja.py --codigo caso` → 8/11 nas duas (falham v08, v09, v10, de CPF/cadastro, fora do escopo). Diffs em `rodada1.diff` e `rodada2.diff`. **Limite e condição para rever o escopo:** o golden master garante que nada mudou, não que está certo: ele congela os erros do `> 200` e do `round()` e só cobre as 630 entradas gravadas. Revisei a rodada 2 depois da 1, já conhecendo o código, o que favorece a segunda. Na rodada 1 o agente já tinha o golden master e o `CLAUDE.md` no contexto, então o resultado sem escopo foi mais contido do que seria sem esse contexto. Eu ampliaria o escopo só numa mudança separada para corrigir R1.3/R1.5, com testes derivados do contrato e regravação declarada do golden master; e reduziria se o diff passasse do da rodada 1 ou se fosse preciso tocar outro arquivo.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code, Claude Opus 5.5 (`claude-opus-5-5`); tarefa delegada e contexto: script do golden master, execução das rodadas 1 e 2, medição dos diffs e rascunho deste registro e do `AGENTS.md`, com o repositório e o `CLAUDE.md` como contexto; trecho aproveitado: script, diffs e rascunho do texto; minha verificação/intervenção: escolhi o escopo, pedi a revisão do plano e escolhi a versão de diff mínimo, revisei os dois diffs cronometrando e conferi as equivalências (constante 200, fatores, `and` do NATAL). Use "não informado" para metadados indisponíveis. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] golden master; [x] duas rodadas com números; [x] seis campos; [x] AGENTS.md; [x] até uma página.
