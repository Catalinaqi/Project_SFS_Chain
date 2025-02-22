from off_chain.domain.entity.product_entity import ProductEntity


class ProductRepository:
    """
    Handles database operations related to products.
    """

    @staticmethod
    def insert_product(name_product, type_product, quantity_product, status_product):
        """
        Inserts a new product into the database.
        """
        query = """
        INSERT INTO SFS_PRODUCT (name_product, type_product, quantity_product, status_product)
        VALUES (?, ?, ?, ?);
        """
        DatabaseRepository.execute_query(query, (name_product, type_product, quantity_product, status_product))

    @staticmethod
    def get_all_products():
        """
        Retrieves all products from the database.
        """
        query = "SELECT * FROM SFS_PRODUCT;"
        results = DatabaseRepository.fetch_query(query)
        return [ProductEntity(*row) for row in results]

    @staticmethod
    def get_product_by_id(id_product):
        """
        Retrieves a product by its ID.
        """
        query = "SELECT * FROM SFS_PRODUCT WHERE id_product = ?;"
        result = DatabaseRepository.fetch_one(query, (id_product,))
        return ProductEntity(*result) if result else None

    @staticmethod
    def get_products_by_name(name_product):
        """
        Retrieves products filtered by name.
        """
        query = "SELECT * FROM SFS_PRODUCT WHERE name_product = ?;"
        results = DatabaseRepository.fetch_query(query, (name_product,))
        return [ProductEntity(*row) for row in results]

    @staticmethod
    def update_product_quantity(id_product, new_quantity):
        """
        Updates the quantity of a product.
        """
        query = "UPDATE SFS_PRODUCT SET quantity_product = ? WHERE id_product = ?;"
        DatabaseRepository.execute_query(query, (new_quantity, id_product))

    @staticmethod
    def delete_product(id_product):
        """
        Deletes a product from the database.
        """
        query = "DELETE FROM SFS_PRODUCT WHERE id_product = ?;"
        DatabaseRepository.execute_query(query, (id_product,))

    @staticmethod
    def get_prodotti_to_composizione(id_company):
        """
        Retrieves products used in the transformation process by a given company.
        """
        query = """
        SELECT P.id_product, P.name_product, P.quantity_product
        FROM SFS_PRODUCT P
        WHERE P.status_product != 110
        AND P.id_product IN (
            SELECT O.id_product
            FROM SFS_OPERATION O
            WHERE O.id_company = ? AND O.operation_description = 'Trasformazione'
        );
        """
        results = DatabaseRepository.fetch_query(query, (id_company,))
        return [ProductEntity(*row) for row in results]

    # Le seguenti quattro funzioni permettono l'inserimento di un'operazione
    # a seconda del tipo di azienda che la sta effettuando
    @staticmethod
    def inserisci_operazione_azienda_agricola(product_name, quantity, id_company, operation_date, co2_footprint,
                                              operation_description):
        """
        Inserts a new agricultural product and logs the operation.
        """
        queries = [
            # Insert product into SFS_PRODUCT
            ("""
            INSERT INTO SFS_PRODUCT (name_product, quantity_product, status_product)
            VALUES (?, ?, ?);
            """, (product_name, quantity, 0)),  # Status 0: Newly created product

            # Retrieve the last inserted product ID
            ("""
            SELECT last_insert_rowid();
            """, ())
        ]

        # Insert operation into SFS_OPERATION
        queries.append((
            """
            INSERT INTO SFS_OPERATION (id_company, id_product, created_date, co2_footprint, operation_description)
            VALUES (?, last_insert_rowid(), ?, ?, ?);
            """,
            (id_company, operation_date, co2_footprint, operation_description)
        ))

        try:
            DatabaseRepository.execute_transaction(queries)
        except Exception as e:
            raise Exception(f"Error inserting agricultural operation: {str(e)}")

    # Questa funzione restituisce i prodotti che l'azienda di trasformazione
    # può inserire nella tabella "composizione" come valori dell'attributo "materia prima"
    @staticmethod
    def get_materie_prime(id_company):
        """
        Retrieves raw materials that a transformation company can use for composition.
        """
        query = """
        SELECT SFS_PRODUCT.id_product, SFS_PRODUCT.name_product, SFS_PRODUCT.quantity_product
        FROM SFS_PRODUCT
        JOIN SFS_OPERATION ON SFS_PRODUCT.id_product = SFS_OPERATION.id_product
        WHERE SFS_OPERATION.operation_description = "Trasformazione"
        AND SFS_OPERATION.id_company = ?
        ORDER BY SFS_OPERATION.created_date DESC;
        """
        try:
            return DatabaseRepository.fetch_query(query, (id_company,))
        except Exception as e:
            raise Exception(f"Error retrieving raw materials: {str(e)}")

    @staticmethod
    def get_prodotti_to_rivenditore():
        """
        Retrieves products available for retailers (status = 11).
        """
        query = """
        SELECT id_product, name_product, quantity_product
        FROM SFS_PRODUCT
        WHERE status_product = 11;
        """
        try:
            return DatabaseRepository.fetch_query(query)
        except Exception as e:
            raise Exception(f"Error retrieving retailer products: {str(e)}")


