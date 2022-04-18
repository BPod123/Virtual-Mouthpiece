import json
import os
import shutil

from Slideshow.Format_Slideshow import emptyDirectory
from concurrent.futures import ThreadPoolExecutor


def saveFile(file, dest, durationSeconds):
    with open(dest, "wb") as f:
        f.write(file.read())
    return {'path': os.path.basename(dest), 'seconds': durationSeconds}


def compileSlideshow(folderPath, fileSeconds, title: str):
    """
    Compiles slideshow folder into a zipped folder and remove folderPath

    :param folderPath: The name of the folder you want to store the slideshow in
    :param fileSeconds: iterable tuples (file reader object, seconds to display for)
    Creates a zipped folder with all the images/videos
    In the folder, there will be a json file named info.json that contains a list of dicts. Inside each dict is a mapping
    "src": relative src of the file withing the folder, "seconds": the amount to seconds to display item for
    :return The src of the zipped workingDir
    :param title: The title of the slideshow
    """
    if not os.path.isdir(folderPath):
        os.mkdir(folderPath)

    savedInfoFutures = []

    executor = ThreadPoolExecutor()
    for file, seconds in fileSeconds:
        dest = os.path.basename(file.filename)
        # Copy files to new destination and append items list
        savedInfoFutures.append(executor.submit(saveFile, file, os.path.join(folderPath, dest), seconds))
    executor.shutdown()
    info = {'title': title, 'info': [x.result() for x in savedInfoFutures]}
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
