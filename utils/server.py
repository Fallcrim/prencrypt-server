import socket
import threading
import os

from .message import Message
from .database import Database


class Server:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clients = []
        self._client_threads = []

        self.database = None

        self._running = False

    def start(self):
        """
        Starts the server socket and initializes the database connection. If the database file does not exist, it will be created and initialized.
        :return:
        """
        self._sock.bind(('0.0.0.0', 843))
        self._sock.listen()
        self.database = Database('database.db')
        self.database.connect()
        if not os.path.isfile('database.db'):
            self.database.initialize_database()
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
        while self._running:
            message = client.recv(1024)
            if not message:
                continue
            parsed_message: Message = Message.parse_message(message)
            if parsed_message.opcode == "0x11":
                # register new user
                success = self.database.register_new_user(parsed_message.data)
                if not success:
                    error_message = Message("0xFF", parsed_message.userid, b'', b'Public key already exists').as_bytes
                    client.send(error_message)
            else:
                pass

    def accept_connections(self):
        while self._running:
            client, address = self._sock.accept()
            self._clients.append(client)
            self._client_threads.append(threading.Thread(target=self.handle_client, args=(client,)))
