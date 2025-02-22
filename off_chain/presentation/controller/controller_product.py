from off_chain.model.product_model import ProductModel as Product, ProductModel
from off_chain.domain.repository import ProductRepository


class ProductController:

    def new_product(self, product_type, company_id, name, type, quantity, emissions):
        product = Product(1, product_type, company_id, name, type, quantity, "today", emissions)
        product.save()

    def see_all_products(self):
        return Product.see_all_products()

    @staticmethod
    def get_all_products():
        """Convert entities into data models for the API."""
        products = ProductRepository.get_all_products()
        return [ProductModel(p.id_product, p.name_product, p.type_product, p.quantity_product, p.status_product) for p in products]

