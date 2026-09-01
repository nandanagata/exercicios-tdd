from decimal import Decimal

from src.extrato import Conta


def test_deposito_deve_aumentar_saldo():
    conta = Conta()

    transacao = conta.depositar(Decimal("100.00"))

    assert conta.saldo == Decimal("100.00")
    assert transacao.valor == Decimal("100.00")
    assert transacao.tipo == "CREDITO"
    assert transacao.status == "CONCLUIDO"
    assert len(conta.transacoes) == 1