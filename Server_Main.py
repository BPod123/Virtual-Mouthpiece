import os
from app import main as appMain
from threading import Thread
from Server import ServerInstance
def startReact():
    os.system("yarn --cwd virtual-mouthpiece start")
def startApp():
    appMain()
def main():
    ServerInstance.server.start()
    Thread(target=startReact).start()
    startApp()
if __name__ == '__main__':
    main()