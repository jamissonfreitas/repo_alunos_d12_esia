# AV3 B3 — Corrige reserva parcial de estoque na criação de pedidos

## Intenção e comportamento

Cumprir R2.2: se algum item não tiver estoque, responder `409` sem consumir saldo nem deixar reservas desta tentativa. Antes, a falta de estoque em um item posterior mantinha os débitos dos itens anteriores. Agora, `Estoque.reservar_lote` simula os débitos em uma cópia dos saldos, acumula as quantidades de SKUs repetidos e só efetiva as reservas quando todos os itens podem ser atendidos. Reservas anteriores, inclusive do mesmo usuário, são preservadas na recusa.

## Escopo e plano

A mudança de código fica em `caso/miniloja/estoque.py`, `caso/miniloja/pedidos.py` e na expectativa de colaboração em `caso/testes_existentes/test_pedidos.py` (20 linhas adicionadas e quatro removidas). Os artefatos da AV3 incluem teste de regressão, escopo, evidências, registro individual e descrição da entrega.

O escopo de seis campos está em `avaliacoes/av3/ESCOPO_PREVIO.md`: objetivo, arquivos permitidos, arquivos proibidos, invariantes, condição de conclusão e condição de parada. A assinatura de `PedidoService.criar`, as respostas, a exceção de estoque e os fluxos aprovado e de pagamento recusado são preservados. `testes/`, `caso/regras.md`, cálculo, cadastro, acesso e pagamentos ficam fora da alteração.

Plano registrado para a implementação:

1. Escrever uma regressão com estoque, repositório e gateway reais e executá-la na base `1a12ad2`.
2. Validar o lote inteiro antes de reservar, incluindo SKUs repetidos.
3. Integrar a reserva em lote ao serviço de pedidos e ajustar o teste de colaboração.
4. Reexecutar regressão, suítes e golden masters; conferir o diff e registrar resultados.

O plano e o escopo foram revisados e aceitos pelo estudante.

## Verificação: comandos e saídas

Executar da raiz, com Python 3.11+ e somente biblioteca padrão. Os resultados abaixo foram executados e conferidos pelo estudante com Python 3.13.14; `avaliacoes/av3/EVIDENCIAS.md` registra as saídas.

| Comando | Resultado observado | Saída do processo |
| --- | --- | --- |
| `python -B -m unittest avaliacoes/av3/test_reserva_estoque.py -v` | `Ran 2 tests`; `OK` | 0 |
| `python -B testes/test_miniloja.py --codigo caso --existentes` | `Ran 26 tests`; `OK` | 0 |
| `python -B testes/test_miniloja.py --codigo caso` | `Ran 11 tests`; `FAILED (failures=3)` | 1 |
| `python -B artefatos/golden_master.py --compare` | `OK: 12` saídas iguais exatamente às capturadas | 0 |
| `python -B avaliacoes/av2/golden.py --compare` | `IGUAL: 2882 casos, 268203 bytes (calculo.py)` | 0 |
| `git diff --check HEAD` | Sem saída; nenhuma inconsistência de whitespace detectada | 0 |

As três falhas gerais são as anteriores de cadastro: v08 (`201 != 422`), v09 (`201 != 422`) e v10 (`400 != 422`). São declaradas como falhas e permanecem fora de B3. Os 26 testes existentes não são usados isoladamente como prova da correção.

O golden da AV2 é uma verificação complementar que depende dos insumos locais daquela avaliação, excluídos da entrega B3. A regressão B3 pode ser executada sem esses insumos.

## Teste que falharia sem a mudança

`TestReservaEstoque.test_falha_preserva_estado_e_nao_cobra_nem_salva`, em `avaliacoes/av3/test_reserva_estoque.py`, compara exatamente saldos e reservas anteriores e exige resposta `409`, nenhuma cobrança e nenhum pedido salvo.

Reprodução em uma cópia temporária da base `1a12ad2`, adicionando somente o novo arquivo de teste:

```text
python -B -m unittest avaliacoes/av3/test_reserva_estoque.py -v
Ran 2 tests
FAILED (failures=3)
```

Falharam os subtestes de item intermediário, último item e SKU repetido: saldos observados `{'A': 3, 'B': 3}`, `{'A': 3, 'B': 2}` e `{'A': 2, 'B': 3}`, respectivamente, contra `{'A': 4, 'B': 3}` esperado. Com a correção, ambos os métodos de teste passam, incluindo esses cenários, a insuficiência no primeiro item e uma compra aprovada com SKU repetido. Isso demonstra que a regressão detecta o defeito original.

## Dependências e modo de interação

Nenhuma dependência nova; implementação e testes usam somente a biblioteca padrão.

Modo usado: agente de codificação com escopo explícito. O raio de impacto fica limitado a estoque e pedidos; o oráculo é o contrato R2.2, verificado por estado real antes/depois; a familiaridade foi construída pela leitura do contrato e dos módulos. A implementação e a preparação das evidências foram delegadas ao Claude (Claude Code, modelo Claude Sonnet 5.5), com revisão e decisão de aceite pelo estudante.

Alternativa comparada: edição manual daria controle por linha e exigiria a mesma prova de regressão. O agente foi escolhido para delegar uma implementação pequena, delimitada por arquivos, invariantes e verificações observáveis. A declaração completa de procedência e as correções dos erros da IA constam em `avaliacoes/av3/registro-av3-lucasmacena.md`.

## Limites

A solução atende à execução sequencial em memória. Concorrência, persistência e compensação de pagamento exigem outro desenho. A representação existente de reservas de SKUs repetidos no fluxo aprovado foi preservada.
