import sqlite3
from off_chain.domain.repository.database_repository import DatabaseRepository


class CredentialRepository:
    """
    Handles database operations related to SFS_CREDENTIAL.
    """

    @staticmethod
    def get_credential_by_username(username):
        """
        Retrieves credential details by username.
        """
        query = """
        SELECT id_credential, username, password_hash, topt_secret, public_key, private_key, role_credential
        FROM SFS_CREDENTIAL WHERE username = ?;
        """
        try:
            credential = DatabaseRepository.fetch_query(query, (username,))
            return credential[0] if credential else None
        except sqlite3.Error as e:
            raise Exception(f"Error retrieving credential data: {str(e)}")

    @staticmethod
    def insert_credential(username, password_hash, topt_secret):
        """
        Inserts a new credential record.
        """
        query = """
        INSERT INTO SFS_CREDENTIAL (username, password_hash, topt_secret)
        VALUES (?, ?, ?, ?);
        """
        try:
            DatabaseRepository.execute_query(query, (username, password_hash, topt_secret))
            return True
        except sqlite3.IntegrityError:
            raise Exception("Error: Username already exists.")
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    def get_lista_credenziali():
        query = """
        SELECT * FROM SFS_CREDENTIAL
        """
        return DatabaseRepository.fetch_query(query)
