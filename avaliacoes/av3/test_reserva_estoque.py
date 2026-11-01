"""Regressões de R2.2 com estado real; executar da raiz com unittest."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "caso"))

from miniloja import handlers
from miniloja.estoque import Estoque
from miniloja.pagamentos import GatewayFake
from miniloja.pedidos import PedidoService
from miniloja.repositorio import RepositorioPedidos


def item(sku, qtd):
    return {"sku": sku, "qtd": qtd, "preco": 50.0}


class TestReservaEstoque(unittest.TestCase):
    def test_falha_preserva_estado_e_nao_cobra_nem_salva(self):
        cenarios = {
            "primeiro": [item("X", 1), item("A", 1)],
            "intermediario": [item("A", 1), item("X", 1), item("B", 1)],
            "ultimo": [item("A", 1), item("B", 1), item("X", 1)],
            "sku_repetido": [item("A", 2), item("A", 3)],
        }
        for nome, itens in cenarios.items():
            with self.subTest(nome=nome):
                estoque = Estoque({"A": 6, "B": 4})
                # Reservas anteriores de outro usuário e do mesmo usuário.
                estoque.reservar("B", 1, "tmp-9")
                estoque.reservar("A", 2, "tmp-1")
                repo, gateway = RepositorioPedidos(), GatewayFake()
                service = PedidoService(repo, estoque, gateway)
                saldos, reservas = dict(estoque.saldos), dict(estoque.reservas)
                with patch.object(handlers, "_service", service):
                    status, corpo = handlers.post_pedidos(1, {"itens": itens})
                self.assertEqual(status, 409)
                self.assertEqual(corpo["sku"], "A" if nome == "sku_repetido" else "X")
                self.assertEqual(estoque.saldos, saldos)
                self.assertEqual(estoque.reservas, reservas)
                self.assertEqual(gateway.cobrancas, [])
                self.assertEqual(repo.todos(), [])

    def test_lote_valido_com_sku_repetido_cria_pedido(self):
        estoque = Estoque({"A": 5, "B": 2})
        repo, gateway = RepositorioPedidos(), GatewayFake()
        service = PedidoService(repo, estoque, gateway)
        with patch.object(handlers, "_service", service):
            status, pedido = handlers.post_pedidos(
                1, {"itens": [item("A", 2), item("A", 3), item("B", 1)]}
            )
        self.assertEqual(status, 201)
        self.assertEqual(pedido["status"], "pago")
        self.assertEqual(estoque.saldos, {"A": 0, "B": 1})
        self.assertEqual(repo.todos(), [pedido])
        self.assertEqual(gateway.cobrancas, [(pedido["total"], "tok_ok")])


if __name__ == "__main__":
    unittest.main(verbosity=2)
