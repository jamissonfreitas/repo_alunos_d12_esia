"""AV1.3: testes propostos (2 mutantes + 3 casos derivados do contrato).

Uso, na raiz do pacote: python -B exercicios/aula-3/test_av13.py [--codigo DIR]
O esperado de cada teste foi calculado à mão a partir de caso/regras.md, não do código.
No código atual, c1 e c2 FALHAM de propósito: são as divergências do ADR do registro.
"""
import os
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
codigo = RAIZ / "caso"
if "--codigo" in sys.argv:
    i = sys.argv.index("--codigo")
    codigo = Path(sys.argv[i + 1]).resolve()
    del sys.argv[i:i + 2]
sys.path.insert(0, str(codigo))

from miniloja.calculo import calcular_total  # noqa: E402
from miniloja.estoque import Estoque  # noqa: E402


class TestAV13(unittest.TestCase):
    # Mutantes sobreviventes
    def test_m1_natal_vinte_por_cento(self):
        # mata "NATAL: 20% -> 21%": 100 x 0,80 = 80,00; + 29,90 = 109,90; x 1,08 = 118,692 -> 118,69
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        try:
            self.assertEqual(calcular_total([{"preco": 100.0, "qtd": 1}], "NATAL", "XX"), 118.69)
        finally:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)

    def test_m2_reservar_exatamente_o_saldo(self):
        # mata "limite exato do estoque" (< vira <=): pedir o saldo inteiro deve funcionar
        e = Estoque({"BOLA-01": 3})
        self.assertTrue(e.reservar("BOLA-01", 3, "p1"))
        self.assertEqual(e.saldo("BOLA-01"), 0)

    # Casos derivados do contrato (R1)
    def test_c1_fronteira_200_frete_gratis(self):
        # R1.3: subtotal 200,00 >= 200 -> frete 0; R1.4: 200,00 x 1,05 = 210,00
        self.assertEqual(calcular_total([{"preco": 100.0, "qtd": 2}], None, "PE"), 210.00)

    def test_c2_desconto_antes_do_frete_e_meio_para_cima(self):
        # R1.6: 220 x 0,90 = 198,00 (< 200, paga frete); + 12,90 = 210,90; x 1,05 = 221,445
        # R1.5: meio para cima -> 221,45
        self.assertEqual(calcular_total([{"preco": 220.0, "qtd": 1}], "PROMO10", "PE"), 221.45)

    def test_c3_frete_e_taxa_rj(self):
        # R1.3/R1.4: (40,00 + 21,50) x 1,06 = 65,19 (também mata o mutante "frete RJ")
        self.assertEqual(calcular_total([{"preco": 40.0, "qtd": 1}], None, "RJ"), 65.19)


if __name__ == "__main__":
    unittest.main(verbosity=2)
