from dataclasses import dataclass


@dataclass
class CompensationActionEntity:
    """
    Represents a compensation action taken by a company.
    """
    id_compensation_action: int = None
    id_company: int = None
    name_compensation_action: str = None
    co2_compensation: float = None
    created_date: str = None  # Can be `datetime` if needed

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        if self.id_company is None:
            raise ValueError("Company ID is required.")

        if not self.name_compensation_action or not isinstance(self.name_compensation_action, str):
            raise ValueError("Compensation action name must be a valid string.")

        if self.co2_compensation < 0:
            raise ValueError("CO2 compensation cannot be negative.")
