from Manager import Manager
from Server import MainServer
from Slideshow.Maker import compileSlideshow
from time import sleep
from threading import Thread
def ManagerThread():
    manager = Manager('Test Manager Working Directory', "Config.json")
    manager.start()
    pass

def serverThread():
    port = 9005
    slideshowPath = "myshow.zip"
    server = MainServer(port)
    server.start()
    sleep(5)
    # server.sendSlideshow("Display Test", slideshowPath)




if __name__ == '__main__':
    # fileNames = [
    #     r'C:\Users\Ben\Documents\Georgia Tech\Georgia_Tech\2022 Spring\Junior Design\Slideshow\Old_Stuff\mp4Video.mp4',
    #     r'C:\Users\Ben\Documents\Georgia Tech\Georgia_Tech\2022 Spring\Junior Design\Slideshow\Old_Stuff\still image.jpg',
    #     r'C:\Users\Ben\Documents\Georgia Tech\Georgia_Tech\2022 Spring\Junior Design\Slideshow\Old_Stuff\FirstWin.gif'
    # ]
    # times = [2, 5, 10]
    # pathMillis = zip(fileNames, times)
    # zipPath = compileSlideshow('myshow', pathMillis)
    Thread(target=ManagerThread).start()
    Thread(target=serverThread).start()

    z = 3

