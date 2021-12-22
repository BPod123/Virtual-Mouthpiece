# tutorial at https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
import socket, tqdm, os
from threading import Thread
def recieveFiles():
    while True:
        try:
            # device's IP address
            SERVER_HOST = "0.0.0.0"
            SERVER_PORT = 5001
            # receive 4096 bytes each time
            BUFFER_SIZE = 4096
            SEPARATOR = "<SEPARATOR>"

            # create the server socket
            # TCP socket
            s = socket.socket()

            # bind the socket to our local address
            s.bind((SERVER_HOST, SERVER_PORT))

            # enabling our server to accept connections
            # 5 here is the number of unaccepted connections that
            # the system will allow before refusing new connections
            s.listen(5)
            print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

            # accept connection if there is any
            client_socket, address = s.accept()
            # if below code is executed, that means the sender is connected
            print(f"[+] {address} is connected.")

            # receive the file infos
            # receive using client socket, not server socket
            received = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            # remove absolute path if there is
            filename = os.path.abspath('RecievedFile/{0}'.format(os.path.basename(filename)))
            # convert to integer
            filesize = int(filesize)

            # start receiving the file from the socket
            # and writing to the file stream
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)
                    # update the progress bar
                    progress.update(len(bytes_read))

            # close the client socket
            client_socket.close()
            # close the server socket
            s.close()
            # https://code-with-me.jetbrains.com/yhPTNhKptyay9Jc-cJ4tow#p=PY&fp=7EBDD41414B7EEEB447C295DF886716C85F39C4E8DAD291095D53A20F7AEAABD
        except:
            pass
def startRecievingFiles():
    fileRecieveThread = Thread(target=recieveFiles)
    fileRecieveThread.start()




if __name__ == '__main__':
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    # create the server socket
    # TCP socket
    s = socket.socket()

    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))

    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.abspath('RecievedFile/{0}'.format(os.path.basename(filename)))
    # convert to integer
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()
    #https://code-with-me.jetbrains.com/yhPTNhKptyay9Jc-cJ4tow#p=PY&fp=7EBDD41414B7EEEB447C295DF886716C85F39C4E8DAD291095D53A20F7AEAABD
