import streamlit as st
from domain.entities.ab_tester import ABTester
from domain.entities.variation import Variation
# A classe que faz a mágica acontecer
from domain.use_cases.ab_statistical_validator import ABStatisticalValidator 

class ResultsComponent:
    """
    Componente Streamlit para orquestrar os cálculos e renderizar
    todos os resultados do teste A/B.
    """
    def __init__(self, tester: ABTester, variation: Variation):
        """
        Inicializa o componente, recebe as entidades e executa os cálculos.
        
        Args:
            tester (ABTester): A entidade com as definições do teste.
            variation (Variation): A entidade com os dados do teste.
        """
        if not tester or not variation:
            # Em vez de raise, podemos mostrar um erro no Streamlit se preferir,
            # mas para um componente, raise pode ser apropriado.
            st.error("As entidades Tester e Variation são obrigatórias para ResultsComponent.")
            # Para evitar que o app quebre completamente, podemos setar self.results para None
            # e checar isso no método render.
            self.results = None
            self.variation = None # Para evitar AttributeError no _display_main_result
            return

        self.tester = tester
        self.variation = variation
        
        validator = ABStatisticalValidator(tester=self.tester, variation=self.variation)
        self.results = validator.get_statistical_results()

    def _display_main_result(self):
        """Exibe o resultado principal (significante ou não) de forma destacada."""
        if not self.results or not self.variation: # Checagem adicional
            return

        p_value = self.results.get("p_value", 1.0)
        # O confidence_level na variation já está como 0.xx
        significance_level = 1.0 - self.variation.confidence_level 

        if p_value < significance_level:
            st.success(f"**Resultado Significante!** (p-valor {p_value:.4f} < {significance_level:.2f})")
            st.write("Há evidência estatística para rejeitar a hipótese nula. A variação (H1) teve um desempenho diferente do controle (Ho).")
        else:
            st.warning(f"**Resultado Não Significante.** (p-valor {p_value:.4f} >= {significance_level:.2f})")
            st.write("Não há evidência estatística suficiente para afirmar uma diferença entre a variação e o controle.")

    def render(self):
        """Renderiza todos os resultados na tela de forma organizada."""
        if not self.results: # Se __init__ falhou em obter resultados
            st.error("Não foi possível calcular os resultados. Verifique os dados de entrada.")
            return

        st.header("3. Resultados do Teste")
        
        self._display_main_result()
        st.divider()

        st.subheader("Métricas Estatísticas")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Z-Score", f'{self.results.get("z_score", 0):.4f}')
            st.metric("Uplift da Conversão", f'{self.results.get("conversion_rate_uplift", 0):.2%}')
        with col2:
            st.metric("P-Valor", f'{self.results.get("p_value", 0):.4f}')
            st.metric("Poder do Teste (Power)", f'{self.results.get("observed_test_power", 0):.2%}')
        with col3:
            st.metric("Z-Crítico", f'{self.results.get("z_critical", 0):.4f}')
            st.metric("Confiança Atual", f'{self.results.get("current_confidence", 0):.2%}')

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Intervalos de Confiança")
            lower = self.results.get("control_lower_bound", 0)
            upper = self.results.get("control_upper_bound", 0)
            st.write(f"**Controle (Ho):** `{lower:.2%}` – `{upper:.2%}`")
            
            lower_v = self.results.get("variation_lower_bound", 0)
            upper_v = self.results.get("variation_upper_bound", 0)
            st.write(f"**Variação (H1):** `{lower_v:.2%}` – `{upper_v:.2%}`")
        
        with col2:
            st.subheader("SRM (Sample Ratio Mismatch)")
            srm_results = self.results.get("srm_results", {})
            has_srm = srm_results.get("has_srm", False)
            srm_p_value = srm_results.get("srm_p_value", 1.0)
            
            if has_srm:
                st.error(f"SIM - Alerta de SRM! (p-valor: {srm_p_value:.4f})")
            else:
                st.success(f"NÃO (p-valor: {srm_p_value:.4f})")

        st.divider()

        st.subheader("Planejamento e Duração")
        planning = self.results.get("planning_results", {})
        temporal = self.results.get("temporal_validation_results", {})
        
        total_duration = temporal.get("total_duration_days", 0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Para 80% de Poder Estatístico:**")
            req_users_80 = planning.get("required_users_80_power", "N/A")
            req_days_80 = planning.get("required_days_80_power", "N/A")
            remaining_days_80 = "N/A"
            if isinstance(req_days_80, (int, float)) and isinstance(total_duration, (int, float)):
                 remaining_days_80 = max(0, req_days_80 - total_duration)


            st.metric("Usuários Necessários", f"{req_users_80:,}" if isinstance(req_users_80, (int,float)) else req_users_80)
            st.metric("Dias Totais Estimados", f"{req_days_80}", f"{remaining_days_80} dias restantes" if remaining_days_80 != "N/A" else "")

        with col2:
            st.write("**Para 95% de Poder Estatístico:**")
            req_users_95 = planning.get("required_users_95_power", "N/A")
            req_days_95 = planning.get("required_days_95_power", "N/A")
            remaining_days_95 = "N/A"
            if isinstance(req_days_95, (int, float)) and isinstance(total_duration, (int, float)):
                remaining_days_95 = max(0, req_days_95 - total_duration)

            st.metric("Usuários Necessários", f"{req_users_95:,}" if isinstance(req_users_95, (int,float)) else req_users_95)
            st.metric("Dias Totais Estimados", f"{req_days_95}", f"{remaining_days_95} dias restantes" if remaining_days_95 != "N/A" else "")

# REMOVA O CÓDIGO ABAIXO DESTE PONTO NO SEU ARQUIVO results_component.py
# from components.ab_tester_component import ABTesterComponent
# from components.variation_component import VariationComponent
# st.set_page_config(layout="wide", page_title="Calculadora de Teste A/B")
# st.title("Calculadora de Significado Estatístico para Teste A/B")
# ... (todo o resto do código que estava aqui)