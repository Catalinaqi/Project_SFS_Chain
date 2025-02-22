from off_chain.service.py_product_service import ProductService


class ProductController:
    """
    Controlador que maneja la lógica de interacción de productos en la UI.
    """

    @staticmethod
    def load_products(view):
        """Carga productos desde la BD y actualiza la vista."""
        products = ProductService.get_all_products()
        view.update_product_list(products)