from dataclasses import dataclass


@dataclass
class OperationEntity:
    """
    Represents an operation performed by a company on a product.
    """
    id_operation: int = None
    id_company: int = None
    id_product: int = None
    co2_footprint: float = None
    operation_description: str = None
    created_date: str = None  # Can be `datetime` if needed

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        if self.id_company is None or self.id_product is None:
            raise ValueError("Company ID and Product ID are required.")

        if self.co2_footprint < 0:
            raise ValueError("CO2 footprint cannot be negative.")