from off_chain.domain.repository.database_repository import DatabaseRepository


class ProductRepository:
    """
    Handles database operations related to SFS_PRODUCT.
    """

    @staticmethod
    def get_prodotti_to_azienda_trasformazione(operation_type):
        """
        Retrieves products available for transformation companies.
        If the operation is 'Transformation', fetches products with status 1.
        Otherwise, fetches final products from SFS_THRESHOLD.
        """
        if operation_type == "Trasformazione":
            query = """
            SELECT id_product, name_product, quantity_product
            FROM SFS_PRODUCT
            WHERE status_product = 1;
            """
            try:
                return DatabaseRepository.fetch_query(query)
            except Exception as e:
                raise Exception(f"Error retrieving transformation products: {str(e)}")
        else:
            return ProductRepository.get_final_products()

    @staticmethod
    def get_final_products():
        """
        Retrieves distinct final products from SFS_THRESHOLD.
        """
        query = """
        SELECT DISTINCT product_threshold FROM SFS_THRESHOLD WHERE tipo = "final product";
        """
        try:
            results = DatabaseRepository.fetch_query(query)
            return [row[0] for row in results]  # Extracting only product names
        except Exception as e:
            raise Exception(f"Error retrieving final products: {str(e)}")

    @staticmethod
    def get_prodotti_to_azienda_trasporto(destinatario):
        """
        Retrieves products available for transport to transformation companies or retailers.
        """
        query_transformation = """
        SELECT id_product, name_product, quantity_product
        FROM SFS_PRODUCT
        WHERE (status_product = 0 OR status_product = 10)
        AND name_product IN (
            SELECT product_threshold
            FROM SFS_THRESHOLD
            WHERE tipo = "materia prima"
        );
        """

        query_retailer = """
        SELECT id_product, name_product, quantity_product 
        FROM SFS_PRODUCT
        WHERE status_product = 0 OR status_product = 10;
        """

        try:
            if destinatario == "Azienda di trasformazione":
                return DatabaseRepository.fetch_query(query_transformation)
            return DatabaseRepository.fetch_query(query_retailer)
        except Exception as e:
            raise Exception(f"Error retrieving transport products: {str(e)}")

    # Restituisce lo storico del prodotto selezionato
    @staticmethod
    def get_storico_prodotto(prodotto):
        query = """
        SELECT
            SFS_OPERATION.id_operation,
            SFS_COMPANY.name_company,
            SFS_PRODUCT.name_product,
            SFS_OPERATION.created_date,
            SFS_OPERATION.co2_footprint,
            SFS_OPERATION.operation_description
        FROM SFS_OPERATION
        JOIN SFS_COMPANY ON SFS_OPERATION.id_company = Azienda.id_company
        JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = Prodotto.id_product
        WHERE SFS_OPERATION.id_product IN (
            SELECT cod_raw_material
            FROM SFS_COMPOSITION
            WHERE cod_product = ?
        );
        """
        return DatabaseRepository.fetch_query(query, (prodotto,))

    @staticmethod
    def co2_consumata_prodotti(self, prodotti):
        lista_con_co2 = []
        for prodotto in prodotti:
            storico = self.get_storico_prodotto(prodotto[0])
            totale_co2 = sum(t[4] for t in storico)
            lista_con_co2.append((prodotto, totale_co2))
        return lista_con_co2


    # Restituisce i prodotti certificati sullo scaffale filtrati per nome
    @staticmethod
    def get_prodotti_certificati_by_nome(self,nome):
        query = """
        SELECT
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.name_product,
            SFS_PRODUCT.quantity_product,
            SFS_PRODUCT.status_product,
            SFS_COMPANY.name_company
        FROM SFS_OPERATION
        JOIN SFS_COMPANY ON SFS_OPERATION.id_company = SFS_COMPANY.id_company
        JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = SFS_PRODUCT.id_product
        WHERE SFS_OPERATION.operation_description = "Messo sugli scaffali"
        AND SFS_OPERATION.id_product IN (
            SELECT id_product FROM SFS_CERTIFICATION_BODY
        )
        AND Prodotto.Nome = ?;
        """
        return self.co2_consumata_prodotti(DatabaseRepository.fetch_query(query, (nome, )))


    # Restituisce i prodotti certificati sullo scaffale filtrati per rivenditore
    @staticmethod
    def get_prodotti_certificati_by_rivenditore(self, id_rivenditore):
        query = """
        SELECT
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.name_product,
            SFS_PRODUCT.quantity_product,
            SFS_PRODUCT.status_product,
            SFS_COMPANY.name_company
        FROM SFS_OPERATION
        JOIN SFS_COMPANY ON SFS_OPERATION.id_company = Azienda.id_company
        JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = SFS_PRODUCT.id_product
        WHERE SFS_OPERATION.operation_description = "Messo sugli scaffali"
        AND SFS_OPERATION.id_product IN (
            SELECT id_product FROM SFS_CERTIFICATION_BODY
        )
        AND SFS_OPERATION.Id_azienda = ?;
        """
        return self.co2_consumata_prodotti(DatabaseRepository.fetch_query(query, (id_rivenditore, )))

    # Restituisce tutti i prodotti sugli scaffali con un certo nome
    @staticmethod
    def get_prodotti_by_nome(self, nome):
        query = """
                SELECT
                    SFS_PRODUCT.id_product,
                    SFS_PRODUCT.name_product,
                    SFS_PRODUCT.quantity_product,
                    SFS_PRODUCT.status_product,
                    SFS_PRODUCT.id_product
                FROM SFS_OPERATION
                JOIN SFS_COMPANY ON SFS_OPERATION.id_operation = SFS_COMPANY.id_operation
                JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = SFS_PRODUCT.id_product
                WHERE SFS_OPERATION.operation_description = "Messo sugli scaffali"
                AND SFS_PRODUCT.id_product = ?;
                """
        return self.co2_consumata_prodotti(DatabaseRepository.fetch_query(query, (nome, )))

    # Restituisce una lista di prodotti sullo scaffale filtrati per rivenditore
    @staticmethod
    def get_lista_prodotti_by_rivenditore(self, rivenditore):
        query = """
        SELECT
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.quantity_product,
            SFS_PRODUCT.status_product,
            SFS_COMPANY.name_company
        FROM SFS_OPERATION
        JOIN SFS_COMPANY ON SFS_OPERATION.id_operation = SFS_COMPANY.id_operation
        JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = SFS_PRODUCT.id_product
        WHERE SFS_OPERATION.operation_description = "Messo sugli scaffali"
        AND SFS_OPERATION.id_operation = ?;
        """
        return self.co2_consumata_prodotti(DatabaseRepository.fetch_query(query, (rivenditore,)))

    # Restituisce la lista di tutti i prodotti sullo scaffale certificati
    @staticmethod
    def get_prodotti_certificati(self):
        query = """
        SELECT
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.quantity_product,
            SFS_PRODUCT.status_product,
            SFS_COMPANY.name_company
        FROM SFS_OPERATION
        JOIN SFS_COMPANY ON SFS_OPERATION.id_operation = SFS_COMPANY.id_operation
        JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = SFS_PRODUCT.id_product
        WHERE SFS_OPERATION.operation_description = "Messo sugli scaffali"
        AND SFS_OPERATION.id_product IN (
            SELECT id_product FROM SFS_CERTIFICATION_BODY
        );
        """
        return self.co2_consumata_prodotti(DatabaseRepository.fetch_query(query))


    # Restituisce la lista di prodotti sugli scaffali per il guest
    @staticmethod
    def get_lista_prodotti(self):
        query = """
        SELECT
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.id_product,
            SFS_PRODUCT.quantity_product,
            SFS_PRODUCT.status_product,
            SFS_COMPANY.name_company
        FROM SFS_OPERATION
        JOIN SFS_COMPANY ON SFS_OPERATION.id_operation = SFS_COMPANY.id_operation
        JOIN SFS_PRODUCT ON SFS_OPERATION.id_product = SFS_PRODUCT.id_product
        WHERE SFS_OPERATION.operation_description = "Messo sugli scaffali";
        """
        return self.co2_consumata_prodotti(DatabaseRepository.fetch_query(query))

    # Restituisce tutti i prodotti sugli scaffali ordinati per co2 consumata
    @staticmethod
    def get_prodotti_ordinati_co2(self):
        return sorted(self.get_lista_prodotti(), key=lambda x: x[1])


    # Restituisce i prodotti certificati sullo scaffale ordinati per co2 consumata
    @staticmethod
    def get_prodotti_certificati_ordinati_co2(self):
        return sorted(self.get_prodotti_certificati(), key=lambda x: x[1])