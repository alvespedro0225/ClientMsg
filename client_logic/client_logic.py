import socket
from contextlib import contextmanager
from .info import SERVER

class ClientConnector:

    @classmethod
    @contextmanager
    def socket_connect(cls, server_address):
        mysocket = socket.create_connection(server_address)
        try:
            yield mysocket
        finally:
            mysocket.close()
            print('Closed')

    @classmethod
    def send_message(cls, message, server_address=SERVER):
        with cls.socket_connect(server_address) as SOCKET:
            for value in message:   
                SOCKET.send(bytes((value+'ṕ'), 'UTF-8'))