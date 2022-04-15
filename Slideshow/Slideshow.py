import json
import os
from Slideshow.Format_Slideshow import formatSlideshow


class Slideshow(object):
    def __init__(self, zippedPath: str, workingDir: str, width, height, deleteLock):
        self.zippedDir = zippedPath
        self.workingDir = workingDir
        self._info = None
        self._width = width
        self._height = height
        self.dimsChanged = False
        self.deleteLock = deleteLock
        self.collapse()

    @property
    def infoPath(self):
        return os.path.join(self.workingDir, "info.json")
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, newWidth):
        if self.width != newWidth:
            self._width = newWidth
            self.dimsChanged = True

    @height.setter
    def height(self, newHeight):
        if self.height != newHeight:
            self._height = newHeight
            self.dimsChanged = True

    @property
    def isUnzipped(self):
        return os.path.isfile(self.infoPath)

    @property
    def info(self):
        if self._info is None and self.isUnzipped:
            with open(self.infoPath, "r") as f:
                self._info = json.load(f)
        return self._info

    def reset(self):
        """
        Collapses the working directory and then unzips the zip file and recreates the working directory.
        """
        self.collapse()
        self.unzipAndFormat()

    def unzipAndFormat(self):
        """
        Unzips the slideshow to self.wokingDir and sets self._info and self._infoPath
        """
        self.deleteLock.acquire()
        self._info, self._infoPath = formatSlideshow(self.zippedDir, self.workingDir, self.width, self.height)
        self.dimsChanged = False
        self.deleteLock.release()

    def collapse(self):
        """
        Removes any slideshow files in self.workingDir and removes info.json as well. The zipped file is left intact.
        """

        if self.info is None:
            return
        self.deleteLock.acquire()
        for slideItem in self.info:
            fileName = os.path.basename(slideItem['path'])
            path = os.path.join(self.workingDir, fileName)
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except:
                continue
        try:
            if os.path.isfile(os.path.join(self.workingDir, "info.json")):
                os.remove(os.path.join(self.workingDir, "info.json"))
        except:
            pass
        self._info = None
        self.deleteLock.release()

