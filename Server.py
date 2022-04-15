import socket
from threading import Thread, Lock
from math import ceil, log2


class MainServer(object):
    def __init__(self, port, getRequestPort):
        self.port = port
        self.getRequestPort = getRequestPort
        self.connectionLock = Lock()
        self.connections = {}
        self.onChangeCallback = None  # Callback for when a connection is added or removed
        self.ipaddress = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket()
        self.sock.bind((self.ipaddress, self.port))
        self.getRequestSock = socket.socket()
        self.getRequestSock.bind((self.ipaddress, self.getRequestPort))

    def handleConnection(self, connectionSocket: socket.socket, addr: tuple):
        name = self.receiveBytes(connectionSocket).decode()
        self.connections[name] = addr, connectionSocket
        self.connectionLock.release()

    def acceptGetRequestConnections(self, acceptor: socket.socket):
        """
        Handles get requests to get the list of billboard names
        """
        acceptor.listen(10)
        while True:
            connectionSocket, addr = acceptor.accept()
            retString = ";;".join(list(self.connections.keys()))
            if retString == "":
                retString = "No Displays Connected"
            connectionSocket.send(retString.encode())
            connectionSocket.close()

    def acceptConnections(self, acceptor: socket.socket):
        acceptor.listen(10)
        while True:
            connectionSocket, addr = acceptor.accept()
            self.connectionLock.acquire()
            Thread(target=self.handleConnection, args=(connectionSocket, addr)).start()

    def start(self):
        Thread(target=self.run).start()

    def run(self):

        Thread(target=self.acceptConnections, args=(self.sock,)).start()
        Thread(target=self.acceptGetRequestConnections, args=(self.getRequestSock,)).start()

    @staticmethod
    def receiveBytes(connectionSocket: socket.socket):
        """
        :param connectionSocket: socket connected to a sender
        :return: any information sent by sender
        """
        while True:
            recv = connectionSocket.recv(1024)
            if not recv:
                break
            yield recv
        # numBytes = int()
        #
        # recv = connectionSocket.recv(1024).decode()
        # connectionSocket.send("".encode())
        # twoPow = int(2 ** ceil(log2(14)))
        # bufferSize = twoPow if twoPow - numBytes < 2048 else numBytes + 2048
        information = connectionSocket.recv(1024)
        return information

    def sendSlideshow(self, name, zipPath: str):
        self.connectionLock.acquire()
        connectionSocket = self.connections[name][1]
        with open(zipPath, 'rb') as f:
            connectionSocket.sendfile(f)
        self.connectionLock.release()

        # breakpoint()

    @staticmethod
    def sendBytes(connectionSocket: socket.socket, information: bytes):
        connectionSocket.send(str(len(information)).encode())
        _ = connectionSocket.recv(1024)
        connectionSocket.send(information)


#
# @staticmethod
# def sendFile(connectionSocket: socket.socket, information: bytes, isFile: bool):
#     """
#     :param connectionSocket: socket connected to a receiver
#     :return: any information sent by sender
#     """
#     numBytes = len(information)
#     connectionSocket.sendfile()
# connectionSocket = self.connections[addr][1]
# Send first the number of bytes that are about to be sent,
# so the receiver can allocate a buffer of appropriate size
# connectionSocket.send(str(len(information)).encode())
# connectionSocket.send(information)


if __name__ == '__main__':
    ipaddress = socket.gethostbyname(socket.gethostname())
    port = 9005
    server = MainServer(port)
    server.run()
    # breakpoint()
    # from time import sleep

    # sleep(0.1)
    # sock = socket.socket()
    # sock.bind((ipaddress, 9002))
    # sock.connect((ipaddress, 9001))
    # sock.send("Test Name".encode())
    # breakpoint()
