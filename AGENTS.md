# AGENTS.md

- Runtime: Python 3.11+, somente biblioteca padrão (sem instalar dependências).
- Verificações (na raiz): `python -B testes/test_miniloja.py --codigo caso`; uma só: `--teste TestMiniLoja.nome`.
- Suíte existente: `... --codigo caso --existentes` (26 testes, parte tautológica de propósito; não serve como prova).
- Código em `caso/miniloja/`; use `--codigo DIR` para testar uma cópia de trabalho.
- Limites: não alterar `testes/` nem `caso/regras.md`; declare escopo e plano antes de mudar o caso.
- Convenção não óbvia: `caso/regras.md` (contrato) vale mais que o código atual; em caso de conflito, o código está errado.
- Saída `1` = há falhas, `0` = sucesso; no material inicial, 3 das 11 verificações falham (tarefas do bloco 1).