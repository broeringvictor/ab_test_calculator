import streamlit as st
from datetime import date, timedelta
from domain.entities.ab_tester import ABTester # Importa sua entidade

class ABTesterComponent:
    """
    Um componente Streamlit para renderizar e gerenciar os inputs
    de definição de um teste A/B.
    """
    def __init__(self):
        """Inicializa o componente com valores padrão."""
        # Adicionando type hints para clareza
        self.name: str = "Teste A/B"
        self.start_date: date = date.today()
        self.end_date: date = self.start_date + timedelta(days=14)
        self.hypothesis: str = ""
        self.desired_confidence_level: float = 95.0

    def render_inputs(self):
        """
        Renderiza os widgets de input e atualiza os atributos da classe
        com os valores selecionados pelo usuário.
        """
        st.header("Definições do Teste")

        self.name = st.text_input(
            label="Nome do Teste",
            value=self.name,
            help="Dê um nome descritivo para o seu teste A/B."
        )

        self.hypothesis = st.text_area(
            label="Hipótese do Teste",
            placeholder="Ex: Se alterarmos a cor do botão 'Comprar' para verde, a taxa de cliques aumentará.",
            help="Descreva o que você espera que aconteça e por quê."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            self.start_date = st.date_input(
                label="Data de Início",
                value=self.start_date,
                min_value=date(2020, 1, 1)
            )

        with col2:
            self.end_date = st.date_input(
                label="Data de Encerramento",
                value=self.end_date,
                min_value=self.start_date
            )

        self.desired_confidence_level = st.selectbox(
            label="Nível de Confiança Desejado",
            options=[90.0, 95.0, 99.0],
            index=1, # Deixa 95.0 como padrão
            format_func=lambda x: f"{x:.0f}%", # Formata para "95%" em vez de "95.0%"
            help="O nível de confiança estatística para validar o resultado."
        )

    def get_ab_tester_entity(self) -> ABTester | None:
        """
        Cria e retorna uma instância da entidade ABTester com os dados do formulário.
        Retorna None se os dados forem inválidos.
        """
        if self.end_date < self.start_date:
            st.error("A data de encerramento não pode ser anterior à data de início.")
            return None

        return ABTester(
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            hypothesis=self.hypothesis,
            desired_confidence_level=self.desired_confidence_level
        )