from off_chain.persistence.repository_impl.py_credential_repository_impl import UserRepositoryImpl
from off_chain.model.py_credential_model import UserModel
from off_chain.domain.entity.py_credential_entity import UserEntity


class UserService:
    """
    Service layer for user authentication management.
    """

    @staticmethod
    def login(username: str, password: str):
        """Verifies if the user is valid."""
        user = UserRepositoryImpl.validate_user(username, password)
        return UserModel(user.id_credential, user.username, user.role_credential, user.created_date) if user else None

    @staticmethod
    def register(user_data: dict) -> int:
        """Registers a new user."""
        user = UserEntity(**user_data)
        return UserRepositoryImpl.create_user(user)
