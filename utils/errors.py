class _DatabaseError(Exception):
    """Base class for database-related errors."""
    pass


class UserAlreadyExistsError(_DatabaseError):
    """Raised when trying to register a user that already exists."""
    def __init__(self, public_key_fingerprint: str, *args, **kwargs):
        super().__init__("Public key already exists in the database.")
        self.public_key_fp = public_key_fingerprint


class InvalidPublicKeyError(_DatabaseError):
    """Raised when an invalid public key is provided."""
    pass


class UserIDNotFoundError(_DatabaseError):
    """Raised when a user ID is not found in the database."""
    pass
