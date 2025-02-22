from dataclasses import dataclass


@dataclass
class CredentialEntity:
    """
    Represents user credentials in the system.
    """
    id_credential: int = None
    username: str = None
    password_hash: str = None
    topt_secret: str = None
    public_key: str = None
    private_key: str = None
    role_credential: str = None
    created_date: str = None  # Can be `datetime` if needed

    def __post_init__(self):
        """
        Validates values after initialization.
        """
        if not self.username or not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("Username must be a non-empty string.")

        if not self.password_hash or not isinstance(self.password_hash, str):
            raise ValueError("Password hash is required.")

        if not self.topt_secret or not isinstance(self.topt_secret, str):
            raise ValueError("TOTP secret is required.")
