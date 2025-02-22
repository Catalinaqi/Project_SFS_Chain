from off_chain.configuration.log_setting import logger
from off_chain.database.db_cnx_and_exec import DatabaseConfig

if __name__ == "__main__":
    conn = DatabaseConfig.get_connection()
    print("Database connection established successfully.")
    logger.info("Database connection established successfully.")
    logger.debug("Database connection established successfully.")
    conn.close()
