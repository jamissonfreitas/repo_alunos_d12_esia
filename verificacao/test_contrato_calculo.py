#!/usr/bin/env python3
"""Testes de calcular_total derivados do CONTRATO (caso/regras.md, R1), não do código.

Cada esperado foi calculado à mão a partir do contrato; a conta está no comentário.
Nenhum esperado foi copiado da saída do código.

  python -B verificacao/test_contrato_calculo.py --codigo trabalho
  python -B verificacao/test_contrato_calculo.py --codigo caso      # mesmo resultado no original

Escolha das entradas: fora da terceira casa 5 (para o teste não depender do
arredondamento), exceto nos casos que testam justamente o arredondamento.
As divergências conhecidas D1 e D2 (ADR-001) ficam em TestDivergenciasConhecidas,
marcadas com expectedFailure: falham hoje, e se alguém corrigir o código o
resultado vira "unexpected success" e a execução termina com código 1, obrigando
a atualizar o ADR e o marcador.
"""
import argparse
import os
import sys
import unittest


def item(preco, qtd=1):
    return {"preco": preco, "qtd": qtd}


class Base(unittest.TestCase):
    def setUp(self):
        self._flag = os.environ.pop("MINILOJA_PROMO_NATAL", None)

    def tearDown(self):
        os.environ.pop("MINILOJA_PROMO_NATAL", None)
        if self._flag is not None:
            os.environ["MINILOJA_PROMO_NATAL"] = self._flag


class TestR1Subtotal(Base):
    def test_r1_1_soma_preco_vezes_quantidade_de_varios_itens(self):
        # 12,50x2 + 5,00x3 = 40,00; RJ: (40,00 + 21,50) x 1,06 = 65,19
        self.assertEqual(calcular_total([item(12.5, 2), item(5.0, 3)], None, "RJ"), 65.19)

    def test_r1_1_item_com_quantidade_zero_nao_soma(self):
        # 10,00x0 = 0; RJ: (0 + 21,50) x 1,06 = 22,79
        self.assertEqual(calcular_total([item(10.0, 0)], None, "RJ"), 22.79)


class TestR1Desconto(Base):
    def test_r1_2_promo10_desconta_dez_por_cento(self):
        # 80,00 x 0,90 = 72,00; SP: (72,00 + 19,90) x 1,07 = 98,333 -> 98,33
        self.assertEqual(calcular_total([item(80.0)], "PROMO10", "SP"), 98.33)

    def test_r1_2_vip15_desconta_quinze_por_cento(self):
        # 30,00 x 0,85 = 25,50; RJ: (25,50 + 21,50) x 1,06 = 49,82
        self.assertEqual(calcular_total([item(30.0)], "VIP15", "RJ"), 49.82)

    def test_r1_2_natal_com_campanha_ativa_desconta_vinte_por_cento(self):
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        # 50,00 x 0,80 = 40,00; SP: (40,00 + 19,90) x 1,07 = 64,093 -> 64,09
        self.assertEqual(calcular_total([item(50.0)], "NATAL", "SP"), 64.09)

    def test_r1_2_natal_sem_campanha_nao_desconta(self):
        # flag ausente: 50,00; SP: (50,00 + 19,90) x 1,07 = 74,793 -> 74,79
        self.assertEqual(calcular_total([item(50.0)], "NATAL", "SP"), 74.79)

    def test_r1_2_natal_com_flag_diferente_de_1_nao_desconta(self):
        os.environ["MINILOJA_PROMO_NATAL"] = "0"
        self.assertEqual(calcular_total([item(50.0)], "NATAL", "SP"), 74.79)

    def test_r1_2_cupom_desconhecido_e_ignorado_sem_erro(self):
        # 70,00; RJ: (70,00 + 21,50) x 1,06 = 96,99 (o mesmo valor sem cupom)
        self.assertEqual(calcular_total([item(70.0)], "CUPOMFALSO", "RJ"), 96.99)

    def test_r1_2_fretegratis_nao_altera_o_valor_dos_itens(self):
        # 100,00 sem desconto, frete 0; SP: 100,00 x 1,07 = 107,00
        self.assertEqual(calcular_total([item(100.0)], "FRETEGRATIS", "SP"), 107.0)


