from xmlrpc.client import Boolean


class Variation:
    def __init__(self,
                 variation_a_visitors: int,
                 variation_b_visitors: int,
                 conversions_a: int,
                 conversions_b: int,
                 tail_numbers: int,
                 estimated_uplift: float) -> None:

        self.variation_a_visitors = variation_a_visitors
        self.variation_b_visitors = variation_b_visitors
        self.conversions_a = conversions_a
        self.conversions_b = conversions_b
        self.tail_numbers = tail_numbers
        self.estimated_uplift = estimated_uplift
        self.conversion_rate_a = (conversions_a / variation_a_visitors) if variation_a_visitors != 0 else 0.0
        self.conversion_rate_b = (conversions_b / variation_b_visitors) if variation_b_visitors != 0 else 0.0
        self.obs_power = self.calculate_obs_power()

    def calculate_obs_power(self) -> float:
        """
        Calcula o poder da observação com base nos números de cauda e nas taxas de conversão.
        """
        if self.tail_numbers == 0:
            return 0.0
        return Boolean(self.conversion_rate_b > self.conversion_rate_a)
    
