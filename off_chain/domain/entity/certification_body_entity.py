from dataclasses import dataclass


@dataclass
class CertificationBodyEntity:
    """
    Represents a certification body approving a product.
    """
    id_certification_body: int = None
    id_product: int = None
    id_company: int = None
    description: str = None
    created_date: str = None  # Can be `datetime` if needed

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        if self.id_product is None or self.id_company is None:
            raise ValueError("Product ID and Company ID are required.")
