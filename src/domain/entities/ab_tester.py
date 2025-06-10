from datetime import date

class ABTester:
    """
    Representa os dados de um teste A/B.
    """
    def __init__(self,
                 name: str,
                 start_date: date,
                 end_date: date,
                 hypothesis: str,
                 desired_confidence_level: float):
        """
        Inicializa a entidade do teste A/B.

        Args:
            name (str): Nome do teste.
            start_date (date): Data de início.
            end_date (date): Data de encerramento.
            hypothesis (str): Hipótese a ser validada.
            desired_confidence_level (float): Nível de confiança desejado (ex: 95.0, 99.0).
        """
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.hypothesis = hypothesis
        # A entidade deve armazenar o valor real (ex: 95.0), não um valor multiplicado.
        self.desired_confidence_level = desired_confidence_level