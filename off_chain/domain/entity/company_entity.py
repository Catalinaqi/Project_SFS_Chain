from dataclasses import dataclass


@dataclass
class CompanyEntity:
    """
    Represents a company entity in the system.
    """
    id_company: int = None
    id_credential: int = None
    name_company: str = None
    type_company: str = None
    location_company: str = None
    created_date: str = None  # Can be `datetime` if needed

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        valid_types = {'Farmer', 'Producer', 'Logistics', 'Retailer', 'CertificationBody'}
        if self.type_company not in valid_types:
            raise ValueError(f"Invalid type_company. Must be one of {valid_types}.")

        if not self.name_company or not isinstance(self.name_company, str) or not self.name_company.strip():
            raise ValueError("Name must be a non-empty string.")

        if not self.location_company or not isinstance(self.location_company, str) or not self.location_company.strip():
            raise ValueError("Location must be a non-empty string.")
