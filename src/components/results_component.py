import pandas as pd
import streamlit as st
import textwrap
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

    def _apply_custom_css(self):
            """Aplica CSS customizado para corrigir a largura dos tooltips."""
            st.markdown("""
            <style>
            /* Alvo específico do container do conteúdo do tooltip do Streamlit */
            div[data-testid="stTooltipContent"] {
                max-width: 1000px !important;  /* Aumenta a largura E força a aplicação da regra */
                word-wrap: break-word;
                white-space: normal;
            }
            </style>
            """, unsafe_allow_html=True)

    def _display_main_result(self):
        st.subheader("Resultado Principal")
        p_value = self.results.get("p_value", 1.0)
        
        # Nível de confiança desejado, ex: 95.0
        desired_confidence = self.tester.desired_confidence_level
        
        # Nível de significância (alfa), ex: 0.05 para 95% de confiança
        significance_level = 1.0 - (desired_confidence / 100.0)


        confidence_text = f"{desired_confidence:.1f}%".replace(".0%", "%")

        if p_value < significance_level:
        
            st.success("### 🎉 Temos um vencedor!")
            st.write(
                f"Pode comemorar! A **Variação (B)** superou o **Controle (A)** "
                f"com um nível de confiança de **{confidence_text}**."
            )
            st.caption(
                "Isso significa que a mudança na Variação (B) tem alta probabilidade de ser a causa "
                f"da melhoria, não sendo apenas uma obra do acaso. (p-valor: {p_value:.4f})"
            )
        else:
            # --- COPY MELHORADO (Resultado Não Significante) ---
            st.warning("### 🤔 Resultado Inconclusivo")
            st.write(
                f"Ainda não há evidências para declarar a **Variação (B)** como vencedora sobre o **Controle (A)**, "
                f"considerando o nível de confiança de **{confidence_text}**."
            )
            st.caption(
                "Isso não significa que a Variação (B) é pior, mas que a diferença observada não foi "
                f"grande o suficiente para descartarmos a chance de ser um resultado aleatório."
            )

        with st.expander("Critério de Decisão Estatística"):
            st.markdown(f"""
            A decisão de significância é baseada na comparação entre o **p-valor** do teste e o **nível de significância (α)**.

            - **Nível de Significância (α):** `{significance_level:.3f}` (calculado como `100% - {confidence_text}`)
            - **P-Valor do Teste:** `{p_value:.4f}`

            A regra de decisão é: se o **p-valor for menor que o nível de significância (α)**, o resultado é estatisticamente significante.

            Neste caso, como `{p_value:.4f}` é **{'menor' if p_value < significance_level else 'maior ou igual a'}** `{significance_level:.3f}`, o resultado foi considerado **{'Significante' if p_value < significance_level else 'Inconclusivo'}**.
            """)
        
        st.write("---") # Separador visual
        
        col1, col2, col3 = st.columns(3)
        col1.metric(
            label="Uplift da Conversão",
            value=f"{self.results.get('conversion_rate_uplift', 0):.2%}",
            help="Indica o aumento ou diminuição percentual da taxa de conversão da Variação (B) em relação ao Controle (A). Esta métrica quantifica o impacto direto da alteração testada."
        )

        col2.metric(
            label="P-Valor",
            value=f"{p_value:.4f}",
            help="Probabilidade de obter os resultados observados (ou mais extremos) caso a hipótese nula seja verdadeira. Um p-valor baixo (menor que o nível de significância α) sugere que o resultado observado não é fruto do acaso."
        )

        col3.metric(
            label="Confiança do Resultado",
            value=f"{(1 - p_value):.2%}",
            help="Representa a probabilidade de que a diferença observada seja real. Calculada como (1 - p-valor), oferece uma interpretação intuitiva da significância. Uma confiança de 97% corresponde a um p-valor de 0.03."
        )

    def _display_confidence_intervals(self):
        """
        Exibe a análise de significância estatística com uma interface clara e conclusões diretas.
        """
        with st.expander("💡 Análise de Significância Estatística e Uplift", expanded=True):
            st.markdown("""
            Para garantir que a diferença de conversão não é fruto do acaso, analisamos os **Intervalos de Confiança**.
            Pense neles como a "margem de erro" de cada versão. Eles nos mostram a faixa onde a verdadeira taxa de conversão provavelmente se encontra.
            """)

            p_a = self.results.get('control_conversion_rate', 0)
            p_b = self.results.get('variation_conversion_rate', 0)
            lower_a = self.results.get('control_lower_bound', 0)
            upper_a = self.results.get('control_upper_bound', 0)
            lower_b = self.results.get('variation_lower_bound', 0)
            upper_b = self.results.get('variation_upper_bound', 0)
            
            # --- NOVO: Lógica para verificar a sobreposição ---
            # A sobreposição ocorre se o limite inferior de um grupo for menor que o limite superior do outro.
            # Verificamos a condição de NÃO sobreposição para simplificar.
            no_overlap = (upper_a < lower_b) or (upper_b < lower_a)
            
            st.divider() # Adiciona uma linha visual

            # --- NOVO: Mensagem de conclusão baseada na sobreposição ---
            if no_overlap:
                st.success(
                    "**✅ Resultado Significativo: Os intervalos de confiança NÃO se sobrepõem.**\n\n"
                    "Há uma forte evidência estatística de que a diferença entre os grupos é real."
                )
            else:
                st.warning(
                    "**⚠️ Resultado Inconclusivo: Os intervalos de confiança se sobrepõem.**\n\n"
                    "Não há evidência estatística para afirmar que uma versão é superior à outra."
                )

            st.divider()

            # --- NOVO: Layout em colunas com st.metric ---
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Controle (A)**")
                st.metric(label="Taxa de Conversão", value=f"{p_a:.2%}")
                st.markdown(f"**Intervalo de Confiança (95%):** `{lower_a:.2%}` — `{upper_a:.2%}`")
                
            with col2:
                st.markdown("**Variação (B)**")
                st.metric(label="Taxa de Conversão", value=f"{p_b:.2%}")
                st.markdown(f"**Intervalo de Confiança (95%):** `{lower_b:.2%}` — `{upper_b:.2%}`")

            st.caption("Nota Técnica: Um nível de confiança de 95% indica que, se repetíssemos o teste 100 vezes, em 95 delas a taxa de conversão real estaria dentro do intervalo.")


    def _display_temporal_and_planning_analysis(self):
        """
        Exibe a análise temporal com um visual aprimorado usando barras de progresso.
        """
        with st.expander("🗓️ Análise Temporal e Planejamento do Teste", expanded=True): # Deixei expandido por padrão
            st.markdown("""
            Esta seção contextualiza o teste no tempo e compara a duração atual com o planejamento necessário para alcançar poder estatístico, ajudando a decidir quando parar o teste com segurança.
            """)

            temporal_results = self.results.get("temporal_validation_results", {})
            planning_results = self.results.get("planning_results", {})
            dias_corridos = temporal_results.get('total_duration_days', 0)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Situação Atual")
                st.metric("Duração do Teste (Dias)", f"{dias_corridos}")
                st.metric("Duração (Dias Úteis)", f"{temporal_results.get('business_days_duration', 0)}")
                st.metric("Média de Visitantes/Dia", f"{int(temporal_results.get('average_daily_visitors', 0))}")

            with col2:
                st.subheader("Progresso para Conclusão")

                # --- Cartão para 80% de Poder ---
                with st.container(border=True):
                    dias_necessarios_80 = planning_results.get('required_days_80_power', 0)
                    st.markdown("##### Para 80% de Poder Estatístico")

                    if dias_necessarios_80 > 0:
                        progresso_80 = min(1.0, dias_corridos / dias_necessarios_80)
                        st.progress(progresso_80)
                        st.caption(f"{dias_corridos} de {dias_necessarios_80} dias concluídos.")
                    else:
                        st.caption("Não foi possível calcular a duração necessária.")

                    # Status final
                    if dias_corridos >= dias_necessarios_80 and dias_necessarios_80 > 0:
                        st.success("✅ **CONCLUÍDO:** A duração para 80% de poder foi atingida.")
                    else:
                        dias_faltantes_80 = max(0, dias_necessarios_80 - dias_corridos)
                        st.info(f"⏳ **Em andamento:** Faltam {dias_faltantes_80} dias para atingir a meta.")
                
                st.write("") # Adiciona um pequeno espaço vertical

                # --- Cartão para 95% de Poder ---
                with st.container(border=True):
                    dias_necessarios_95 = planning_results.get('required_days_95_power', 0)
                    st.markdown("##### Para 95% de Poder Estatístico")

                    if dias_necessarios_95 > 0:
                        progresso_95 = min(1.0, dias_corridos / dias_necessarios_95)
                        st.progress(progresso_95)
                        st.caption(f"{dias_corridos} de {dias_necessarios_95} dias concluídos.")
                    else:
                        st.caption("Não foi possível calcular a duração necessária.")

                    # Status final
                    if dias_corridos >= dias_necessarios_95 and dias_necessarios_95 > 0:
                        st.success("✅ **CONCLUÍDO:** A duração para 95% de poder foi atingida.")
                    else:
                        dias_faltantes_95 = max(0, dias_necessarios_95 - dias_corridos)
                        st.info(f"⏳ **Em andamento:** Faltam {dias_faltantes_95} dias para atingir a meta.")


    def _display_test_validity(self):
        with st.expander("✅ Análise de Validade e Poder do Teste"):
            st.markdown("""
            Esta seção verifica se os resultados do seu teste são confiáveis. Verificamos o **Poder Estatístico** (a capacidade de detectar um efeito real) e o **SRM** (se o tráfego foi dividido corretamente).
            """)

            # Poder do Teste Observado
            power = self.results.get("observed_test_power", 0)
            st.subheader("Poder do Teste Observado", help=textwrap.dedent("""
            Pense no Poder Estatístico como o 'poder de resolução' do seu teste. Ele quantifica a 
            capacidade do experimento de 'enxergar' uma diferença real entre as variações, caso ela exista.
            
            Tecnicamente, é a probabilidade de rejeitar corretamente a hipótese nula quando 
            ela é, de fato, falsa.

            Sua importância é crítica para evitar o Erro Tipo II (falso negativo). Um teste com 
            baixo poder pode levar a uma conclusão perigosa: abandonar uma ideia vencedora por achar 
            que 'não houve diferença', quando na verdade o teste apenas não teve 'força' para detectá-la.
            
            O padrão de 80% de poder garante que você tenha uma alta probabilidade de confirmar 
            cientificamente as suas hipóteses bem-sucedidas.
            """))
            st.markdown("""
                        >O padrão de 80% de poder garante que você tenha uma alta probabilidade de confirmar 
                        cientificamente as suas hipóteses bem-sucedidas.
            """)
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
            st.subheader("SRM (Sample Ratio Mismatch)", help=textwrap.dedent("""
            O SRM (Sample Ratio Mismatch) verifica se a proporção de visitantes entre os grupos Controle e Variação está correta. 
            """))      
            if not has_srm:
                st.success(f"**NÃO HÁ SRM.** (P-valor do SRM: {srm_p_value:.3f})")
                st.write("A divisão de tráfego entre os grupos parece correta. Os resultados do teste são confiáveis nesse quesito.")
            else:
                st.error(f"**ALERTA DE SRM!** (P-valor do SRM: {srm_p_value:.3f})")
                st.write("A proporção de visitantes entre os grupos Controle e Variação é inesperadamente diferente. Isso pode indicar um problema na configuração do teste e invalida os resultados. Verifique sua ferramenta de A/B testing.")



    def _display_full_results_table(self):
        """
        Exibe uma tabela completa com TODAS as métricas calculadas (incluindo
        as aninhadas), seus valores e descrições.
        """
        with st.expander("📖 Glossário de Métricas e Resultados Detalhados"):
            
            # Lista de dicionários para definir cada métrica, sua descrição e formatação.
            # A chave 'path' é uma tupla que indica o caminho para o valor no dicionário de resultados.
            metrics_glossary = [
                # --- Resultados Principais ---
                {'label': 'Uplift da Conversão', 'path': ('conversion_rate_uplift',), 'description': 'A melhoria percentual da Variação (B) em relação ao Controle (A).', 'formatter': lambda x: f"{x:.2%}"},
                {'label': 'P-Valor', 'path': ('p_value',), 'description': 'Probabilidade do resultado ser aleatório. Um valor baixo (< 0.05) indica significância estatística.', 'formatter': lambda x: f"{x:.4f}"},
                {'label': 'Confiança do Resultado', 'path': ('current_confidence',), 'description': 'Certeza de que a diferença observada é real (calculada como 1 - P-Valor).', 'formatter': lambda x: f"{x:.2%}"},
                
                # --- Validade do Teste ---
                {'label': 'Poder do Teste Observado', 'path': ('observed_test_power',), 'description': 'Probabilidade de detectar um efeito real, caso ele exista. Idealmente > 80%.', 'formatter': lambda x: f"{x:.2%}"},
                {'label': 'SRM (Sample Ratio Mismatch)', 'path': ('srm_results', 'has_srm'), 'description': 'Indica se a divisão de tráfego foi desigual, o que pode invalidar o teste.', 'formatter': lambda x: "Sim" if x else "Não"},
                
                # --- Análise Temporal (Situação Atual) ---
                {'label': 'Duração Atual (Dias)', 'path': ('temporal_validation_results', 'total_duration_days'), 'description': 'Número de dias corridos que o teste está ativo.', 'formatter': lambda x: f"{int(x)}"},
                {'label': 'Duração Atual (Dias Úteis)', 'path': ('temporal_validation_results', 'business_days_duration'), 'description': 'Número de dias úteis (Seg-Sex) que o teste está ativo.', 'formatter': lambda x: f"{int(x)}"},
                {'label': 'Média de Visitantes por Dia', 'path': ('temporal_validation_results', 'average_daily_visitors'), 'description': 'Média de visitantes diários totais (Controle + Variação).', 'formatter': lambda x: f"{int(x)}"},

                # --- Planejamento do Teste ---
                {'label': 'Usuários Necessários (80% Poder)', 'path': ('planning_results', 'required_users_80_power'), 'description': 'Amostra total necessária para atingir 80% de poder estatístico.', 'formatter': lambda x: f"{int(x):,}"},
                {'label': 'Dias Necessários (80% Poder)', 'path': ('planning_results', 'required_days_80_power'), 'description': 'Estimativa de dias para atingir 80% de poder com o tráfego atual.', 'formatter': lambda x: f"{int(x)}"},
                {'label': 'Usuários Necessários (95% Poder)', 'path': ('planning_results', 'required_users_95_power'), 'description': 'Amostra total necessária para atingir 95% de poder estatístico.', 'formatter': lambda x: f"{int(x):,}"},
                {'label': 'Dias Necessários (95% Poder)', 'path': ('planning_results', 'required_days_95_power'), 'description': 'Estimativa de dias para atingir 95% de poder com o tráfego atual.', 'formatter': lambda x: f"{int(x)}"},

                # --- Detalhes Estatísticos ---
                {'label': 'Z-Score', 'path': ('z_score',), 'description': 'Mede a diferença entre os grupos em unidades de desvio padrão.', 'formatter': lambda x: f"{x:.4f}"},
                {'label': 'Z-Crítico', 'path': ('z_critical',), 'description': 'Valor de referência para o Z-Score baseado no nível de confiança.', 'formatter': lambda x: f"{x:.4f}"},
                {'label': 'Erro Padrão da Diferença', 'path': ('standard_error_difference',), 'description': 'O desvio padrão da diferença entre as taxas de conversão.', 'formatter': lambda x: f"{x:.6f}"},
                {'label': 'Intervalo Confiança - Controle', 'path': ('control_lower_bound',), 'description': 'Faixa provável da verdadeira taxa de conversão do Controle.', 'formatter': lambda x, u=self.results.get('control_upper_bound', 0): f"{x:.2%} - {u:.2%}"},
                {'label': 'Intervalo Confiança - Variação', 'path': ('variation_lower_bound',), 'description': 'Faixa provável da verdadeira taxa de conversão da Variação.', 'formatter': lambda x, u=self.results.get('variation_upper_bound', 0): f"{x:.2%} - {u:.2%}"},
            ]
            
            table_data = []
            # Loop para processar e formatar os dados para a tabela
            for metric_info in metrics_glossary:
                value = self.results
                try:
                    # Navega pelo caminho para encontrar o valor aninhado
                    for key in metric_info['path']:
                        value = value[key]
                    
                    # Formatação especial para os intervalos de confiança
                    if 'Intervalo Confiança' in metric_info['label']:
                        # O valor já é formatado com o limite superior na lambda
                        formatted_value = metric_info['formatter'](value)
                    else:
                        formatted_value = metric_info['formatter'](value)

                    table_data.append({
                        "Métrica": metric_info['label'],
                        "Valor Calculado": formatted_value,
                        "Descrição": metric_info['description']
                    })
                except (KeyError, TypeError):
                    # Ignora a métrica se o caminho não for encontrado
                    continue
            
            # Filtra entradas duplicadas de intervalos de confiança
            unique_table_data = []
            seen_metrics = set()
            for item in table_data:
                if item['Métrica'] not in seen_metrics:
                    unique_table_data.append(item)
                    seen_metrics.add(item['Métrica'])

            # Cria e exibe o DataFrame do pandas
            if unique_table_data:
                df = pd.DataFrame(unique_table_data)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Métrica": st.column_config.TextColumn("Métrica", width="medium"),
                        "Valor Calculado": st.column_config.TextColumn("Valor", width="small"),
                        "Descrição": st.column_config.TextColumn("Descrição", width="large"),
                    }
                )
            else:
                st.warning("Não foi possível gerar a tabela de resumo de métricas.")
    def render(self):
        self._apply_custom_css()
        if not self.results: # Check if results were properly initialized
            st.error("Não foi possível gerar o relatório de resultados. Verifique os dados de entrada.")
            return
            
        st.title("📊 Relatório de Resultados")
        self._display_main_result()
        st.divider()
        self._display_confidence_intervals()
        self._display_test_validity()
        self._display_temporal_and_planning_analysis()
        self._display_full_results_table()
        st.write("---")