from dataclasses import dataclass


@dataclass
class UserEntity:
    """
    Domain entity representing the SFS_CREDENTIAL table.
    """
    id_credential: int
    username: str
    password_hash: str
    topt_secret: str
    public_key: str
    private_key: str
    role_credential: str
    created_date: str