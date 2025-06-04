from ..entities.variation import Variation
from domain.entities import variation

class ABStatisticalValidator:
    def __init__(self, variation: Variation) -> None:
        self.variation = variation
        significance_alpha = (1 - self.variation.confidence_level)
        self.standard_error_difference = ( self.variation.

    def get_statistical_metrics(self):
        """
        Verifica a validação estatística da variação A/B.
        """
        z_score = 



        return {
       
        }
    
    def z_score_calculation(self):
        """
        Calcula o z-score para a variação A/B.
        """
        if self.variation.variation_a_visitors == 0 or self.variation.variation_b_visitors == 0:
            return 0.0
                
        pooled_prob = (self.variation.conversions_a + self.variation.conversions_b) / (n_a + n_b)

        z_score = (self.variation.conversion_rate_b - self.variation.conversion_rate_a) 

                  ((pooled_prob * (1 - pooled_prob) * (1 / self.variation.variation_a_visitors + 1 / self.variation.variation_b_visitors)) ** 0.5)

        return z_score

    def calculate_standard_error_difference:
        """
        Calcula o erro padrão da diferença entre as taxas de conversão.
        """
        

        
        return standard_error_difference    
