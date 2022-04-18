import time

from Manager import Manager
from Slideshow.Maker import compileSlideshow
from time import sleep
from threading import Thread
from Server_Main import main as startServerSide, ServerInstance
def ManagerThread():
    manager = Manager('BACKEND_TESTS', "Config.json")
    manager.start()
    pass

def shutoffManagerAfterWait(mangager: Manager, waitTime):
    sleep(waitTime)
    print("Stopping Manager")
    mangager.shutdown()
    sleep(30)
    print("Restarting Manager")
    mangager._shuttingDown = False
    mangager.start()
    sleep(5)


def runTests(tests: list):
    for test, args in tests:
        test(*args)




if __name__ == '__main__':
    # fileNames = [
    #     r'C:\Users\Ben\Documents\Georgia Tech\Georgia_Tech\2022 Spring\Junior Design\Slideshow\Old_Stuff\mp4Video.mp4',
    #     r'C:\Users\Ben\Documents\Georgia Tech\Georgia_Tech\2022 Spring\Junior Design\Slideshow\Old_Stuff\still image.jpg',
    #     r'C:\Users\Ben\Documents\Georgia Tech\Georgia_Tech\2022 Spring\Junior Design\Slideshow\Old_Stuff\FirstWin.gif'
    # ]
    # times = [2, 5, 10]
    # pathMillis = zip(fileNames, times)
    # zipPath = compileSlideshow('myshow', pathMillis)
    # Thread(target=ManagerThread).start()
    # Thread(target=serverThread).start()
    manager1 = Manager('BACKEND_TESTS/Manager1', "BACKEND_TESTS/Config1.json")
    manager2 = Manager("BACKEND_TESTS/Manager2", "BACKEND_TESTS/Config2.json")

    manager1.start()
    manager2.start()
    tests = [
        (shutoffManagerAfterWait, (manager2, 10))
    ]
    Thread(target=runTests, args=(tests))
    Thread(target=shutoffManagerAfterWait, args=(manager2, 10)).start()
    startServerSide()

    z = 3

