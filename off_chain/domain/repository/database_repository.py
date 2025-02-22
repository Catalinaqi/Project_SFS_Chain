from off_chain.database.db_cnx_and_exec import DatabaseConfig


class DatabaseRepository:
    """
    Handles direct interactions with the database.
    """

    @staticmethod
    def fetch_query(query, params=()):
        """
        Executes a SELECT query and returns multiple results.
        """
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            raise Exception(f"Error executing SELECT query: {e}")

    @staticmethod
    def fetch_one(query, params=()):
        """
        Executes a SELECT query and returns a single result.
        """
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            raise Exception(f"Error executing SELECT query: {e}")

    @staticmethod
    def execute_query(query, params=(), multiple=False):
        """
        Executes an INSERT, UPDATE, or DELETE query.
        Uses transactions to ensure atomicity.

        Parameters:
        - query: SQL query to execute.
        - params: Tuple or list of tuples (if multiple=True) for parameterized queries.
        - multiple: If True, executes multiple queries using executemany().
        """
        conn = None
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()

            # Begin transaction
            cursor.execute("BEGIN TRANSACTION;")

            if multiple:
                cursor.executemany(query, params)  # Execute multiple queries
            else:
                cursor.execute(query, params)  # Execute single query

            conn.commit()  # Commit changes
        except Exception as e:
            if conn:
                conn.rollback()  # Rollback on error
            raise Exception(f"Database error: {e}")
        finally:
            if conn:
                conn.close()  # Ensure the connection is closed

    @staticmethod
    def execute_transaction(queries):
        """
        Executes multiple SQL queries within a single transaction.

        Parameters:
        - queries: List of tuples containing (query, params).
        """
        conn = None
        try:
            conn = DatabaseConfig.get_connection()
            cursor = conn.cursor()

            # Begin transaction
            cursor.execute("BEGIN TRANSACTION;")

            for query, params in queries:
                cursor.execute(query, params)

            conn.commit()  # Commit all changes
        except Exception as e:
            if conn:
                conn.rollback()  # Rollback on error
            raise Exception(f"Transaction error: {e}")
        finally:
            if conn:
                conn.close()  # Close connection