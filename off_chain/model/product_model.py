class ProductModel:
    """
    DTO model that represents a Product without directly exposing the domain entity.
    """
    def __init__(self, id_product, name_product, type_product, quantity_product, status_product):
        self.id_product = id_product
        self.name_product = name_product
        self.type_product = type_product
        self.quantity_product = quantity_product
        self.status_product = status_product

    def save(self):
        pass

    @classmethod
    def see_all_products(cls):
        pass
