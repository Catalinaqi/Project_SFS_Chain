from off_chain.domain.repository.database_repository import DatabaseRepository


class ThresholdRepository:
    """
    Handles database operations related to SFS_THRESHOLD.
    """

    # Questa funzione restituisce la soglia data l'operazione e il prodotto
    @staticmethod
    def get_soglia_by_operazione_and_prodotto(operation_threshold, product_threshold):
        """
        Retrieves the maximum threshold for a given operation and product.
        Returns 999 if no threshold is found.
        """
        query = """
        SELECT threshold_maximum 
        FROM SFS_THRESHOLD 
        WHERE operation_threshold = ? AND product_threshold = ?;
        """
        result = DatabaseRepository.fetch_query(query, (operation_threshold, product_threshold))

        if not result:
            print("Threshold not found, returning default value 999.")
            return 999

        return result[0][0]  # Retorna el valor del threshold máximo

    # Le seguenti quattro funzioni restituiscono gli elementi che verranno visualizzati nelle
    # rispettive combo box, a seconda del tipo di azienda che sta effettuando l'operazione
    @staticmethod
    def get_prodotti_to_azienda_agricola():
        """
        Retrieves distinct raw materials from SFS_THRESHOLD.
        """
        query = """
            SELECT DISTINCT product_threshold FROM SFS_THRESHOLD WHERE tipo = "materia prima";
            """
        try:
            results = DatabaseRepository.fetch_query(query)
            return [row[0] for row in results]  # Extracting only product names
        except Exception as e:
            raise Exception(f"Error retrieving raw materials for agricultural companies: {str(e)}")

    # Restituisce la lista di tutte le soglie
    @staticmethod
    def get_lista_soglie():
        """
        Retrieves the complete list of thresholds from SFS_THRESHOLD.
        """
        query = """
        SELECT * FROM SFS_THRESHOLD;
        """
        try:
            return DatabaseRepository.fetch_query(query)
        except Exception as e:
            raise Exception(f"Error retrieving thresholds: {str(e)}")