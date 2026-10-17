# AGENTS.md — MiniLoja

- Verificar: `python -B testes/test_miniloja.py --codigo caso` (3 falhas de CPF/cadastro são esperadas no material inicial) e `python -B exercicios/aula-2/golden_master.py` (exit 0 = comportamento preservado).
- Python 3.11+, somente biblioteca padrão; não instale dependências.
- Não altere `testes/`, `caso/regras.md` nem arquivos fora do escopo declarado no pedido.
- Refatoração preserva comportamento: se algo parecer bug, **reporte e não corrija**.
- O contrato é `caso/regras.md`, não o código; o golden master congela o comportamento atual, inclusive erros conhecidos (`> 200`, `round()`).
- Antes de executar, apresente o plano e espere a revisão.
