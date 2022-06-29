import socket
import json


class SocketClient:
    def __init__(self, port):
        self.port = port
        self.server = socket.socket()
        self.server.connect(("127.0.0.1", self.port))

    def send(self, msg):
        self.server.send(msg)

    def recv(self):
        print(self.server.recv(4096))


if __name__ == '__main__':
    client = SocketClient(9999)
    msgObj = dict()
    msgObj["action"] = "list_pocs"
    for i in range(3):
        client.send(json.dumps(msgObj).encode())
        client.recv()
