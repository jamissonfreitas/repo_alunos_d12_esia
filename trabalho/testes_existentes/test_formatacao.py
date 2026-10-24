import unittest

from miniloja.formatacao import formatar_moeda


class TestFormatacao(unittest.TestCase):
    def test_formatar_moeda_milhar(self):
        self.assertEqual(formatar_moeda(1234.5), "R$ 1.234,50")

    def test_formatar_moeda_nao_quebra(self):
        formatar_moeda(0)
        formatar_moeda(99.999)
