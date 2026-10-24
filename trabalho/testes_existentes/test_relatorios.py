import unittest

from miniloja.relatorios import resumo_vendas, simular_desconto


class TestRelatorios(unittest.TestCase):
    def test_resumo_vendas(self):
        r = resumo_vendas([{"total": 10.0}, {"total": 20.0}])
        self.assertEqual(r["quantidade"], 2)
        self.assertEqual(r["total"], 30.0)

    def test_simular_desconto(self):
        self.assertTrue(simular_desconto(100.0, "PROMO10").startswith("R$"))
