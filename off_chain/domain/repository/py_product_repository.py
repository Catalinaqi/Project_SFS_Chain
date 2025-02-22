from abc import ABC, abstractmethod
from off_chain.domain.entity.product_entity import ProductEntity


class ProductRepository(ABC):
    """
    Repository interface for product persistence.
    """

    @staticmethod
    @abstractmethod
    def create(product: ProductEntity) -> int:
        """Insert a new product into the database."""
        pass

    @staticmethod
    @abstractmethod
    def get_by_id(product_id: int) -> ProductEntity:
        """Gets a product by its ID."""
        pass

    @staticmethod
    @abstractmethod
    def get_all() -> list:
        """Get all stored products."""
        pass
