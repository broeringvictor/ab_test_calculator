import streamlit as st
from domain.entities.ab_tester import ABTester
from domain.entities.variation import Variation
from domain.use_cases.ab_statistical_validator import ABStatisticalValidator 

class ResultsComponent:
    def __init__(self, tester: ABTester, variation: Variation): # Changed signature
        self.tester = tester
        self.variation = variation # Store variation entity

        if not self.tester or not self.variation:
            st.error("As entidades Tester e Variation são obrigatórias para ResultsComponent.")
            self.results = {} # Initialize as empty dict to avoid errors
            return

        # Perform statistical validation internally
        validator = ABStatisticalValidator(variation=self.variation, tester=self.tester)
        self.results = validator.get_statistical_results()

        # Ensure conversion rates are in self.results for _display_confidence_intervals
        # if they are not already added by ABStatisticalValidator
        if 'control_conversion_rate' not in self.results:
            self.results['control_conversion_rate'] = self.variation.conversion_rate_a
        if 'variation_conversion_rate' not in self.results:
            self.results['variation_conversion_rate'] = self.variation.conversion_rate_b

    def _display_main_result(self):
        st.subheader("Resultado Principal")
        p_value = self.results.get("p_value", 1.0)
        
        # Correctly calculate significance_level from desired_confidence_level (e.g., 95.0 -> 0.05)
        significance_level = 1.0 - (self.tester.desired_confidence_level / 100.0)

        if p_value < significance_level:
            st.success(f"### 🎉 Resultado Significante!")
            # Use self.tester.desired_confidence_level for the message consistency
            st.write(f"Com uma confiança de **{self.tester.desired_confidence_level}%**, a Variação (B) mostrou um desempenho estatisticamente diferente do Controle (A). (p-valor: {p_value:.4f})")
        else:
            st.warning(f"### 🤔 Resultado Não Significante")
            st.write(f"Não há evidência estatística suficiente para afirmar uma diferença de desempenho entre a Variação (B) e o Controle (A) com o nível de confiança desejado de **{self.tester.desired_confidence_level}%**. (p-valor: {p_value:.4f})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Uplift da Conversão", f"{self.results.get('conversion_rate_uplift', 0):.2%}")
        col2.metric("P-Valor", f"{p_value:.4f}")
        # current_confidence is calculated by ABStatisticalValidator based on p_value
        col3.metric("Confiança do Resultado", f"{self.results.get('current_confidence', 0):.2%}")
    
    def _display_confidence_intervals(self):
        with st.expander("🔍 Análise de Uplift e Intervalos de Confiança"):
            st.markdown("""
            O **Intervalo de Confiança** mostra a faixa provável da verdadeira taxa de conversão para cada grupo. Se os intervalos **não se sobrepõem**, é um forte indicativo de que a diferença entre eles é real.
            """)
            
            # These should now be correctly populated in self.results by __init__
            p_a = self.results.get('control_conversion_rate', 0)
            p_b = self.results.get('variation_conversion_rate', 0)
            lower_a = self.results.get('control_lower_bound', 0)
            upper_a = self.results.get('control_upper_bound', 0)
            lower_b = self.results.get('variation_lower_bound', 0)
            upper_b = self.results.get('variation_upper_bound', 0)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Controle (A): {p_a:.2%}**")
                st.write(f"Intervalo: `{lower_a:.2%}` a `{upper_a:.2%}`")
            with col2:
                st.markdown(f"**Variação (B): {p_b:.2%}**")
                st.write(f"Intervalo: `{lower_b:.2%}` a `{upper_b:.2%}`")

    def _display_test_validity(self):
        with st.expander("✅ Análise de Validade e Poder do Teste"):
            st.markdown("""
            Esta seção verifica se os resultados do seu teste são confiáveis. Verificamos o **Poder Estatístico** (a capacidade de detectar um efeito real) e o **SRM** (se o tráfego foi dividido corretamente).
            """)

            # Poder do Teste Observado
            power = self.results.get("observed_test_power", 0)
            st.subheader("Poder do Teste Observado")
            if isinstance(power, (float, int)):
                st.progress(int(power * 100))
                st.write(f"O poder observado do seu teste foi de **{power:.2%}**.")
                if power >= 0.8:
                    st.success("**Excelente!** Seu teste teve uma alta probabilidade de detectar uma diferença real, caso ela exista.")
                else:
                    st.warning("**Atenção!** O poder do teste foi baixo. Isso significa que, mesmo que houvesse uma diferença real, o teste tinha uma baixa probabilidade de detectá-la. Para testes futuros, considere aumentar o número de visitantes.")
            else:
                st.write("Poder do teste não pôde ser calculado.")
            
            st.divider()

            # Validação de SRM
            srm_results = self.results.get("srm_results", {})
            has_srm = srm_results.get("has_srm", False)
            srm_p_value = srm_results.get("srm_p_value", 1.0)
            st.subheader("SRM (Sample Ratio Mismatch)")
            if not has_srm:
                st.success(f"**NÃO HÁ SRM.** (P-valor do SRM: {srm_p_value:.3f})")
                st.write("A divisão de tráfego entre os grupos parece correta. Os resultados do teste são confiáveis nesse quesito.")
            else:
                st.error(f"**ALERTA DE SRM!** (P-valor do SRM: {srm_p_value:.3f})")
                st.write("A proporção de visitantes entre os grupos Controle e Variação é inesperadamente diferente. Isso pode indicar um problema na configuração do teste e invalida os resultados. Verifique sua ferramenta de A/B testing.")

    def render(self):
        if not self.results: # Check if results were properly initialized
            st.error("Não foi possível gerar o relatório de resultados. Verifique os dados de entrada.")
            return
            
        st.title("📊 Relatório de Resultados")
        self._display_main_result()
        st.divider()
        self._display_confidence_intervals()
        self._display_test_validity()