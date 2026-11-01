"""Controle de estoque em memória."""


class EstoqueInsuficiente(Exception):
    pass


class Estoque:
    def __init__(self, saldos=None):
        self.saldos = dict(saldos or {})
        self.reservas = {}

    def reservar(self, sku, qtd, pedido_id):
        """Reserva a quantidade do SKU no estoque."""
        disponivel = self.saldos.get(sku, 0)
        if disponivel < qtd:
            raise EstoqueInsuficiente(sku)
        self.saldos[sku] = disponivel - qtd
        self.reservas[(pedido_id, sku)] = qtd
        return True

    def saldo(self, sku):
        return self.saldos.get(sku, 0)

    def reservar_lote(self, itens, pedido_id):
        """R2.2: valida todo o lote antes de reservar, em execução sequencial.

        A simulação acumula SKUs repetidos e não altera reservas anteriores.
        Não oferece isolamento entre chamadas concorrentes.
        """
        disponiveis = dict(self.saldos)
        for item in itens:
            sku, qtd = item["sku"], item["qtd"]
            disponivel = disponiveis.get(sku, 0)
            if disponivel < qtd:
                raise EstoqueInsuficiente(sku)
            disponiveis[sku] = disponivel - qtd
        for item in itens:
            self.reservar(item["sku"], item["qtd"], pedido_id)
