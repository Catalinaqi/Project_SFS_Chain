from off_chain.domain.repository.database_repository import DatabaseRepository
from off_chain.domain.entity.operation_entity import OperationEntity


class OperationRepository:
    """
    Handles database operations related to SFS_OPERATION.
    """

    @staticmethod
    def insert_operation(id_company, id_product, co2_footprint, operation_description):
        """
        Inserts a new operation into the database.
        """
        query = """
        INSERT INTO SFS_OPERATION (id_company, id_product, co2_footprint, operation_description)
        VALUES (?, ?, ?, ?);
        """
        DatabaseRepository.execute_query(query, (id_company, id_product, co2_footprint, operation_description))

    @staticmethod
    def get_operation_by_id(id_operation):
        """
        Retrieves an operation by its ID.
        """
        query = "SELECT * FROM SFS_OPERATION WHERE id_operation = ?;"
        result = DatabaseRepository.fetch_one(query, (id_operation,))
        return OperationEntity(*result) if result else None

    @staticmethod
    def get_all_operations():
        """
        Retrieves all operations from the database.
        """
        query = "SELECT * FROM SFS_OPERATION;"
        results = DatabaseRepository.fetch_query(query)
        return [OperationEntity(*row) for row in results]

    @staticmethod
    def get_operazioni_ordinate_co2(id_company):
        """
        Retrieves operations performed by a product, ordered by CO2 footprint (ascending).
        """
        query = """
        SELECT 
            O.id_operation, P.id_product, P.name_product, P.quantity_product,
            O.created_date,O.co2_footprint, O.operation_description
        FROM SFS_OPERATION O
        JOIN SFS_PRODUCT P ON O.id_product = P.id_product
        WHERE O.id_company = ?
        ORDER BY O.co2_footprint ASC;
        """
        results = DatabaseRepository.fetch_query(query, (id_company,))
        return [OperationEntity(*row) for row in results]

    @staticmethod
    def update_operation(operation):
        """
        Updates an existing operation.
        """
        query = """
        UPDATE SFS_OPERATION 
        SET id_company=?, id_product=?, co2_footprint=?, operation_description=?
        WHERE id_operation=?;
        """
        DatabaseRepository.execute_query(query, (
            operation.id_company, operation.id_product, operation.co2_footprint,
            operation.operation_description, operation.id_operation
        ))

    @staticmethod
    def delete_operation(id_operation):
        """
        Deletes an operation from the database.
        """
        query = "DELETE FROM SFS_OPERATION WHERE id_operation=?;"
        DatabaseRepository.execute_query(query, (id_operation,))

    @staticmethod
    def get_operazioni_by_data(id_company, start_date, end_date):
        """
        Retrieves operations performed by a company within a given date range.
        """
        query = """
        SELECT 
            O.id_operation, P.id_product, P.name_product, P.quantity_product, 
            O.created_date,O.co2_footprint, O.operation_description
        FROM SFS_OPERATION O
        JOIN SFS_PRODUCT P ON O.id_product = P.id_product
        WHERE O.id_company = ?
        AND O.created_date BETWEEN ? AND ?;
        """
        results = DatabaseRepository.fetch_query(query, (id_company, start_date, end_date,))
        return [OperationEntity(*row) for row in results]

    @staticmethod
    def get_operazioni_by_azienda(id_company, start_date, end_date):
        """
        Restituisce la lista di tutte le operazioni effettuate da una certa azienda.
        """
        query = """
        SELECT 
            O.id_operation, P.id_product, P.name_product, P.quantity_product, 
            O.operation_description,O.co2_footprint, O.operation_description
        FROM SFS_OPERATION O
        JOIN SFS_PRODUCT P ON O.id_product = P.id_product
        WHERE O.id_company = ?;
        """
        results = DatabaseRepository.fetch_query(query, (id_company, start_date, end_date,))
        return [OperationEntity(*row) for row in results]

    @staticmethod
    def inserisci_operazione_azienda_rivenditore(id_company, id_product, operation_date, co2_footprint,
                                                 operation_description):
        """
        Inserts a new operation for a retailer and updates the product status in a single transaction.
        """
        queries = [
            ("""
            INSERT INTO SFS_OPERATION (id_company, id_product, created_date, co2_footprint, operation_description)
            VALUES (?, ?, ?, ?, ?);
            """, (id_company, id_product, operation_date, co2_footprint, operation_description)),

            ("""
            UPDATE SFS_PRODUCT SET status_product = ? WHERE id_product = ?;
            """, (111, id_product))
        ]

        try:
            DatabaseRepository.execute_transaction(queries)
        except Exception as e:
            raise Exception(f"Error inserting retailer operation: {str(e)}")

    @staticmethod
    def inserisci_operazione_azienda_trasformazione(id_company, product, operation_date, co2_footprint,
                                                    operation_description, quantity=0, raw_materials=None):
        """
        Inserts a transformation operation. If the product is a new transformation, it creates a new product record.
        Updates product status and registers composition.
        """
        if raw_materials is None:
            raw_materials = []

        queries = []

        if operation_description == "Trasformazione":
            # In questo caso, il parametro prodotto è l'id del prodotto che seleziono
            # Inserisci l'operazione
            queries.append((
                """
                INSERT INTO SFS_OPERATION (id_company, id_product, created_date, co2_footprint, operation_description)
                VALUES (?, ?, ?, ?, ?);
                """,
                (id_company, product[0], operation_date, co2_footprint, operation_description)
            ))
            # Modifica lo stato del prodotto
            queries.append((
                """
                UPDATE SFS_PRODUCT SET status_product = ? WHERE id_product = ?;
                """,
                (101, product[0])  # Stato 101: Prodotto trasformato
            ))

        else:
            # In quest'altro caso, invece, il parametro prodotto è il nome del prodotto che seleziono.
            # Questo perché devo creare una nuova istanza di prodotto e mi serve il nome
            # (l'id nella tabella prodotto è autoincrement).
            queries.append((
                """
                INSERT INTO SFS_PRODUCT (name_product, quantity_product, status_product)
                VALUES (?, ?, ?);
                """,
                (product, quantity, 10)  # Stato 10: Prodotto grezzo
            ))

            # Ottieni l'ID del prodotto inserito
            queries.append((
                """
                SELECT last_insert_rowid();
                """,
                ()
            ))

            # Inserisci l'operazione
            queries.append((
                """
                INSERT INTO SFS_OPERATION (id_company, id_product, created_date, 
                co2_footprint, operation_description)
                VALUES (?, last_insert_rowid(), ?, ?, ?);
                """,
                (id_company, operation_date, co2_footprint, operation_description)
            ))

            # Inserisci la composizione
            queries.append((
                """
                INSERT INTO SFS_COMPOSITION (cod_product, cod_raw_material)
                VALUES (last_insert_rowid(), last_insert_rowid());
                """,
                ()
            ))

            for raw_material in raw_materials:
                queries.append((
                    """
                    INSERT INTO SFS_COMPOSITION (cod_product, cod_raw_material)
                    VALUES (last_insert_rowid(), ?);
                    """,
                    (raw_material,)
                ))

                # Modifica lo stato del prodotto
                queries.append((
                    """
                    UPDATE SFS_PRODUCT SET status_product = ? WHERE id_product = ?;
                    """,
                    (110, raw_material)  # Stato 110: Prodotto trasformato
                ))

        try:
            DatabaseRepository.execute_transaction(queries)
        except Exception as e:
            raise Exception(f"Error inserting transformation operation: {str(e)}")

    @staticmethod
    def inserisci_operazione_azienda_trasporto(id_company, id_product, operation_date, co2_footprint,
                                               operation_description, new_status):
        """
        Inserts a transport operation and updates the product status.
        If the new status is 11 (Retailer), inserts a record in SFS_COMPOSITION.
        """
        queries = [
            # Insert operation into SFS_OPERATION
            ("""
            INSERT INTO SFS_OPERATION (id_company, id_product, created_date, co2_footprint, operation_description)
            VALUES (?, ?, ?, ?, ?);
            """, (id_company, id_product, operation_date, co2_footprint, operation_description)),

            # Update product status in SFS_PRODUCT
            ("""
            UPDATE SFS_PRODUCT SET status_product = ? WHERE id_product = ?;
            """, (new_status, id_product))
        ]

        if new_status == 11:  # If the destination is a retailer
            queries.append((
                """
                INSERT OR IGNORE INTO SFS_COMPOSITION (cod_product, cod_raw_material)
                VALUES (?, ?);
                """, (id_product, id_product)
            ))

        try:
            DatabaseRepository.execute_transaction(queries)
        except Exception as e:
            raise Exception(f"Error inserting transport operation: {str(e)}")


