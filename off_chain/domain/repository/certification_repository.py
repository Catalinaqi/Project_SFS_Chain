from off_chain.domain.repository.database_repository import DatabaseRepository


class CertificationRepository:
    """
    Handles database operations related to SFS_CERTIFICATION_BODY.
    """

    # Restituisce il numero di certificazioni di un'azienda
    @staticmethod
    def get_numero_certificazioni(id_company):
        """
        Retrieves the number of certifications issued by a company.
        """
        query = """
        SELECT COUNT(*) FROM SFS_CERTIFICATION_BODY WHERE id_company = ?;
        """
        try:
            result = DatabaseRepository.fetch_query(query, (id_company,))
            return result[0][0] if result and result[0][0] is not None else 0
        except Exception as e:
            raise Exception(f"Error retrieving the number of certifications: {str(e)}")

    # Restituisce true se il prodotto è certificato, false altrimenti
    @staticmethod
    def is_certificato(id_product):
        """
        Checks if a product is certified.
        Returns True if certified, False otherwise.
        """
        query = """
        SELECT * FROM SFS_CERTIFICATION_BODY WHERE id_product = ?;
        """
        try:
            result = DatabaseRepository.fetch_query(query, (id_product,))
            return bool(result)  # True if the product is found, False otherwise
        except Exception as e:
            raise Exception(f"Error checking product certification: {str(e)}")

    # Inserisce un nuovo certificato
    @staticmethod
    def inserisci_certificato(id_product, description, id_company, certification_date):
        """
        Inserts a new certification for a product.
        """
        query = """
        INSERT INTO SFS_CERTIFICATION_BODY (id_product, description, id_company, created_date)
        VALUES (?, ?, ?, ?);
        """
        try:
            DatabaseRepository.execute_query(query, (id_product, description, id_company, certification_date))
        except Exception as e:
            raise Exception(f"Error inserting certification: {str(e)}")

    # Restituisce la certificazione del prodotto selezionato
    @staticmethod
    def get_certificazione_by_prodotto(prodotto):
        query = """
        SELECT 
            SFS_CERTIFICATION_BODY.id_certification_body,
            SFS_PRODUCT.name_product,
            SFS_CERTIFICATION_BODY.description,
            SFS_COMPANY.name_company,
            SFS_CERTIFICATION_BODY.created_date
        FROM SFS_CERTIFICATION_BODY
        JOIN SFS_COMPANY ON SFS_CERTIFICATION_BODY.id_company = SFS_COMPANY.id_company
        JOIN SFS_PRODUCT ON SFS_CERTIFICATION_BODY.id_product = SFS_PRODUCT.id_product
        WHERE SFS_CERTIFICATION_BODY.id_product = ?;
        """
        return DatabaseRepository.fetch_query(query, (prodotto,))
