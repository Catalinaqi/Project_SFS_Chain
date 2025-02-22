from off_chain.domain.repository.database_repository import DatabaseRepository
from off_chain.domain.entity.company_entity import CompanyEntity


class CompanyRepository:
    """
    Handles database operations related to companies.
    """

    @staticmethod
    def insert_company(id_credential, name_company, type_company, location_company):
        """
        Inserts a new company into the database.
        """
        query = """
        INSERT INTO SFS_COMPANY (id_credential, name_company, type_company, location_company)
        VALUES (?, ?, ?, ?);
        """
        DatabaseRepository.execute_query(query, (id_credential, name_company, type_company, location_company))

    @staticmethod
    def get_company_by_id(id_company):
        """
        Retrieves a company by its ID.
        """
        query = "SELECT * FROM SFS_COMPANY WHERE id_company = ?;"
        result = DatabaseRepository.fetch_one(query, (id_company,))
        return CompanyEntity(*result) if result else None

    @staticmethod
    def get_all_companies():
        """
        Retrieves all companies from the database.
        """
        query = "SELECT * FROM SFS_COMPANY;"
        results = DatabaseRepository.fetch_query(query)
        return [CompanyEntity(*row) for row in results]

    @staticmethod
    def update_company(company):
        """
        Updates an existing company.
        """
        query = """
        UPDATE SFS_COMPANY 
        SET id_credential=?, name_company=?, type_company=?, location_company=?
        WHERE id_company=?;
        """
        DatabaseRepository.execute_query(query, (
            company.id_credential, company.name_company, company.type_company,
            company.location_company, company.id_company
        ))

    @staticmethod
    def delete_company(id_company):
        """
        Deletes a company from the database.
        """
        query = "DELETE FROM SFS_COMPANY WHERE id_company=?;"
        DatabaseRepository.execute_query(query, (id_company,))

    @staticmethod
    def get_azienda_by_id(id_company):
        """
        Retrieves company details along with total CO₂ consumption and compensation.
        """
        query_company = """
        SELECT id_company, type_company, location_company, name_company 
        FROM SFS_COMPANY WHERE id_company = ?;
        """

        query_co2_consumed = """
        SELECT SUM(co2_footprint) FROM SFS_OPERATION WHERE id_company = ?;
        """

        query_co2_compensated = """
        SELECT SUM(co2_compensation) FROM SFS_COMPENSATION_ACTION WHERE id_company = ?;
        """

        try:
            company = DatabaseRepository.fetch_query(query_company, (id_company,))
            if not company:
                return None

            co2_consumed = DatabaseRepository.fetch_query(query_co2_consumed, (id_company,))
            co2_compensated = DatabaseRepository.fetch_query(query_co2_compensated, (id_company,))

            total_co2_consumed = co2_consumed[0][0] \
                if co2_consumed and co2_consumed[0][0] is not None \
                else 0
            total_co2_compensated = co2_compensated[0][0] \
                if co2_compensated and co2_compensated[0][0] is not None \
                else 0

            return {
                "company": company[0],  # Details of the company
                "co2_consumed": total_co2_consumed,
                "co2_compensated": total_co2_compensated
            }
        except Exception as e:
            raise Exception(f"Error retrieving company data: {str(e)}")

    # Restituisce la lista di tutte le aziende con i rispettivi valori di CO2 consumata e compensata
    # filtrata per nome
    @staticmethod
    def get_azienda_by_nome(nome):
        query = """
        SELECT id_company, type_company, location_company, name_company FROM SFS_COMPANY WHERE Tipo != "Certificatore"
        AND Nome = ?
        """
        aziende = DatabaseRepository.fetch_query(query, (nome,))
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(co2_footprint) FROM SFS_OPERATION WHERE id_company = ?;
            """
            query_co2_compensata = """
            SELECT SUM(co2_compensation) FROM SFS_COMPENSATION_ACTION WHERE id_company = ?;
            """
            if not DatabaseRepository.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = DatabaseRepository.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not DatabaseRepository.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = DatabaseRepository.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    # Restituisce la lista di tutte le aziende con i rispettivi valori di CO2 consumata e compensata
    # filtrata per tipo
    @staticmethod
    def get_lista_aziende_filtrata_tipo(tipo):
        query = """
        SELECT id_company, type_company, location_company, name_company FROM SFS_COMPANY WHERE type_company != "Certificatore"
        AND Tipo = ?
        """
        aziende = DatabaseRepository.fetch_query(query, (tipo,))
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(co2_footprint) FROM SFS_OPERATION WHERE id_company = ?;
            """
            query_co2_compensata = """
            SELECT SUM(co2_compensation) FROM SFS_COMPENSATION_ACTION WHERE id_company = ?;
            """
            if not DatabaseRepository.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = DatabaseRepository.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not DatabaseRepository.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = DatabaseRepository.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    # Restituisce la lista di tutte le aziende con i rispettivi valori di CO2 consumata e compensata
    @staticmethod
    def get_lista_aziende():
        query = """
        SELECT id_company, type_company, location_company, name_company FROM SFS_COMPANY WHERE type_company != "Certificatore"
        """
        aziende = DatabaseRepository.fetch_query(query)
        lista_con_co2 = []
        for azienda in aziende:
            query_co2_consumata = """
            SELECT SUM(co2_footprint) FROM SFS_OPERATION WHERE id_company = ?;
            """
            query_co2_compensata = """
            SELECT SUM(co2_compensation) FROM SFS_COMPENSATION_ACTION WHERE id_company = ?;
            """
            if not DatabaseRepository.fetch_query(query_co2_consumata, (azienda[0],))[0][0]:
                co2_consumata = 0
            else:
                co2_consumata = DatabaseRepository.fetch_query(query_co2_consumata, (azienda[0],))[0][0]
            if not DatabaseRepository.fetch_query(query_co2_compensata, (azienda[0],))[0][0]:
                co2_compensata = 0
            else:
                co2_compensata = DatabaseRepository.fetch_query(query_co2_compensata, (azienda[0],))[0][0]
            lista_con_co2.append((azienda, co2_consumata, co2_compensata))
        return lista_con_co2

    # Restituisce la lista dei rivenditori
    @staticmethod
    def get_lista_rivenditori():
        query = """
        SELECT id_company, type_company, location_company, name_company FROM SFS_COMPANY WHERE type_company = "Rivenditore"
        """
        return DatabaseRepository.fetch_query(query)

    @staticmethod
    def get_azienda(self, n):
        return self.get_lista_aziende()[n]

    # Restituisce la lista ordinata per saldo CO2 di tutte le aziende
    @staticmethod
    def get_lista_aziende_ordinata(self):
        lista_ordinata = sorted(self.get_lista_aziende(), key=lambda x: (x[2] or 0) - (x[1] or 0), reverse=True)
        return lista_ordinata
