from scipy.stats import norm, chisquare
from typing import Dict, Any
import math
from datetime import date, timedelta
import numpy as np
from domain.entities.ab_tester import ABTester
from domain.entities.variation import Variation

class ABStatisticalValidator:
    def __init__(self, variation: Variation, tester: ABTester) -> None:
        self.variation = variation
        self.tester = tester

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
        current_confidence = float(1.00 - p_value)

        control_upper_bound = self._calculate_upper_bound(
            conversion_rate=self.variation.conversion_rate_a,
            standard_error=self.variation.default_error_a,
            z_critical=z_critical
        )
        control_lower_bound = self._calculate_lower_bound(
            conversion_rate=self.variation.conversion_rate_a,
            standard_error=self.variation.default_error_a,
            z_critical=z_critical
        )
       
        variation_upper_bound = self._calculate_upper_bound(
            conversion_rate=self.variation.conversion_rate_b,
            standard_error=self.variation.default_error_b,
            z_critical=z_critical
        )
        variation_lower_bound = self._calculate_lower_bound(
            conversion_rate=self.variation.conversion_rate_b,
            standard_error=self.variation.default_error_b,
            z_critical=z_critical
        )

        srm_results = self.check_sample_ratio_mismatch()
        temporal_validation_results = self.get_temporal_validation_results()
        planning_results = self.get_test_planning_metrics(mde=self.variation.estimated_uplift)

        # --- Retornar todos os resultados ---
        return {
            "standard_error_difference": std_err_diff,
            "z_score": z_score,
            "z_critical": z_critical,
            "p_value": p_value,
            "conversion_rate_uplift": conversion_rate_uplift,
            "observed_test_power": observed_test_power,
            "current_confidence": current_confidence,
            "control_upper_bound": control_upper_bound,
            "control_lower_bound": control_lower_bound,
            "variation_upper_bound": variation_upper_bound,
            "variation_lower_bound": variation_lower_bound,
            "srm_results": srm_results,
            "temporal_validation_results": temporal_validation_results,
            "planning_results": planning_results  # Combina o dicionário de planejamento ao resultado final
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
            # Para testes bicaudais, o p-value é 2 * (área na cauda)
            p_value = 2 * (1 - norm.cdf(abs(z_score)))
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
            # --- CORREÇÃO: Carregar as variáveis corretas ---
            # Em vez de 'conversions', usamos as taxas (rates) e erros padrão (standard errors)
            rate_a = self.variation.conversion_rate_a
            std_err_a = self.variation.default_error_a
            rate_b = self.variation.conversion_rate_b
            std_err_b = self.variation.default_error_b
            
            # A lógica da planilha espera um Z-Crítico positivo. Como o seu código
            # calcula um valor negativo, usamos o valor absoluto (abs) para corrigir.
            z_crit_abs = abs(z_critical)

            # Condição baseada na célula D15 (OBS Power)
            if self.variation.obs_power_on:
                # Parte VERDADEIRA da fórmula: (D7 + D8*H4 - E7) / E8
                # Onde D7=rate_a, D8=std_err_a, H4=z_critical, E7=rate_b, E8=std_err_b
                if std_err_b == 0:
                    return 0.0
                
                numerador = rate_a + (std_err_a * z_crit_abs) - rate_b
                denominador = std_err_b
                x = numerador / denominador
                return float(norm.sf(x)) # norm.sf(x) é 1 - norm.cdf(x)
            else:
                # Parte FALSA da fórmula: (E7 + E8*H4 - D7) / D8
                if std_err_a == 0:
                    return 0.0

                numerador = rate_b + (std_err_b * z_crit_abs) - rate_a
                denominador = std_err_a
                y = numerador / denominador
                return float(norm.sf(y))
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

    def _calculate_upper_bound(self, conversion_rate: float, standard_error: float, z_critical: float) -> float:
        """
        Calculates the generic upper confidence interval bound for any group.
        """
        # CORREÇÃO: Usamos abs(z_critical) para garantir que o cálculo seja sempre uma SOMA,
        # independentemente do sinal do Z-Crítico de entrada.
        upper_bound = conversion_rate + (standard_error * abs(z_critical))
        return float(upper_bound)

    def _calculate_lower_bound(self, conversion_rate: float, standard_error: float, z_critical: float) -> float:
        """
        Calculates the generic lower confidence interval bound for any group.
        """
    

        # CORREÇÃO: Usamos abs(z_critical) para garantir que o cálculo seja sempre uma SUBTRAÇÃO.
        lower_bound = conversion_rate - (standard_error * abs(z_critical))
        return float(lower_bound)
        """
        Calculates the generic lower confidence interval bound for any group.

        Args:
            conversion_rate: The conversion rate of the group (e.g., control's or variation's).
            standard_error: The standard error of the group.
            z_critical: The critical Z-score for the desired confidence level.

        Returns:
            The lower bound of the confidence interval.
        """
        lower_bound = conversion_rate - (standard_error * z_critical)
        return float(lower_bound)
    
    def check_sample_ratio_mismatch(self) -> Dict[str, Any]:


        """
        Verifica a existência de Sample Ratio Mismatch (SRM) usando um Teste Qui-Quadrado.

        SRM ocorre quando o tráfego não é dividido na proporção esperada (ex: 50/50),
        o que pode invalidar os resultados do teste.

        Returns:
            Um dicionário contendo:
            - 'has_srm': True se o p-valor for <= 0.01, indicando SRM.
            - 'srm_p_value': O p-valor do teste qui-quadrado.
            - 'srm_expected_per_variation': A contagem de visitantes esperada para cada grupo.
        """
        # Valores observados (visitantes reais em cada grupo)
        # Excel: D5:E5
        observed_visitors = [self.variation.variation_a_visitors, self.variation.variation_b_visitors]

        total_visitors = sum(observed_visitors)
        if total_visitors == 0:
            return {
                "has_srm": False,
                "srm_p_value": 1.0,
                "srm_expected_per_variation": 0
            }

        # Valores esperados (tráfego dividido igualmente)
        # Excel: =(D5+E5)*0,5
        expected_value = total_visitors / 2.0
        expected_visitors = [expected_value, expected_value]

        # Calcula o p-valor do Teste Qui-Quadrado
        # Excel: =TESTE.QUIQUA(D5:E5;H19:I19)
        _, p_value = chisquare(f_obs=observed_visitors, f_exp=expected_visitors)

        # Verifica se há SRM com base no p-valor (nível de significância de 1%)
        # Excel: =SE(H20<=0,01;"SIM";"NÃO")
        has_srm = bool(p_value <= 0.01)

        return {
            "has_srm": has_srm,
            "srm_p_value": float(p_value),
            "srm_expected_per_variation": float(expected_value)
        }
    
    def get_temporal_validation_results(self) -> dict:
        """
        Orquestra e retorna um dicionário com todas as métricas de validação temporal.
        """
        # Define a data final a ser usada: a data de término do teste ou a data de hoje.
        effective_end_date = self.tester.end_date if self.tester.end_date else date.today()
        
        # Calcula cada métrica temporal
        total_duration = self._calculate_total_duration_days(effective_end_date)
        business_days = self._calculate_business_days_duration(effective_end_date)
        daily_visitors = self._calculate_average_daily_visitors(total_duration)
        
        return {
            "current_date": date.today().strftime("%d/%m/%Y"),
            "total_duration_days": total_duration,
            "business_days_duration": business_days,
            "average_daily_visitors": daily_visitors,
        }

    def _calculate_total_duration_days(self, effective_end_date: date) -> int:
        """
        Calcula a duração total do teste em dias corridos.
        Fórmula Excel: =H23-A8
        """
        return (effective_end_date - self.tester.start_date).days

    def _calculate_business_days_duration(self, effective_end_date: date) -> int:
        """
        Calcula a duração do teste em dias úteis (seg-sex).
        Fórmula Excel: =SE(A10="";DIATRABALHOTOTAL(A8;H23);DIATRABALHOTOTAL(A8;A10))
        """

        inclusive_end_date = effective_end_date + timedelta(days=1)
        return np.busday_count(self.tester.start_date, inclusive_end_date).item()

    def _calculate_average_daily_visitors(self, total_duration_days: int) -> float:
        """
        Calcula a média de visitantes diários.
        Fórmula Excel: =SOMA(D5:E5)/H24
        """
        total_visitors = self.variation.variation_a_visitors + self.variation.variation_b_visitors

        if total_duration_days <= 0:
            return float(total_visitors) # Evita divisão por zero
            
        return round(total_visitors / total_duration_days, 2)
    
    def get_test_planning_metrics(self, mde: float) -> dict:
        """
        Orquestra os cálculos de planejamento do teste (usuários e dias necessários).
        """
        p_control = self.variation.conversion_rate_a


        required_users_80_power = self._calculate_required_users(
            p_control=p_control, mde=mde, power_constant=16
        )

        required_users_95_power = self._calculate_required_users(
            p_control=p_control, mde=mde, power_constant=26
        )


        temporal_results = self.get_temporal_validation_results()
        daily_visitors = temporal_results.get("average_daily_visitors", 0)


        required_days_80_power = self._calculate_required_days(
            required_users=required_users_80_power, daily_visitors=daily_visitors
        )

        required_days_95_power = self._calculate_required_days(
            required_users=required_users_95_power, daily_visitors=daily_visitors
        )

        return {
            "required_users_80_power": required_users_80_power,
            "required_users_95_power": required_users_95_power,
            "required_days_80_power": required_days_80_power,
            "required_days_95_power": required_days_95_power,
        }

    def _calculate_required_users(self, p_control: float, mde: float, power_constant: float) -> int:
        """
        Calcula o número total de usuários necessários com base na fórmula da planilha.

        Fórmula Excel: =2*(CONSTANTE*POTÊNCIA(RAIZ(D7*(1-D7))/(D7*D17);2))
        Onde:
        - D7 = p_control
        - D17 = mde
        - CONSTANTE = 16 (para 80% de poder) ou 26 (para 95% de poder)
        """
        if p_control <= 0 or mde <= 0:
            return 0


        absolute_uplift = p_control * mde

        if absolute_uplift <= 0:
            return 0


        variance = p_control * (1 - p_control)

        required_users = 2 * (power_constant * (variance / (absolute_uplift**2)))

        return math.ceil(required_users)

    def _calculate_required_days(self, required_users: int, daily_visitors: float) -> int:
        """
        Calcula o número de dias necessários para atingir a amostra.

        Fórmula Excel: =Numero de Usuários Necessários / Visitantes Diarios
        """
        if not daily_visitors or daily_visitors <= 0:
        
            return 0

        days = required_users / daily_visitors
        return math.ceil(days)