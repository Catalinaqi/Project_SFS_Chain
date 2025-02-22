from abc import ABC, abstractmethod
from off_chain.domain.entity.py_credential_entity import UserEntity


class UserRepository(ABC):
    """
    Repository interface for user persistence.
    """

    @staticmethod
    @abstractmethod
    def validate_user(username: str, password: str) -> UserEntity:
        """Validates user credentials."""
        pass

    @staticmethod
    @abstractmethod
    def create_user(user: UserEntity) -> int:
        """Creates a new user in the database."""
        pass
