from dataclasses import dataclass


@dataclass
class UserModel:
    """
    Data Transfer Object (DTO) for user authentication.
    """
    id_credential: int
    username: str
    role_credential: str
    created_date: str