class TestR1FretePorUF(Base):
    # Mesmas entradas para isolar frete + taxa de cada UF.
    def test_r1_3_e_r1_4_pe(self):
        # (33,33 + 12,90) x 1,05 = 48,5415 -> 48,54 (também mata arredondamento em 3 casas)
        self.assertEqual(calcular_total([item(33.33)], None, "PE"), 48.54)

    def test_r1_3_e_r1_4_sp(self):
        # 45,00x2 = 90,00; (90,00 + 19,90) x 1,07 = 117,593 -> 117,59
        self.assertEqual(calcular_total([item(45.0, 2)], None, "SP"), 117.59)

    def test_r1_3_e_r1_4_rj(self):
        # (70,00 + 21,50) x 1,06 = 96,99
        self.assertEqual(calcular_total([item(70.0)], None, "RJ"), 96.99)

    def test_r1_3_e_r1_4_demais_ufs(self):
        # (60,00 + 29,90) x 1,08 = 97,092 -> 97,09, para qualquer UF fora da tabela
        for uf in ("BA", "XX"):
            with self.subTest(uf=uf):
                self.assertEqual(calcular_total([item(60.0)], None, uf), 97.09)


class TestR1FreteGratis(Base):
    def test_r1_3_logo_abaixo_de_200_paga_frete(self):
        # (199,99 + 12,90) x 1,05 = 223,5345 -> 223,53
        self.assertEqual(calcular_total([item(199.99)], None, "PE"), 223.53)

    def test_r1_3_logo_acima_de_200_nao_paga_frete(self):
        # 200,01 x 1,05 = 210,0105 -> 210,01
        self.assertEqual(calcular_total([item(200.01)], None, "PE"), 210.01)

    def test_r1_3_bem_acima_de_200_nao_paga_frete(self):
        # 250,00 x 1,07 = 267,50 (mata limite 200 -> 300)
        self.assertEqual(calcular_total([item(250.0)], None, "SP"), 267.5)

    def test_r1_3_fretegratis_abaixo_de_200_zera_frete(self):
        # 40,00; RJ: 40,00 x 1,06 = 42,40
        self.assertEqual(calcular_total([item(40.0)], "FRETEGRATIS", "RJ"), 42.4)


class TestR1Ordem(Base):
    def test_r1_6_desconto_antes_do_frete_tira_do_frete_gratis(self):
        # 220,00 x 0,90 = 198,00 (< 200, paga frete); (198,00 + 19,90) x 1,07 = 233,153 -> 233,15
        # Se o frete olhasse o subtotal SEM desconto (220 > 200): 198,00 x 1,07 = 211,86.
        self.assertEqual(calcular_total([item(220.0)], "PROMO10", "SP"), 233.15)

    def test_r1_6_desconto_antes_do_frete_varios_itens(self):
        # 120,00 + 40,00x2 = 200,00; x 0,85 = 170,00; (170,00 + 19,90) x 1,07 = 203,193 -> 203,19
        self.assertEqual(calcular_total([item(120.0), item(40.0, 2)], "VIP15", "SP"), 203.19)

    def test_r1_6_desconto_que_ainda_fica_acima_de_200_mantem_frete_gratis(self):
        # 222,23 x 0,90 = 200,007 (> 200); 200,007 x 1,05 = 210,00735 -> 210,01
        self.assertEqual(calcular_total([item(222.23)], "PROMO10", "PE"), 210.01)

    def test_r1_4_taxa_incide_sobre_o_frete_tambem(self):
        # (70,00 + 21,50) x 1,06 = 96,99. Se a taxa ignorasse o frete: 70 x 1,06 + 21,50 = 95,70.
        self.assertEqual(calcular_total([item(70.0)], None, "RJ"), 96.99)
        self.assertNotEqual(calcular_total([item(70.0)], None, "RJ"), 95.7)


class TestDivergenciasConhecidas(Base):
    """Contrato x código hoje. Ver docs/ADR-001. NÃO trocar o esperado pelo valor do código."""

    @unittest.expectedFailure
    def test_d1_r1_3_subtotal_exatamente_200_tem_frete_gratis(self):
        # Contrato: >= 200 é grátis. 200,00 x 1,05 = 210,00. Código hoje: 223,55.
        self.assertEqual(calcular_total([item(100.0, 2)], None, "PE"), 210.0)

    @unittest.expectedFailure
    def test_d2_r1_5_arredonda_meio_para_cima(self):
        # Contrato: 2x1,00 = 2,00; (2,00 + 12,90) x 1,05 = 15,645 -> 15,65. Código hoje: 15,64.
        self.assertEqual(calcular_total([item(1.0, 2)], None, "PE"), 15.65)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--codigo", default="trabalho", help="pasta que contém o pacote miniloja")
    p.add_argument("-x", "--failfast", action="store_true")
    a, resto = p.parse_known_args()
    sys.path.insert(0, os.path.abspath(a.codigo))
    global calcular_total
    from miniloja.calculo import calcular_total  # noqa: E402
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    r = unittest.TextTestRunner(verbosity=1, failfast=a.failfast).run(suite)
    return 0 if r.wasSuccessful() else 1


calcular_total = None
if __name__ == "__main__":
    sys.exit(main())