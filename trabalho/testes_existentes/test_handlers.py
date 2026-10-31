import unittest

from miniloja import handlers


class TestHandlers(unittest.TestCase):
    def test_criar_e_obter_pedido(self):
        status, pedido = handlers.post_pedidos(
            10, {"itens": [{"sku": "BOLA-01", "preco": 50.0, "qtd": 2}], "uf": "PE"}
        )
        self.assertEqual(status, 201)
        self.assertEqual(pedido["total"], 118.55)
        status2, corpo = handlers.get_pedido(10, pedido["id"])
        self.assertEqual(status2, 200)
        self.assertEqual(corpo["id"], pedido["id"])

    def test_pedido_inexistente(self):
        status, _ = handlers.get_pedido(10, 9999)
        self.assertEqual(status, 404)

    def test_estoque_insuficiente_retorna_409(self):
        status, corpo = handlers.post_pedidos(
            11, {"itens": [{"sku": "CHUTEIRA-42", "preco": 300.0, "qtd": 999}]}
        )
        self.assertEqual(status, 409)
        self.assertEqual(corpo["sku"], "CHUTEIRA-42")
