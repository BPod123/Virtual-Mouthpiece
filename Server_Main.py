import os
from app import main as appMain
from threading import Thread
from Server import MainServer
from time import sleep
def startReact():
    os.system("yarn --cwd virtual-mouthpiece start")
def startApp():
    appMain()

if __name__ == '__main__':
    server = MainServer(9001, 9002)
    server.start()
    # sleep(1)
    Thread(target=startReact).start()
    # Thread(target=startApp).start()
    startApp()