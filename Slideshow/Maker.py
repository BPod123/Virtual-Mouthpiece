import json
import os
import shutil

from Slideshow.Format_Slideshow import emptyDirectory
from concurrent.futures import ThreadPoolExecutor


def saveFile(src, dest, durationSeconds):
    shutil.copy(src, dest)
    return {'path': os.path.basename(dest), 'seconds': durationSeconds}


def compileSlideshow(folderPath, pathSeconds):
    """
    Compiles slideshow folder into a zipped folder and remove folderPath

    :param folderPath: The name of the folder you want to store the slideshow in
    :param pathSeconds: iterable tuples (src to .npy file, amount of time to display)
    Creates a zipped folder with all the images/videos
    In the folder, there will be a json file named info.json that contains a list of dicts. Inside each dict is a mapping
    "src": relative src of the file withing the folder, "seconds": the amount to seconds to display item for
    :return The src of the zipped workingDir
    """
    if not os.path.isdir(folderPath):
        os.mkdir(folderPath)

    savedInfoFutures = []

    executor = ThreadPoolExecutor()
    for src, seconds in pathSeconds:
        dest = os.path.basename(src)
        # Copy files to new destination and append items list
        savedInfoFutures.append(executor.submit(saveFile, src, os.path.join(folderPath, dest), seconds))
    executor.shutdown()
    info = [x.result() for x in savedInfoFutures]
    infoPath = os.path.join(folderPath, "info.json")

    # saveFile = os.src.join(folderPath, "info.json")
    with open(infoPath, "w") as f:
        json.dump(info, f, indent=4)
    # Zip file
    shutil.make_archive(folderPath, 'zip', folderPath)
    # Delete unzipped file as it is no longer necessary
    emptyDirectory(folderPath)
    os.removedirs(folderPath)
    return folderPath + ".zip"
