import socket
import threading


class Server:
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._clients = []
        self._client_threads = []

        self._running = False

    def start(self):
        self._sock.bind(('0.0.0.0', 843))
        self._sock.listen()
        self._running = True

    def stop(self):
        self._sock.close()

    def handle_client(self, client):
        pass

    def accept_connections(self):
        while self._running:
            client, address = self._sock.accept()
            self._clients.append(client)
            self._client_threads.append(threading.Thread(target=self.handle_client, args=(client,)))
