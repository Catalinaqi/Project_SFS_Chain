from off_chain.domain.entity.product_entity import ProductEntity
from off_chain.persistence.repository_impl.py_product_repository_impl import ProductRepositoryImpl
from off_chain.model.py_product_model import ProductModel


class ProductService:
    """
    Capa de servicio para la gestión de productos.
    """

    @staticmethod
    def get_all_products() -> list:
        """Obtiene todos los productos y los transforma en modelos de datos."""
        products = ProductRepositoryImpl.get_all()
        return [ProductModel(p.id_product, p.name_product, p.type_product, p.quantity_product, p.status_product, p.created_date) for p in products]

    @staticmethod
    def create_product(product_data: dict) -> int:
        """Crea un nuevo producto y lo almacena en la base de datos."""
        product = ProductEntity(**product_data)
        return ProductRepositoryImpl.create(product)
