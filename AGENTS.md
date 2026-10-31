# AGENTS.md — MiniLoja
- Verificações: `python -B testes/test_miniloja.py --codigo caso` (11) e o mesmo com `--existentes` (26).
- Refatorar `caso/miniloja/calculo.py` exige `python -B golden/golden_calculo.py` = 224/224 (igualdade exata).
- Não alterar `testes/`, `golden/` nem `caso/regras.md`.
- Código diverge de `caso/regras.md`? Em refatoração, reporte; não corrija.
- Não usar `sum()` nem `Decimal` em `calculo.py`: soma compensada (Python 3.12+) e arredondamento mudam centavos e quebram o golden.
- Antes de editar: declarar o que pode e não pode tocar e apresentar o plano.
