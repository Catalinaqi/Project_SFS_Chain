from off_chain.domain.repository.database_repository import DatabaseRepository


class CompensationRepository:
    """
    Handles database operations related to SFS_COMPENSATION_ACTION.
    """

    # Restituisce la lista delle azioni compensative per azienda
    @staticmethod
    def get_lista_azioni(id_company):
        """
        Retrieves all compensation actions for a specific company.
        """
        query = """
        SELECT * FROM SFS_COMPENSATION_ACTION WHERE id_company = ?;
        """
        try:
            return DatabaseRepository.fetch_query(query, (id_company,))
        except Exception as e:
            raise Exception(f"Error retrieving compensation actions: {str(e)}")

    # Restituisce la lista di azioni compensative filtrate per data
    @staticmethod
    def get_lista_azioni_per_data(id_company, start_date, end_date):
        """
        Retrieves compensation actions filtered by date range.
        """
        query = """
        SELECT * FROM SFS_COMPENSATION_ACTION
        WHERE id_company = ? AND created_date BETWEEN ? AND ?;
        """
        try:
            return DatabaseRepository.fetch_query(query, (id_company, start_date, end_date))
        except Exception as e:
            raise Exception(f"Error retrieving compensation actions by date: {str(e)}")

    # Restituisce la lista di azioni compensative ordinata per co2 risparmiata
    @staticmethod
    def get_lista_azioni_ordinata(id_company):
        """
        Retrieves all compensation actions for a company sorted by CO₂ compensation.
        """
        query = """
        SELECT * FROM SFS_COMPENSATION_ACTION
        WHERE id_company = ?
        ORDER BY co2_compensation DESC;
        """
        try:
            return DatabaseRepository.fetch_query(query, (id_company,))
        except Exception as e:
            raise Exception(f"Error retrieving compensation actions sorted by CO₂: {str(e)}")

    # Restituisce il valore della co2 compensata per azienda
    @staticmethod
    def get_co2_compensata(id_company):
        """
        Retrieves the total CO₂ compensated by a company.
        """
        query = """
        SELECT SUM(co2_compensation) FROM SFS_COMPENSATION_ACTION WHERE id_company = ?;
        """
        try:
            result = DatabaseRepository.fetch_query(query, (id_company,))
            return result[0][0] if result and result[0][0] is not None else 0
        except Exception as e:
            raise Exception(f"Error retrieving total CO₂ compensated: {str(e)}")

    # Inserisce una nuova azione compensativa
    @staticmethod
    def inserisci_azione(date, id_company, co2_compensated, action_name):
        """
        Inserts a new compensation action.
        """
        query = """
        INSERT INTO SFS_COMPENSATION_ACTION (created_date, id_company, co2_compensation, name_compensation_action)
        VALUES (?, ?, ?, ?);
        """
        try:
            DatabaseRepository.execute_query(query, (date, id_company, co2_compensated, action_name))
        except Exception as e:
            raise Exception(f"Error inserting compensation action: {str(e)}")
