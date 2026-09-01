from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4


class SaldoInsuficienteError(Exception):
    pass

class EstornoInvalidoError(Exception):
    pass

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

    def sacar(self, valor: Decimal) -> Transacao:
        if valor > self.saldo:
            raise SaldoInsuficienteError("Saldo insuficiente para o saque.")

        transacao = Transacao(
            id=str(uuid4()),
            valor=valor,
            tipo="DEBITO",
        )

        self.transacoes.append(transacao)
        return transacao

    def estornar(self, transacao_id: str) -> Transacao:
        transacao = self._buscar_transacao(transacao_id)

        if transacao is None:
            raise EstornoInvalidoError("Transação não encontrada.")

        if transacao.status != "CONCLUIDO":
            raise EstornoInvalidoError("A transação já foi estornada.")

        transacao.status = "ESTORNADO"
        return transacao

    def _buscar_transacao(self, transacao_id: str) -> Transacao | None:
        for transacao in self.transacoes:
            if transacao.id == transacao_id:
                return transacao

        return None