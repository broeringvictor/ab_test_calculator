import math # <-- CORREÇÃO: Importa o módulo de matemática

class Variation:
    """ Repesenta uma entidade de variação em um teste A/B. """
    def __init__(self,
                 variation_a_visitors: int,
                 variation_b_visitors: int,
                 conversions_a: int,
                 conversions_b: int,
                 tail_numbers: int,
                 confidence_level: float,
                 estimated_uplift: float) -> None:

        self.variation_a_visitors = variation_a_visitors
        self.variation_b_visitors = variation_b_visitors
        self.conversions_a = conversions_a
        self.conversions_b = conversions_b
        self.tail_numbers = tail_numbers
        self.confidence_level = confidence_level / 100
        self.estimated_uplift = estimated_uplift / 100
        self.conversion_rate_a = (conversions_a / variation_a_visitors) if variation_a_visitors != 0 else 0.0
        self.conversion_rate_b = (conversions_b / variation_b_visitors) if variation_b_visitors != 0 else 0.0
        self.obs_power_on = True if self.conversion_rate_b > self.conversion_rate_a else False

        self.default_error_a = self.calculate_default_error(self.conversion_rate_a, self.variation_a_visitors)
        self.default_error_b = self.calculate_default_error(self.conversion_rate_b, self.variation_b_visitors)

    def calculate_default_error(self, conversion_rate: float, visitors: int) -> float:
        """ Calcula o ERRO PADRÃO para uma variação. """
        if visitors == 0:
            return 0.0
        # A fórmula da variância de uma proporção
        variance = (conversion_rate * (1 - conversion_rate)) / visitors
        # CORREÇÃO: Usa math.sqrt para calcular a raiz quadrada (Erro Padrão)
        return math.sqrt(variance)