import os
import socket
from threading import Thread, Lock
from math import ceil, log2
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from Slideshow.Maker import compileSlideshow


class Server(object):
    def __init__(self, port):
        self.port = port
        # self.getRequestPort = getRequestPort
        self.connectionLock = Lock()
        self.connections = {}
        self.onChangeCallback = None  # Callback for when a connection is added or removed
        self.ipaddress = socket.gethostbyname(socket.gethostname())
        self.sock = socket.socket()
        self.sock.bind((self.ipaddress, self.port))
        # self.getRequestSock = socket.socket()
        # self.getRequestSock.bind((self.ipaddress, self.getRequestPort))
        self.slideshowCompileFolder = "slideshowCompileFolder"
        self._shuttingdown = False

    @property
    def running(self):
        return not self._shuttingdown

    def shutdown(self):
        self._shuttingdown = True

    def handleConnection(self, connectionSocket: socket.socket, addr: tuple):

        name = connectionSocket.recv(1024).decode()
        sockLock = Lock()
        self.connectionLock.acquire()
        self.connections[addr] = name, connectionSocket, sockLock
        self.connectionLock.release()
        while self.running:
            sleep(2)
            sockLock.acquire()
            isAlive = self.checkIfAlive(connectionSocket)
            if not isAlive:
                self.connectionLock.acquire()
                self.connections.pop(addr)
                self.connectionLock.release()
                sockLock.release()
                break
            sockLock.release()






    # def acceptGetRequestConnections(self, acceptor: socket.socket):
    #     """
    #     Handles get requests to get the list of billboard names
    #     """
    #     acceptor.listen(10)
    #     while True:
    #         connectionSocket, addr = acceptor.accept()
    #         retString = ";;".join(list(self.connections.keys()))
    #         if retString == "":
    #             retString = "No Displays Connected"
    #         connectionSocket.send(retString.encode())
    #         connectionSocket.shutdown(socket.SHUT_RDWR)
    #         connectionSocket.close()


    @staticmethod
    def checkIfAlive(connectionSocket: socket.socket):
        try:
            connectionSocket.settimeout(2)
            connectionSocket.send("A".encode())
            resp = connectionSocket.recv(1).decode()
            connectionSocket.settimeout(None)
            return True
        except:
            return False

    def acceptConnections(self, acceptor: socket.socket):
        acceptor.listen(10)
        while True:
            connectionSocket, addr = acceptor.accept()
            Thread(target=self.handleConnection, args=(connectionSocket, addr)).start()

    def start(self):
        Thread(target=self.run).start()

    def run(self):

        Thread(target=self.acceptConnections, args=(self.sock,)).start()
        # Thread(target=self.acceptGetRequestConnections, args=(self.getRequestSock,)).start()
        # Thread(target=self.updateLiveConnections).start()

    @staticmethod
    def sendBytes(connectionSocket: socket.socket, information: bytes):
        connectionSocket.send(str(len(information)).encode())
        _ = connectionSocket.recv(1024)
        connectionSocket.send(information)

    @staticmethod
    def sendSlideshow(conInfo, zippedFolderPath):
        name, connectionSocket, socketLock = conInfo[:3]
        ex = None
        socketLock.acquire()
        try:
            connectionSocket.send("F".encode())
            with open(zippedFolderPath, "rb") as file:
                while True:
                    bytes = file.read(1024)
                    if not bytes:
                        # The server will wait for acknowledgement from the display manager that it has finished
                        # recieving the file
                        connectionSocket.settimeout(5)
                        try:
                            recv = connectionSocket.recv(1).decode()
                        except:
                            raise Exception(f"{name} did not send confirmation that it received the slideshow.")
                        finally:
                            connectionSocket.settimeout(None)
                        break
                    connectionSocket.send(bytes)
        except Exception as e:
            ex = e
        finally:
            socketLock.release()
        return ex

    def compileAndSendSlideshow(self, args):
        files, boards, title, runTimes = args.images, set(args.boards), args.title, args.runtimes
        fileSeconds = zip(files, runTimes)
        zippedFolderPath = compileSlideshow(self.slideshowCompileFolder, fileSeconds, title)
        self.connectionLock.acquire()
        conInfos = [self.connections[addr] for addr in self.connections if
                           self.connections[addr][0] in boards]
        self.connectionLock.release()
        executor = ThreadPoolExecutor()
        futures = [executor.submit(self.sendSlideshow, conInfo, zippedFolderPath) for conInfo
                   in conInfos]
        executor.shutdown()
        os.remove(zippedFolderPath)
        results = [future.result() for future in futures]
        exceptions = [ex for ex in results if ex is not None]
        return exceptions


class ServerInstance(object):
    server = Server(9001)


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
    server = Server(port)
    server.run()
    # breakpoint()
    # from time import sleep

    # sleep(0.1)
    # sock = socket.socket()
    # sock.bind((ipaddress, 9002))
    # sock.connect((ipaddress, 9001))
    # sock.send("Test Name".encode())
    # breakpoint()
