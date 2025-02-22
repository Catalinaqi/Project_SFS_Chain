from off_chain.domain.repository.database_repository import DatabaseRepository
from off_chain.domain.entity.py_credential_entity import UserEntity
from off_chain.domain.repository.py_credential_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    """
    Implementation of the user repository using DatabaseRepository.
    """

    @staticmethod
    def validate_user(username: str, password: str) -> UserEntity:
        """Queries the database and validates credentials."""
        query = ("SELECT id_credential, username, password_hash, topt_secret, public_key, private_key, role_credential, created_date "
                 "FROM SFS_CREDENTIAL WHERE username = ? AND password_hash = ?")
        row = DatabaseRepository.fetch_one(query, (username, password))
        return UserEntity(*row) if row else None

    @staticmethod
    def create_user(user: UserEntity) -> int:
        """Creates a new user."""
        query = ("INSERT INTO SFS_CREDENTIAL (username, password_hash, topt_secret, public_key, private_key, role_credential, created_date) "
                 "VALUES (?, ?, ?, ?, ?, ?, ?)")
        params = (
            user.username, user.password_hash, user.topt_secret, user.public_key, user.private_key,
            user.role_credential,
            user.created_date)
        return DatabaseRepository.execute_query(query, params)
