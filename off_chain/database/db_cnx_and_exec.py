import sqlite3
import os

from off_chain.configuration.db_load_setting import DATABASE_PATH, SQL_FILE_PATH
from off_chain.configuration.log_setting import logger


class DatabaseConfig:
    """
    Handles database configuration, connection management, and SQL execution.
    """

    @staticmethod
    def get_connection():
        """
        Establishes and returns a connection to the SQLite3 database.
        The connection uses a row factory to allow access to columns by name.
        """
        try:
            # Debugging: Check the database path
            logger.info(f"Attempting to connect to: {DATABASE_PATH}")

            if not os.path.exists(DATABASE_PATH):
                logger.warning(f"Database file does not exist: {DATABASE_PATH}")

            connexion = sqlite3.connect(DATABASE_PATH)
            connexion.row_factory = sqlite3.Row
            logger.info(f"Connected to the database: {DATABASE_PATH}")

            # Initialize database only if required
            DatabaseConfig.initialize_database()

            return connexion
        except sqlite3.OperationalError as e:
            logger.error(f"SQLite Operational Error: {e}")
            raise Exception(f"SQLite Operational Error: {e}")

        except sqlite3.Error as e:
            logger.error(f"General SQLite Error: {e}")
            raise Exception(f"Database connection error: {e}")

        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise Exception(f"Unexpected error: {e}")

    @staticmethod
    def initialize_database():
        """
        Checks if tables exist before executing the SQL script.
        Prevents unnecessary script execution on every connection.
        """
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            # Check if the main table exists before executing the SQL script
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SFS_PRODUCT';")
            table_exists = cursor.fetchone()

            if not table_exists:
                DatabaseConfig.execute_sql_file()

            conn.close()
        except Exception as e:
            logger.error(f"Error verifying the database: {e}")
            raise Exception(f"Error verifying the database: {e}")

    @staticmethod
    def execute_sql_file():
        """
        Executes an SQL script on the database.
        The SQL file path is defined in settings.yaml.
        """
        global conn
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()

            with open(SQL_FILE_PATH, "r", encoding="utf-8") as file:
                sql_script = file.read()

            cursor.executescript(sql_script)
            conn.commit()
            logger.info(f"SQL script executed successfully: {SQL_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error executing SQL script {SQL_FILE_PATH}: {e}")
            raise Exception(f"Error executing SQL script: {e}")

        finally:
            if conn:
                conn.close()
                logger.info("Database connection closed.")
