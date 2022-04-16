"""
Manager controls the billboard computer. It handles sending and receiving files and contains the Player object
for controlling what is on the screen.
"""
from enum import Enum
import json
from threading import Thread, Lock
import os
import socket
import shutil
from time import sleep, time
from Slideshow import Player, Slideshow
import cv2


class ConfigProps(Enum):
    SERVER_ADDR = "SERVER_ADDRESS"
    SERVER_PORT = "SERVER_PORT"
    HOST_PORT = "HOST_PORT"
    NAME = "NAME"
    HEIGHT = "HEIGHT"
    WIDTH = "WIDTH"
    TRANSITION_DURATION = "TRANSITION_DURATION"


class Manager(object):
    def __init__(self, workingDir: str, configPath):
        """
        :param workingDir: String to directory to work within
        :param configPath: Path to configuration file. If None, will search for Config.json in working directory
        Makes the working directory if it doesn't exist yet and initializes private variables
        """

        self.fileDeleteLock = Lock()
        self.workingDir = workingDir

        if not os.path.exists(self.workingDir):
            os.makedirs(self.workingDir)

        self.configPath = os.path.join(self.workingDir, "Config.json")
        self.configBackupPath = os.path.join(self.workingDir, "Config_backup.json")
        if not os.path.exists(self.workingDir) or not os.path.isdir(self.workingDir):
            os.makedirs(self.workingDir)
        if configPath is not None and os.path.isfile(configPath) and os.path.abspath(configPath) != os.path.abspath(
                self.configPath):
            shutil.copyfile(configPath, self.configPath)

        self.slideshowWorkingDir = os.path.join(self.workingDir, "Current Show")
        self.ipaddress = socket.gethostbyname(socket.gethostname())
        self._name = f"{socket.gethostname()}, {self.ipaddress}"  # self.config[ConfigProps.NAME.value] if ConfigProps.NAME.value in self.config else "Name not found: {0}".format(socket.gethostname())
        self._serverAddr = None  # if ConfigProps.SERVER_ADDR.value not in self.config else self.config[ConfigProps.SERVER_ADDR.value]
        self._serverPort = None  # if ConfigProps.SERVER_PORT.value not in self.config else self.config[ConfigProps.SERVER_PORT.value]
        self._hostPort = None  # if ConfigProps.HOST_PORT.value not in self.config else self.config[ConfigProps.HOST_PORT.value]
        self._height = 100  # if ConfigProps.HEIGHT.value not in self.config else self.config[ConfigProps.HEIGHT.value]
        self._width = 100  # if ConfigProps.WIDTH.value not in self.config else self.config[ConfigProps.WIDTH.value]
        self._transitionDuration = 2  # if ConfigProps.TRANSITION_DURATION.value not in self.config else self.config[ConfigProps.TRANSITION_DURATION.value]
        self.config = self.loadConfig(self.configPath)
        self.setValues(self.config)
        self._player = None
        self.zippedSlideshowPath = os.path.join(self.workingDir, "slideshow.zip")
        self._connectionSettingsChanged = True  # Updated when the server ip, server port, or host port change
        self._connectionStartTime = None  # Used to signal when the connection to the server has been reset
        self.needPlayReset = False

    @property
    def player(self):
        if self._player is None:
            self._player = Player(self.name, self.transitionDuration)
        return self._player

    @player.setter
    def player(self, value):
        if self._player is not None:
            self.player.stop()
            if self.player.slideshow is not None:
                self.player.slideshow.collapse()
                while not self.player.isStopped:
                    sleep(1)
                cv2.destroyAllWindows()
        self._player = value

        pass

    @property
    def serverAddr(self):
        return self._serverAddr

    @serverAddr.setter
    def serverAddr(self, value):
        if self.serverAddr != value:
            self._serverAddr = value
            self._connectionSettingsChanged = True

    @property
    def serverPort(self):
        return self._serverPort

    @serverPort.setter
    def serverPort(self, value):
        if self.serverPort != value:
            self._serverPort = value
            self._connectionSettingsChanged = True

    @property
    def hostPort(self):
        return self._hostPort

    @hostPort.setter
    def hostPort(self, value):
        if self.hostPort != value:
            self._hostPort = value
            self._connectionSettingsChanged = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

    @property
    def transitionDuration(self):
        return self._transitionDuration

    @transitionDuration.setter
    def transitionDuration(self, value):
        self._transitionDuration = value

    def generateConfig(self):
        return {
            ConfigProps.SERVER_ADDR.value: self.serverAddr,
            ConfigProps.SERVER_PORT.value: self._serverPort,
            ConfigProps.HOST_PORT.value: self.hostPort,
            ConfigProps.NAME.value: self.name,
            ConfigProps.HEIGHT.value: self.height,
            ConfigProps.WIDTH.value: self.width,
            ConfigProps.TRANSITION_DURATION.value: self.transitionDuration,
        }

    def setValues(self, valueDict: dict):
        """
        :param valueDict: Dict mapping ConfigProps to values
        Any key value pairs in dict will have their attributes updated.
        """
        keyAttrDict = {
            ConfigProps.SERVER_ADDR.value: 'serverAddr',
            ConfigProps.SERVER_PORT.value: 'serverPort',
            ConfigProps.HOST_PORT.value: 'hostPort',
            ConfigProps.NAME.value: 'name',
            ConfigProps.HEIGHT.value: 'height',
            ConfigProps.WIDTH.value: 'width',
            ConfigProps.TRANSITION_DURATION.value: 'transitionDuration',
        }
        for key in keyAttrDict:
            if key in valueDict:
                attr = keyAttrDict[key]
                setattr(self, attr, valueDict[key])

    def saveConfig(self):
        with open(self.configPath, "w") as f:
            json.dump(self.config, f, indent=4)

    def loadConfig(self, path=None):
        """
        :param path: If none, will load from self.configPath (self.workingDir/Config.json) else will load from path
        :return: The config dict
        """
        path = path if path is not None else self.configPath
        with open(path, "r") as f:
            config = json.load(f)
        return config

    def resetPlayer(self):
        self.player = Player(self.name, self.transitionDuration)
        if os.path.isfile(self.zippedSlideshowPath):
            self.player.slideshow = Slideshow(self.zippedSlideshowPath, self.slideshowWorkingDir, self.width,
                                              self.height, self.fileDeleteLock)
            self.player.playThread.start()

    def refresh(self):
        """
        Checks for any changes in property values and acts accordingly
        """
        # A value has been changed. Need to rewrite the config file and possibly more
        # Create a new config from the currently set values
        newConfig = self.generateConfig()
        if self.config != newConfig or self._connectionSettingsChanged:
            # A change to the config has been made, or the connection settings have been changed
            # This also happens on the first call of the function
            # Save the current config as a backup then make and save changes
            with open(self.configBackupPath, "w") as f:
                json.dump(self.config, f, indent=4)
            self.config = newConfig
            self.saveConfig()
            if self.needPlayReset:
                self.needPlayReset = False
                self.resetPlayer()


            if self._connectionSettingsChanged:
                self._connectionSettingsChanged = False
                self.resetConnection()

    def resetConnection(self):
        """
        Resets the connection with the server
        """
        self._connectionStartTime = time()
        Thread(target=self.manageConnection).start()

    def receptionHandler(self, connectionSocket: socket.socket, startTime):
        connectionSocket.settimeout(20)
        try:
            while self._connectionStartTime == startTime:
                messageType = connectionSocket.recv(1).decode()
                if messageType == "A":
                    connectionSocket.send("Y".encode())
                else:
                    if messageType == "F":
                        # Recieving new slideshow
                        with open(self.zippedSlideshowPath, "wb") as f:
                            while True:
                                newBytes = connectionSocket.recv(1024)
                                if not newBytes:
                                    break
                                f.write(newBytes)
                        self.needPlayReset = True

                    elif messageType == "N":
                        # Recieving new Name
                        newName = connectionSocket.recv(1024).decode()
                        self.name = newName
                        self.needPlayReset = True
        except:
            pass
        connectionSocket.close()

    def manageConnection(self):
        """
        Initiates the connection to the server and sends its config data. Then acts upon messages sent from the server.
        """
        thisStartTime = self._connectionStartTime
        if self.serverAddr is not None and self.serverPort is not None and self.hostPort is not None:
            while thisStartTime == self._connectionStartTime:
                connectionSocket = socket.socket()
                try:
                    connectionSocket.bind((self.ipaddress, self.hostPort))
                    # Initiate connection, or at least attempt to
                    connectionSocket.connect((self.serverAddr, self.serverPort))
                    # connectionSocket.send(str(len(str(self.name).encode())).encode())
                    # _ = connectionSocket.recv(1024).decode()
                    connectionSocket.send(self.name.encode())
                    Thread(target=self.receptionHandler, args=(connectionSocket, thisStartTime)).start()
                except:
                    continue

    def start(self):
        Thread(target=self.run).start()

    def run(self):
        self._connectionSettingsChanged = True
        while True:
            self.refresh()
            sleep(1)
    @staticmethod
    def sendBytes(connectionSocket: socket.socket, information: bytes):
        connectionSocket.send(str(len(information)).encode())
        _ = connectionSocket.recv(1024)
        connectionSocket.send(information)

    def __del__(self):
        self._connectionStartTime = time()


if __name__ == '__main__':
    manager = Manager('Test Manager Working Directory', os.path.join('Test Manager Working Directory',
                                                                     'BACKEND_TESTS/Config1.json'))
    manager.run()
