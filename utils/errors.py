class DatabaseError(Exception):
    """Base class for database-related errors."""
    pass


class UserAlreadyExistsError(DatabaseError):
    """Raised when trying to register a user that already exists."""
    def __init__(self, public_key_fingerprint: str, *args, **kwargs):
        super().__init__("Public key already exists in the database.")
        self.public_key_fp = public_key_fingerprint


class InvalidPublicKeyError(DatabaseError):
    """Raised when an invalid public key is provided."""
    pass
