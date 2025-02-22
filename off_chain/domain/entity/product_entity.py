from dataclasses import dataclass
import datetime


@dataclass
class ProductEntity:
    """
    Domain Entity (DDD) that represents the SFS_PRODUCT table.
    """
    id_product: int = None
    name_product: str = None
    type_product: str = None
    quantity_product: int = None
    status_product: int = None
    created_date: str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def is_available(self) -> bool:
        """Business Rule: A product is available if the quantity is greater than 0."""
        return self.quantity_product > 0
