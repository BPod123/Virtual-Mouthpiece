"""
This file is for run by the client (Billboard) computer to format the slideshow to its resolution at play time
"""
import os
import zipfile
from threading import Thread
import numpy as np
from multiprocessing import Pool, cpu_count
from PIL import Image, ImageSequence
import json
import cv2
from Slideshow.resize_GIF import resize_gif
from time import sleep
def getGifFrames(gif: str):
    """
    :param gif: The gif file path
    :return: An array of images of the desired dimension
    """
    gifFrames = np.array(
        [np.array(frame.copy().convert('RGB').getdata(), dtype=np.uint8).reshape(frame.size[1], frame.size[0], 3) for
         frame in ImageSequence.Iterator(Image.open(gif))])
    return gifFrames


def resizeImageVideo(src, dest, width, height):
    if src.lower()[src.rfind('.') + 1:] in ['jpg', 'jpeg', 'png']:
        if not os.path.isfile(src):
            breakpoint()
        Image.open(src).resize((width, height)).save(dest)
        fps = 1
        numFrames = 1
    elif src.lower().endswith('gif'):
        resize_gif(src, dest, (width, height))
        c = cv2.VideoCapture(src)
        fps = c.get(cv2.CAP_PROP_FPS)
        numFrames = c.get(cv2.CAP_PROP_FRAME_COUNT)
        c.release()
    else:
        cap = cv2.VideoCapture(src)
        fps = cap.get(cv2.CAP_PROP_FPS)
        numFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        ret, frame = cap.read()
        out = cv2.VideoWriter(dest, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
        while ret:
            newFrame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            out.write(newFrame)
            ret, frame = cap.read()
        out.release()
        cap.release()
    # os.remove(src)


    return numFrames, fps



def formatSlideshow(zippedSrc, unzippedDest, width, height):
    """
    :param zippedSrc: Path to zipped folder containing a slideshow
    :param unzippedDest: Path to where the finished slideshow folder should go
    :param width: The width of the viewing window
    :param height: The height of the viewing window
    :return: unzippedDest - The src to the folder for the playable slideshow
    """
    unzippedUnformatedDir = os.path.join(unzippedDest, "Unformatted")
    if not os.path.exists(unzippedUnformatedDir) or not os.path.isdir(unzippedUnformatedDir):
        os.makedirs(unzippedUnformatedDir)
    unzipDirectory(zippedSrc, unzippedUnformatedDir)
    # Load the config file
    infoPath = os.path.join(unzippedUnformatedDir, "info.json")
    newInfoPath = os.path.join(unzippedDest, "info.json")
    with open(infoPath, "r") as f:
        data = json.load(f)
    os.remove(infoPath)

    finalData = [x.copy() for x in data]
    # Update all the file paths in data
    for i in range(len(data)):
        finalData[i]['path'] = os.path.join(unzippedDest, data[i]['path'])
        # if data[i]['src'].lower().endswith('.gif'):
        #     data[i]['src'] = data[i]['src'][:-3] + 'mp4'


    # Resize images/videos and remove unformatted directory
    results = [resizeImageVideo(os.path.join(unzippedUnformatedDir, data[i]['path']), finalData[i]['path'], width, height) for i in range(len(data))]
    for i in range(len(results)):
        numFrames, fps = results[i]
        finalData[i]['numFrames'], finalData[i]['fps'] = numFrames, fps
    # pool = Pool(int(min(len(data), cpu_count())))
    # asyncResults =[pool.apply_async(resizeImageVideo,
    #                   args=(os.path.join(unzippedUnformatedDir, data[i]['path']), finalData[i]['path'], width, height
    #                         )) for
    #  i in range(len(data))]
    # pool.close()
    # pool.join()
    # for i in range(len(data)):
    #     numFrames, fps = asyncResults[i].get()
    #     finalData[i]['numFrames'], finalData[i]['fps'] = numFrames, fps
    emptyDirectory(unzippedUnformatedDir)
    # os.removedirs(unzippedUnformatedDir)
    with open(newInfoPath, "w") as f:
        json.dump(finalData, f, indent=4)



    return finalData, newInfoPath


def unzipDirectory(src, dest):
    """
    :param src: src to zipped workingDir
    :param dest: new src to unzipped workingDir
    """
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
        with zipfile.ZipFile(src, 'r') as zipped:
            zipped.extractall(dest)
    except:
        sleep(2)
        if not os.path.exists(dest):
            os.makedirs(dest)
        with zipfile.ZipFile(src, 'r') as zipped:
            zipped.extractall(dest)


def emptyDirectory(folderPath):
    for item in os.listdir(folderPath):
        path = os.path.join(folderPath, item)
        if os.path.isfile(path):
            os.remove(path)
        else:
            try:
                emptyDirectory(path)
                if os.path.exists(path) and len(os.listdir(path)) == 0:
                    os.removedirs(os.path.join(folderPath, item))
            except:
                breakpoint()

