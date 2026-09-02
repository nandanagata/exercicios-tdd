from decimal import Decimal


class ServicoCotacaoIndisponivelError(Exception):
    """Exceção para indisponibilidade do serviço de cotação."""
    pass


class ConversorMoedas:

    SPREAD = Decimal("0.015")

    def __init__(self, cotacao_api):
        self.cotacao_api = cotacao_api

    def converter(
        self,
        moeda_origem: str,
        moeda_destino: str,
        valor
    ) -> Decimal:

        valor = Decimal(str(valor))

        if valor <= 0:
            raise ValueError(
                "O valor deve ser maior que zero."
            )

        try:
            taxa = self.cotacao_api.obter_taxa(
                moeda_origem,
                moeda_destino
            )

        except Exception as erro:
            raise ServicoCotacaoIndisponivelError(
                "Serviço de cotação indisponível."
            ) from erro

        taxa = Decimal(str(taxa))

        valor_convertido = valor * taxa

        valor_com_spread = (
            valor_convertido
            * (Decimal("1.00") + self.SPREAD)
        )

        return valor_com_spread.quantize(
            Decimal("0.01")
        )