class AnaliseCredito:

    RENDA_MINIMA = 1500.00
    PERCENTUAL_LIMITE = 0.30
    SCORE_BONUS = 800
    BONUS = 0.50

    def calcular_limite(
        self,
        renda_mensal: float,
        possui_restricao: bool,
        score_externo: int
    ) -> float:

        if renda_mensal < self.RENDA_MINIMA:
            return 0.0

        if possui_restricao:
            return 0.0

        limite_base = renda_mensal * self.PERCENTUAL_LIMITE

        if score_externo > self.SCORE_BONUS:
            limite_base *= (1 + self.BONUS)

        return round(limite_base, 2)