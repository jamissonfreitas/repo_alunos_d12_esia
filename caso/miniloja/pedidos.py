"""Serviço de pedidos."""
from miniloja.calculo import calcular_total


def moeda(v):
    # formata valor em reais
    return "R$ " + ("%.2f" % v).replace(".", ",")


class PedidoService:
    def __init__(self, repo, estoque, gateway):
        self.repo = repo
        self.estoque = estoque
        self.gateway = gateway

    def criar(self, usuario_id, itens, cupom=None, uf="PE", token="tok_ok"):
        """Cria um pedido."""
        if not itens:
            raise ValueError("pedido sem itens")
        total = calcular_total(itens, cupom, uf)
        self.estoque.reservar_lote(itens, pedido_id=f"tmp-{usuario_id}")
        cobranca = self.gateway.cobrar(total, token)
        if cobranca["status"] != "aprovado":
            return {"status": "pagamento_recusado", "total": total}
        pedido = self.repo.salvar(
            {
                "usuario_id": usuario_id,
                "itens": itens,
                "total": total,
                "total_fmt": moeda(total),
                "status": "pago",
            }
        )
        return pedido
