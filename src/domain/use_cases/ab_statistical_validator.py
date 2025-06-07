import re

from scipy.stats import norm
from typing import Dict, Any
import math

from domain.entities.variation import Variation

class ABStatisticalValidator:
    def __init__(self, variation: Variation) -> None:
        self.variation = variation

    def get_statistical_results(self) -> Dict[str, Any]:
        """
        Orquestra os cálculos e retorna um dicionário com todas as métricas.
        """
        
        std_err_diff = self._calculate_standard_error_difference()
        z_score = self._calculate_z_score(std_err_diff)
        z_critical = self._calculate_z_table_value_critical()
        p_value = self._calculate_p_value(z_score)
        conversion_rate_uplift = self._calculate_conversion_rate_uplift()
        observed_test_power = self._calculate_observed_test_power(z_critical)


        return {
            "standard_error_difference": std_err_diff,
            "z_score": z_score,
            "z_critical": z_critical,
            "p_value": p_value,
            "conversion_rate_uplift": conversion_rate_uplift,
            "observed_test_power": observed_test_power,

        }

    def _calculate_standard_error_difference(self) -> float:
        """ 
        Calcula o erro padrão da diferença.

        """
        # Soma as variâncias de cada grupo e faz a raiz quadrada
        variance_difference = self.variation.default_error_a**2 + self.variation.default_error_b**2

        # Tira a raiz quadrada para obter o erro padrão da diferença --> Não entendi o fato do Autor da tabela elevar ao quadrado antes de tirar a raiz quadrada
        return math.sqrt(variance_difference)

    def _calculate_z_score(self, std_err_diff: float) -> float:
        """
        Calcula o z-score usando os dados da entidade Variation.
        """
        if std_err_diff == 0:
            return 0.0 # Evita divisão por zero
        return (self.variation.conversion_rate_b - self.variation.conversion_rate_a) / std_err_diff

    def _calculate_z_table_value_critical(self) -> float:
        """
        Calcula o valor crítico Z com a biblioteca scipy. 
        """

        prob = (self.variation.tail_numbers - self.variation.confidence_level) / self.variation.tail_numbers
        return float(norm.ppf(prob))
    
    def _calculate_p_value(self, z_score: float) -> float:
        """
        Calcula o valor p a partir do z-score.
        """
        tail = int(self.variation.tail_numbers)
        if tail == 1:
            p_value = 1 - norm.cdf(z_score)
            return float(p_value)
        elif tail == 2:
            p_value = 1 - norm.cdf(abs(z_score))
            return float(p_value)
        else:
            raise ValueError("Número de caudas deve ser 1 ou 2.")
        
    def _calculate_conversion_rate_uplift(self) -> float:
        """
        Calcula o aumento percentual da taxa de conversão.
        """
        if self.variation.conversion_rate_a == 0:
            return float('inf')
        
        uplift = (self.variation.conversion_rate_b - self.variation.conversion_rate_a) / self.variation.conversion_rate_a
        return float(uplift)

    def _calculate_observed_test_power(self, z_critical: float) -> float:
        """
        Calcula o Poder do Teste Observado (Power) conforme a fórmula da planilha.
        
        Fórmula Excel:
        =IF(D15=TRUE(),1-NORM.DIST(((D7+D8*H4-E7)/E8),0,1,TRUE()),1-NORM.DIST(((E7+E8*H4-D7)/D8),0,1,TRUE()))

        """

        conv_a = self.variation.conversions_a
        rate_a = self.variation.conversion_rate_a
        conv_b = self.variation.conversions_b
        rate_b = self.variation.conversion_rate_b
        
        # Condição baseada na célula D15 (OBS Power)
        if self.variation.obs_power_on:
            # Parte VERDADEIRA da fórmula: 1-NORM.DIST(((D7+D8*H4-E7)/E8),0,1,TRUE())
            if rate_b == 0:
                return 0.0
            
            numerador = conv_a + (rate_a * z_critical) - conv_b
            denominador = rate_b
            x = numerador / denominador
            # norm.sf(x) é a Survival Function, equivalente a 1 - norm.cdf(x)
            return float(norm.sf(x))
        else:
            # Parte FALSA da fórmula: 1-NORM.DIST(((E7+E8*H4-D7)/D8),0,1,TRUE())
            if rate_a == 0:
                return float(0.0)

            numerador = conv_b + (rate_b * z_critical) - conv_a
            denominador = rate_a
            y = numerador / denominador
            return float(norm.sf(y))

