from decimal import Decimal

import pytest

from src.extrato import Conta, EstornoInvalidoError, SaldoInsuficienteError


def test_deposito_deve_aumentar_saldo():
    conta = Conta()

    transacao = conta.depositar(Decimal("100.00"))

    assert conta.saldo == Decimal("100.00")
    assert transacao.valor == Decimal("100.00")
    assert transacao.tipo == "CREDITO"
    assert transacao.status == "CONCLUIDO"
    assert len(conta.transacoes) == 1


def test_saque_deve_diminuir_saldo():
    conta = Conta()
    conta.depositar(Decimal("100.00"))

    transacao = conta.sacar(Decimal("40.00"))

    assert conta.saldo == Decimal("60.00")
    assert transacao.valor == Decimal("40.00")
    assert transacao.tipo == "DEBITO"
    assert transacao.status == "CONCLUIDO"
    assert len(conta.transacoes) == 2


def test_saque_com_saldo_insuficiente_deve_lancar_erro():
    conta = Conta()
    conta.depositar(Decimal("50.00"))

    with pytest.raises(SaldoInsuficienteError):
        conta.sacar(Decimal("80.00"))

    assert conta.saldo == Decimal("50.00")
    assert len(conta.transacoes) == 1


def test_estorno_de_deposito_deve_recalcular_saldo():
    conta = Conta()
    deposito = conta.depositar(Decimal("100.00"))

    conta.estornar(deposito.id)

    assert deposito.status == "ESTORNADO"
    assert conta.saldo == Decimal("0.00")


def test_estorno_de_saque_deve_devolver_valor_ao_saldo():
    conta = Conta()
    conta.depositar(Decimal("100.00"))
    saque = conta.sacar(Decimal("30.00"))

    conta.estornar(saque.id)

    assert saque.status == "ESTORNADO"
    assert conta.saldo == Decimal("100.00")


def test_nao_deve_estornar_mesma_transacao_duas_vezes():
    conta = Conta()
    deposito = conta.depositar(Decimal("100.00"))
    conta.estornar(deposito.id)

    with pytest.raises(EstornoInvalidoError):
        conta.estornar(deposito.id)

    assert deposito.status == "ESTORNADO"
    assert conta.saldo == Decimal("0.00")


def test_estorno_de_transacao_inexistente_deve_lancar_erro():
    conta = Conta()

    with pytest.raises(EstornoInvalidoError):
        conta.estornar("id-inexistente")

    assert conta.saldo == Decimal("0.00")
    assert len(conta.transacoes) == 0


def test_sequencia_complexa_de_operacoes_e_estornos():
    conta = Conta()

    primeiro_deposito = conta.depositar(Decimal("1000.00"))
    primeiro_saque = conta.sacar(Decimal("200.00"))
    segundo_deposito = conta.depositar(Decimal("300.00"))
    segundo_saque = conta.sacar(Decimal("100.00"))

    conta.estornar(segundo_deposito.id)
    conta.estornar(segundo_saque.id)

    assert conta.saldo == Decimal("800.00")
    assert len(conta.transacoes) == 4

    assert primeiro_deposito.status == "CONCLUIDO"
    assert primeiro_saque.status == "CONCLUIDO"
    assert segundo_deposito.status == "ESTORNADO"
    assert segundo_saque.status == "ESTORNADO"


def test_historico_deve_preservar_ordem_das_transacoes():
    conta = Conta()

    deposito = conta.depositar(Decimal("200.00"))
    saque = conta.sacar(Decimal("50.00"))

    assert conta.transacoes[0] == deposito
    assert conta.transacoes[1] == saque