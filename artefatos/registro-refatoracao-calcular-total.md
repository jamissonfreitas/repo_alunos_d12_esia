# Revisão da refatoração de `calcular_total`

## Escopo e diff

- Arquivo alterado: `caso/miniloja/calculo.py`.
- Diff: 28 linhas adicionadas e 61 removidas; arquivo passou de 73 para 41 linhas (redução líquida de 32 linhas).
- Linhas atuais: constantes nas linhas 4–10; helpers `_subtotal` (13–18), `_aplicar_desconto` (21–27) e `_calcular_frete` (30–33); `calcular_total` nas linhas 36–41.
- O diff também removeu comentários antigos e substituiu os condicionais de cupom, frete e taxa por dicionários e helpers.

## Classificação das mudanças

**Estruturais:** extração da soma, desconto e frete para três funções privadas; centralização de valores em constantes; troca de ramificações `if/elif` por consultas aos dicionários de taxa e frete. A função pública continua coordenando as mesmas etapas, na mesma ordem.

**Comportamentais nos casos válidos cobertos:** não identifiquei mudança esperada nos 12 casos do golden master. Essa conclusão ainda depende de executar a comparação oficial, pendente conforme abaixo.

**Possíveis mudanças comportamentais/bugs encontrados (não corrigidos):**

- Em `_aplicar_desconto` (linha 23), `cupom in FATOR_DESCONTO` exige valor hashable. Antes, um cupom como lista era comparado às strings e ignorado; agora levanta `TypeError`.
- Em `_calcular_frete` (linha 33) e na seleção de taxa (linha 40), `dict.get(uf, ...)` também exige UF hashable. Antes, uma UF como lista não correspondia às strings e caía nos valores padrão; agora levanta `TypeError`.
- Os novos dicionários de configuração (`FRETE_POR_UF`, `TAXA_POR_UF`, `FATOR_DESCONTO`) são mutáveis e acessíveis no módulo. A lógica anterior não dependia de tabelas mutáveis exportadas; outro código que alterar esses objetos pode alterar os resultados. Não há evidência de mutação no escopo inspecionado.

## Comportamento e golden master

A refatoração mantém a assinatura pública e a ordem de cálculo: subtotal sequencial, desconto, frete, taxa e arredondamento final. Os doze casos registrados em `golden_master_original.json` cobrem cupons, flag NATAL, UFs, limite de R$ 200 e carrinho vazio. A leitura do código indica que as saídas desses casos permanecem iguais.

**Validação executável pendente:** não foi possível executar `python -B artefatos/golden_master.py --compare`, porque `python` e o launcher `py` não estão disponíveis no PATH deste ambiente. Portanto, não registro o golden master como aprovado; a igualdade acima é análise dos casos e do código, não resultado da comparação oficial.

Os casos acima não são exercitados pelo golden master atual.

## Tempo de revisão

Tempo observado nesta revisão: aproximadamente 2 minutos, da inspeção inicial ao registro. A validação oficial não foi concluída pelo motivo de ambiente descrito acima.
