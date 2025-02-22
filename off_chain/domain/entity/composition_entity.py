from dataclasses import dataclass


@dataclass
class CompositionEntity:
    """
    Represents the composition of products (Product - Raw Material relationship).
    """
    cod_product: int
    cod_raw_material: int

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        if self.cod_product is None or self.cod_raw_material is None:
            raise ValueError("Product and Raw Material codes are required.")
