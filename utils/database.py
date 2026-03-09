import hashlib
import logging
import sqlite3
import uuid
from typing import Any, List

from .cryptography import validate_public_key
from .errors import *


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None
        self.logger = None

    def connect(self) -> None:
        """
        Establishes a connection to the SQLite database specified by db_name.
        :return:
        """
        self.logger = logging.getLogger("prencrypt-database")
        self.logger.setLevel(logging.DEBUG)
        self.connection = sqlite3.connect(self.db_name)
        self.logger.debug(f"Connected to database {self.db_name}")

    def disconnect(self) -> None:
        """
        Closes the database connection if it is open.
        :return:
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.debug(f"Disconnected from database {self.db_name}")

    def initialize_database(self) -> None:
        """
        Initializes the database by creating the necessary tables. The schema is defined in the 'schema.sql' file.
        :return:
        """
        if not self.connection:
            raise _DatabaseError("Database connection is not established.")

        cursor = self.connection.cursor()
        with open('schema.sql', 'r') as f:
            schema = f.read()
        cursor.executescript(schema)
        self.connection.commit()
        self.logger.debug(f"Initialized database {self.db_name}")

    def register_new_user(self, public_key: bytes) -> uuid.UUID:
        """
        Registers a new user with the given public key. If the public key already exists in the database,
        the registration will fail.
        :param public_key:
        :return:
        """
        # Check if the public key is valid (e.g., correct length for RSA keys)
        if len(public_key) != 32:
            raise InvalidPublicKeyError("Public key must be 32 bytes long.")
        if not validate_public_key(public_key):
            raise InvalidPublicKeyError("Invalid public key format.")

        # Check if the public key already exists in the database
        pubkey_fingerprint = hashlib.sha256(public_key).hexdigest()
        query = "SELECT * FROM users WHERE fingerprint = ?"
        result = self._execute_query(query, (pubkey_fingerprint,))
        if result:
            raise UserAlreadyExistsError(pubkey_fingerprint)

        # Insert the new user into the database
        query_users = "INSERT INTO users (user_id, public_key, fingerprint) VALUES (?, ?, ?)"
        user_id = uuid.uuid4()
        self._execute_query(query_users, (user_id.hex, public_key, pubkey_fingerprint,))
        return user_id

    def get_public_key(self, user_id: str) -> bytes:
        """
        Retrieves the public key for a given user ID.
        :param user_id:
        :return:
        """
        query = "SELECT public_key FROM users WHERE user_id = ?"
        result = self._execute_query(query, (user_id,))
        if result:
            return result[0][0]
        raise UserIDNotFoundError(user_id)

    def _execute_query(self, query, params=None) -> List[Any]:
        """
        Executes a SQL query with optional parameters and returns the result.
        :param query:
        :param params:
        :return:
        """
        if not self.connection:
            raise Exception("Database connection is not established.")

        cursor: sqlite3.Cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result
