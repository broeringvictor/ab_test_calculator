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

        return {
            "standard_error_difference": std_err_diff,
            "z_score": z_score,
            "z_critical": z_critical
        }

    def _calculate_standard_error_difference(self) -> float:
        """ 
        Calcula o erro padrão da diferença.
        Esta função agora RESPEITA a entidade Variation, sabendo que
        'default_error_a' e 'default_error_b' são as variâncias.
        """
        # Soma as variâncias de cada grupo
        variance_difference = self.variation.default_error_a**2 + self.variation.default_error_b**2

        # Tira a raiz quadrada para obter o erro padrão da diferença
        return math.sqrt(variance_difference)

    def _calculate_z_score(self, std_err_diff: float) -> float:
        """
        Calcula o z-score usando os dados da entidade Variation.
        """
        if std_err_diff == 0:
            return 0.0
        return (self.variation.conversion_rate_b - self.variation.conversion_rate_a) / std_err_diff

    def _calculate_z_table_value_critical(self) -> float:
        """
        Calcula o valor crítico Z usando a SUA fórmula original.
        """
        # Usando a fórmula exata que você definiu na sua classe original
        # que depende de 'tail_numbers'
        prob = (self.variation.tail_numbers - self.variation.confidence_level) / self.variation.tail_numbers
        return float(norm.ppf(prob))