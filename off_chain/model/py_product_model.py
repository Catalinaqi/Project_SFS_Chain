from dataclasses import dataclass


@dataclass
class ProductModel:
    """
    Modelo de datos para transportar información del producto entre capas.
    """
    id_product: int
    name_product: str
    type_product: str
    quantity_product: int
    status_product: int
    created_date: str
