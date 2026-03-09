import logging
import socket
import threading
from sqlite3 import Error as SQLiteError

from .message import Message
from .database import Database
from .errors import *


class Server:
    SERVER_ADDRESS = '0.0.0.0'
    SERVER_PORT = 843

    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clients = []
        self._client_threads = []

        self.database = None

        self.logger = None

        self._running = False

    def start(self):
        """
        Starts the server socket and initializes the database connection. If the database file does not exist, it will be created and initialized.
        :return:
        """
        self.logger = logging.getLogger("prencrypt-server")
        self.log(f"Starting server on {Server.SERVER_ADDRESS}:{Server.SERVER_PORT}")
        self._sock.bind((Server.SERVER_ADDRESS, Server.SERVER_PORT))
        self.debugmsg(f"Server started with socket bound to address {self._sock.getsockname()}")
        self._sock.listen()
        self.database = Database('database.db')
        self.database.connect()
        try:
            self.database.initialize_database()
        except SQLiteError as e:
            pass  # database already initialized
        self._running = True

    def stop(self):
        """
        Stops the server and closes all client connections.
        :return:
        """
        self._running = False
        for client in self._clients:
            client.close()
        self.database.disconnect()
        self._sock.close()

    def handle_client(self, client: socket.socket):
        """
        Per client management thread. Processes messages from the client and acts accordingly.
        :param client:
        :return:
        """
        while self._running:
            message = client.recv(1024)
            if not message:
                continue
            parsed_message: Message = Message.parse_message(message)
            if parsed_message.opcode == "0x11":
                # register new user
                error = ""
                try:
                    self.database.register_new_user(parsed_message.data)
                except SQLiteError as e:
                    self.logger.error(e.sqlite_errorname)
                    error = "Internal server error"
                except UserAlreadyExistsError as e:
                    self.logger.error(f"Failed to register user with public key fingerprint {e.public_key_fp}: {str(e)}")
                    error = "Public key already registered"
                except InvalidPublicKeyError as e:
                    self.logger.error(f"Failed to register user with invalid public key: {str(e)}")
                    error = "Invalid public key"

                if error:
                    error_message = Message("0xFF", parsed_message.userid, b'', error.encode()).as_bytes
                    client.send(error_message)
            else:
                pass

    def accept_connections(self):
        while self._running:
            client, address = self._sock.accept()
            self._clients.append(client)
            self._client_threads.append(threading.Thread(target=self.handle_client, args=(client,)))

    def log(self, message: str):
        if self.logger:
            self.logger.info(message)

    def debugmsg(self, message: str):
        if self.logger:
            self.logger.debug(message)
