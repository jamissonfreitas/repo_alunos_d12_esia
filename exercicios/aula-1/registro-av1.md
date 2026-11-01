# Registro individual — AV1.1

**Limite: uma página, incluindo evidências essenciais.** Estudante: Lucas Macena — Data: 17/10/2026
Origem: tarefas T1–T3 fictícias do enunciado; modalidade: execução própria (T1/T2); T3 hipotética.

| Tarefa | Modo | Tempo até 1ª versão | Tempo até pronto e verificado | Idas e vindas | % corrigido à mão | O que a IA errou | Como verifiquei |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | A: Plan → implementação; revisar escopo antes de editar | 6 min | 6 min | 0, informado | 0%, informado | Impressão Unicode falhou; corrigida para UTF-8 | v08/v09 ok; v10 falha; existentes: 26/26; CPFs adicionais |
| T1 | B: instruções manuais ao Claude; controlar cada etapa | 13 min, incluindo espera | 13 min, incluindo espera | 0, informado | 0%, informado | Nenhum erro funcional identificado; faltou executar a linha de base | v08/v09 ok; v10 falha; existentes: 25/26; 13 entradas de CPF |
| T2 | Claude AcceptEdits; agilizar edições delimitadas | 10 min | 10 min | 0, informado | 0%, informado | Tentou gravar antes de ler; testes rodaram sem alteração; leu, gravou e repetiu | v10/v08 ok; v09 falha; existentes: 24/26 |

**Trecho essencial de evidência (comando e saída que sustentam "verificado"):** `python -B testes/test_miniloja.py --codigo caso` → T2: `Ran 11 tests ... FAILED (failures=1)`, saída 1; v10 ok, falha em v09. Com `--existentes`: `Ran 26 tests ... FAILED (failures=2)`, saída 1. Nenhum teste alterado. Conflitos com testes existentes: B rejeita cadastro sem CPF; T2 também troca 400 por 422, conforme R3. Suítes completas não aprovadas; A ainda aceita CPF ausente.

**T3 (hipotética): raio de impacto alto, produção; oráculo disponível métricas e logs, insuficientes para garantir causa; permissões que concederia leitura e diagnósticos limitados previamente revisados, sem escrita, reinício ou deploy; modo e por quê agente supervisionado, para investigar com impacto limitado; mudanças exigem revisão e autorização próprias.**

**Alternativa para T1/A:** condução manual de T1/B. **Comparação com minha escolha (restrição e consequência):** Plan permite revisar o escopo antecipadamente; condução manual exige aprovar cada etapa. Tempos informados até a primeira versão e até pronto e verificado coincidem: 6 versus 13 min, com espera em B. **Limite da comparação e condição para rever a escolha:** uma rodada por modo, isolamento de A/B não comprovado e decisões diferentes sobre CPF ausente impedem concluir superioridade. A alternância da ordem com o colega não foi validada, pois a atividade foi realizada fora do horário de aula. Mudaria de Plan para condução manual se, em novas rodadas com os mesmos insumos, critérios de aceite e ambientes isolados, ela reduzisse consistentemente o tempo até pronto e verificado, incluindo as esperas por aprovação, sem aumentar falhas ou retrabalho.

**Procedência/IA:** ferramenta e modelo visíveis: Claude Code / Claude Sonnet 5.5, conforme artefatos; tarefa delegada e contexto: validar CPF e acumular erros, com R3, código e testes; trecho aproveitado: validação e respostas de cadastro; minha verificação/intervenção: aprovação de escopo, decisões sobre CPF e conferência das saídas registradas. Versão da ferramenta e assistência na preparação dos roteiros: não informado. O raciocínio e a decisão registrados são meus.

**Revisão:** [x] dois modos em T1; [x] evidência localizada; [x] T3 decidida; [x] alternativa e limite; [x] até uma página.

