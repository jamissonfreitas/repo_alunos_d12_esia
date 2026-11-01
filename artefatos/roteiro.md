# Roteiro AV1.2

Este roteiro orienta a execução do exercício descrito em [`exercicios/aula-2/README.md`](../exercicios/aula-2/README.md). O objetivo é refatorar `calcular_total` em duas rodadas e comparar diff, preservação do comportamento e esforço de revisão. O estudante toma as decisões e escreve o registro individual; o assistente de programação auxilia com inspeção, execução e evidências verificáveis.

## Regras de trabalho

- Leia `CLAUDE.md`, `caso/regras.md`, `caso/miniloja/calculo.py`, `caso/miniloja/flags.py`, a suíte existente pertinente e o README do exercício antes de propor mudanças.
- O contrato R1 informa o comportamento esperado; o golden master registra o comportamento atual. Preserve o comportamento atual durante a refatoração, mesmo quando ele divergir do contrato.
- Se identificar possível bug ou divergência com R1, descreva e registre, sem corrigir. Mudança de comportamento está fora desta refatoração.
- Não edite `caso/regras.md`, `testes/` nem arquivos alheios ao escopo aprovado. Não mude assinatura pública nem ajuste testes para acomodar a implementação.
- Não invente resultados, contagens, duração, aprovação, saída de comandos ou metadados. Diferencie fatos observados, estimativas e campos ainda não preenchidos.
- Se usar as respostas em `apoio/respostas-simuladas/`, trate-as explicitamente como simuladas. Elas não são execução real e não podem ser relatadas como tal.
- Registre o uso de IA com os metadados disponíveis; use “não informado” quando não forem observáveis.

## Fase 1 — Preparação e golden master

1. Confira o estado do repositório e identifique alterações preexistentes. Não as sobrescreva nem as inclua na comparação.
2. Leia o contrato R1, com atenção à ordem desconto → frete → taxa, cupons, UFs e arredondamento. Leia o código e a implementação de `flags.promo_natal_ativa()`.
3. Antes de qualquer pedido de refatoração, escreva o critério de pronto e o escopo da rodada 2.
4. Gere o golden master a partir da implementação original, antes da rodada 1. Use uma lista documentada de entradas variadas que inclua carrinhos, `PROMO10`, `VIP15`, `FRETEGRATIS`, `NATAL` com flag ligada e desligada, cupom inválido, UFs PE, SP, RJ e outra UF. Inclua casos de fronteira pertinentes, como subtotal exatamente R$ 200,00, se possível.
5. Capture e preserve as saídas originais sem alterar a implementação. Documente número e descrição das entradas, ambiente relevante (incluindo valor de `MINILOJA_PROMO_NATAL`) e como reproduzir a captura.
6. A comparação deve usar igualdade exata das saídas, sem tolerância numérica. Aplique a mesma lista de entradas e condições ambientais antes/depois de cada rodada. Não confunda aprovação do golden master com conformidade ao contrato.
7. Mostre ao estudante o método, a captura e a comparação para revisão. Não avance para a rodada 1 sem a validação do golden master pelo estudante.

Se a comparação revelar divergência com R1, não “corrija” o golden master. Preserve a saída atual como referência e anote a divergência para o registro.

## Fase 2 — Rodada 1, sem escopo

1. Com o golden master validado, registre o ponto inicial da rodada (diff/status e arquivos relevantes).
2. Faça somente o pedido sem escopo indicado no exercício: **“Refatore `calcular_total`.”** Não acrescente restrições que transformem a rodada em uma rodada com escopo.
3. Antes de executar mudanças, registre o plano/resposta do assistente e peça ao estudante que conduza/revise a interação conforme a atividade.
4. Ao terminar, registre os arquivos modificados, linhas adicionadas/removidas, resultado da comparação exata e tempo de revisão informado pelo estudante. Separe tempo observado de estimativa; não calcule o tempo por suposição.
5. Inspecione o diff e classifique mudanças estruturais e comportamentais. Registre qualquer possível bug que tenha sido encontrado, sem corrigir.
6. Mostre o diff e os dados ao estudante. Depois da revisão, reverta apenas as alterações da rodada 1, preservando todas as alterações preexistentes. Confirme que o ponto de partida da rodada 2 está limpo em relação à rodada 1.

## Fase 3 — Rodada 2, com escopo

1. Antes de receber um plano do agente, peça ao estudante que preencha, com suas próprias decisões, os seis campos:
   - **Objetivo:**
   - **Pode tocar:**
   - **Não pode tocar:**
   - **Invariantes:**
   - **Critério de pronto:**
   - **Critério de parada:**
2. Registre o escopo e seu horário/ordem em relação ao pedido. O escopo precisa existir antes do pedido ao assistente.
3. Só então solicite um **plano**, sem editar arquivos. Apresente-o ao estudante para revisão.
4. Aguarde o estudante indicar os cortes ou ajustes. Registre o plano original e as alterações feitas antes da execução, com justificativas. Não aprove mudanças fora do escopo por conta própria.
5. Execute apenas após a revisão explícita do estudante. Se o escopo não permitir uma ação necessária, se surgir ambiguidade material ou se houver risco de alteração de comportamento, pare e pergunte, conforme o critério de parada.
6. Rode a mesma comparação exata do golden master. Não altere dados de referência ou testes para obter aprovação. Registre diff, arquivos, resultado, tempo de revisão informado e idas e vindas.
7. Se o comportamento atual divergir do contrato (por exemplo, o código usa `total > 200` enquanto R1 diz frete grátis a partir de `>= 200`), reporte a observação e mantenha o comportamento. Anote-a como possível correção futura fora do escopo.

## Fase 4 — `AGENTS.md` mínimo

Ajude o estudante a redigir um `AGENTS.md` de 5 a 8 linhas, com comandos de verificação reais deste repositório, limites de alteração e uma convenção não óbvia. Não invente comandos. Confira que o arquivo não introduz instruções conflitantes com o escopo ou o contrato. O estudante decide onde salvá-lo e confirma o conteúdo antes de gravar.

## Fase 5 — Registro individual

Preencha com o estudante uma cópia do template [`exercicios/aula-2/template-registro.md`](../exercicios/aula-2/template-registro.md), mantendo o limite de uma página. Inclua:

- descrição e quantidade de entradas do golden master, método de geração e comparação exata;
- números reais das duas rodadas: linhas, arquivos, comportamento e tempo de revisão; inclua idas e vindas se observadas;
- os seis campos do escopo, registrados antes do plano, e cortes/ajustes feitos no plano;
- um possível bug que foi reportado sem correção, se encontrado;
- o `AGENTS.md` mínimo;
- trecho essencial de evidência, limite do golden master e condição para ampliar/reduzir o escopo;
- procedência da assistência de IA, declarando se a execução foi própria ou simulada.

Não assine decisões ou reflexões pelo estudante. Deixe campos pessoais e avaliações subjetivas para ele completar. Se faltarem dados, marque-os como pendentes em vez de preencher por inferência.

## Critério de encerramento

O trabalho está pronto quando o estudante consegue demonstrar que o escopo da rodada 2 foi escrito antes do pedido e do plano, revisar os números e a evidência das duas rodadas, e conferir que a refatoração preservou exatamente as saídas capturadas. Entregue o registro ao estudante para revisão; não envie a terceiros.
