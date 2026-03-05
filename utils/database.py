import hashlib
import sqlite3
import uuid
from typing import Any, List


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = None

    def connect(self) -> None:
        """
        Establishes a connection to the SQLite database specified by db_name.
        :return:
        """
        self.connection = sqlite3.connect(self.db_name)

    def disconnect(self) -> None:
        """
        Closes the database connection if it is open.
        :return:
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize_database(self) -> None:
        """
        Initializes the database by creating the necessary tables. The schema is defined in the 'schema.sql' file.
        :return:
        """
        if not self.connection:
            raise Exception("Database connection is not established.")

        cursor = self.connection.cursor()
        with open('schema.sql', 'r') as f:
            schema = f.read()
        cursor.executescript(schema)
        self.connection.commit()

    def register_new_user(self, public_key: bytes) -> bool:
        """
        Registers a new user with the given public key. If the public key already exists in the database,
        the registration will fail.
        :param public_key:
        :return:
        """
        # Check if the public key already exists in the database
        pubkey_fingerprint = hashlib.sha256(public_key).hexdigest()
        q = "SELECT * FROM user_public_keys WHERE fingerprint = ?"
        result = self._execute_query(q, (pubkey_fingerprint,))
        if result:
            return False

        # Insert the new user into the database
        q_users = "INSERT INTO users (user_id) VALUES (?)"
        q_user_public_keys = "INSERT INTO user_public_keys (user_id, public_key, fingerprint) VALUES (?, ?, ?)"
        self._execute_query(q_users, (pubkey_fingerprint,))
        self._execute_query(q_user_public_keys, (uuid.uuid4().hex, public_key, pubkey_fingerprint,))
        return True

    def get_public_key(self, user_id: str) -> bytes:
        """
        Retrieves the public key for a given user ID.
        :param user_id:
        :return:
        """
        q = "SELECT public_key FROM user_public_keys WHERE user_id = ?"
        result = self._execute_query(q, (user_id,))
        if result:
            return result[0][0]
        return None

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
