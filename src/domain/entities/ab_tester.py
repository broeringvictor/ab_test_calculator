from datetime import date


class ABTester():
    """
    Represents an A/B test with a name, start date, and end date.
    """

    def __init__(self,
                 name: str,
                 start_date: date,
                 end_date: date,
                 hypothesis: str,
                 desired_confidence_level: float):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.hypothesis = hypothesis
        self.desired_confidence_level = desired_confidence_level * 100 # Convert to percentage

        

