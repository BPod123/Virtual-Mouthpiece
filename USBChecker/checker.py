import time
import os

while True:
    #print("top of while loop")
    time.sleep(5)
    arr = os.listdir('/media/pi') 
    print(arr)
