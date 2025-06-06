
class ConfigurationTester:
    """
            A class to configuration A/B tests.
    """

    def __init__(self, tail_numbers: int, obs_power: bool, confidence_level: float, stimated_uplift: float ):
        self.tail_numbers = tail_numbers
        self.obs_power = obs_power
        self.confidence_level = confidence_level * 100
        self.stimated_uplift = stimated_uplift

        

    def is_valid(self, tail_numbers: int, obs_power: bool, confidence_level: float, stimated_uplift: float) -> bool:
        """
        Check if the configuration is valid.
        """
        # Placeholder for actual validation logic
        return True

    def get_configuration(self):
        """
        Get the current configuration.
        """
        return self.config