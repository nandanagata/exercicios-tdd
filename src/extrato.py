from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4


@dataclass
class Transacao:
    id: str
    valor: Decimal
    tipo: str
    status: str = "CONCLUIDO"


class Conta:
    def __init__(self):
        self.transacoes: list[Transacao] = []

    @property
    def saldo(self) -> Decimal:
        total = Decimal("0.00")

        for transacao in self.transacoes:
            if transacao.status != "CONCLUIDO":
                continue

            if transacao.tipo == "CREDITO":
                total += transacao.valor
            else:
                total -= transacao.valor

        return total

    def depositar(self, valor: Decimal) -> Transacao:
        transacao = Transacao(
            id=str(uuid4()),
            valor=valor,
            tipo="CREDITO",
        )

        self.transacoes.append(transacao)
        return transacao