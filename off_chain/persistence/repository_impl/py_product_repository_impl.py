from off_chain.domain.entity.product_entity import ProductEntity
from off_chain.domain.repository.database_repository import DatabaseRepository
from off_chain.domain.repository.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    """
     Implementación del repositorio de productos usando DatabaseRepository.
     """

    @staticmethod
    def create(product: ProductEntity) -> int:
        """Inserta un nuevo producto en la base de datos y devuelve su ID."""
        query = """
        INSERT INTO SFS_PRODUCT (name_product, type_product, quantity_product, status_product, created_date)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (product.name_product, product.type_product, product.quantity_product, product.status_product, product.created_date)
        return DatabaseRepository.execute_query(query, params)

    @staticmethod
    def get_by_id(product_id: int) -> ProductEntity:
        """Obtiene un producto por su ID."""
        query = "SELECT * FROM SFS_PRODUCT WHERE id_product = ?"
        row = DatabaseRepository.fetch_one(query, (product_id,))
        return ProductEntity(*row) if row else None

    @staticmethod
    def get_all() -> list:
        """Obtiene todos los productos almacenados en la base de datos."""
        query = "SELECT * FROM SFS_PRODUCT"
        rows = DatabaseRepository.fetch_query(query)
        return [ProductEntity(*row) for row in rows] if rows else []