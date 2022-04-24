from Slideshow import Slideshow
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
import cv2
from math import floor
from abc import ABCMeta, abstractmethod
from enum import Enum
from Slideshow.Format_Slideshow import getGifFrames
from PIL import Image
from time import time
from screeninfo import get_monitors
class FileType(Enum):
    IMAGE = 0
    GIF = 1
    VIDEO = 2


class MovingAverage(object):
    def __init__(self, sequenceLength, startingAvg):
        self.sequenceLength = sequenceLength
        self.index = 0
        self.arr = np.ones(sequenceLength) * startingAvg
        self._mean = self.arr.mean()
        self.callbacks = []

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, value):
        if value != self.mean:
            self._mean = value
            self.doCallbacks()

    def doCallbacks(self):
        callbacks = self.callbacks.copy()
        self.callbacks.clear()
        [cb() for cb in callbacks]

    def update(self, value):
        self.arr[self.index] = value
        self.index = self.index + 1 if self.index < len(self.arr) - 1 else 0
        if self.index == 0:
            self.mean = self.arr.mean()


class FrameIterator(object, metaclass=ABCMeta):
    def __init__(self, numFrames, fps, duration, movingAvg: MovingAverage):
        self.duration = duration
        self.movingAvg = movingAvg
        self.numFrames, self.fps = numFrames, int(fps)
        self.duration = duration
        # if int(fps) > 0 and self.numFrames > 0:
        #     self.millisPerFrame = int(self.numFrames / self.fps * 1000)
        # else:
        # self.millisPerFrame = 1#int(movingAvg.mean)

        self.frameIndexMod = 0
        self.skipMod = None
        self.millisPerFrame = 0
        self.updateMillisPerFrame()
        # self.movingAvg.callbacks.append(self.updateMillisPerFrame)
        # self.updateMillisPerFrame()

    def updateMillisPerFrame(self):
        # second/frame * 1000 millies/second = millis per frame
        if self.duration is None:
            self.millisPerFrame = floor(1 / self.fps * 1000) if self.fps != 0 else 1  # images have fps of 0
        else:
            self.millisPerFrame = int(self.duration / self.numFrames * 1000)
        if self.millisPerFrame < self.movingAvg.mean or (
                self.fps == 0 and self.numFrames > 1 and self.duration is not None):
            # There are too many frames. So many that they would need to play more than one a millisecond.
            # Need millis per frame >= 1. That is, need 1/fps * 1000 >
            # fps = numFrames / numSeconds
            # millis per frame = 1/fps * 1000
            # Cannot adjust numSeconds, but can adjust numFrames
            if self.fps != 0:
                seconds = 1 / self.fps * self.numFrames
            else:
                seconds = self.duration

            for i in reversed(range(2, self.numFrames // 2)):
                div = self.numFrames // i
                newNumFrames = self.numFrames - div
                self.millisPerFrame = int(seconds / newNumFrames * 1000)
                self.skipMod = i
                if self.millisPerFrame >= self.movingAvg.mean:
                    break

    def read(self):
        result = self._read()
        # if self.skipMod is not None:
        #     if self.frameIndexMod % self.skipMod != 0:
        #         numSkips = self.skipMod - self.frameIndexMod
        #         for i in range(numSkips):
        #             self._read()
        #         self.frameIndexMod = 0
        #         result = self._read()
        #     # self.frameIndexMod += 1
        #     # if self.frameIndexMod % self.skipMod != 0:
        #     #     # Time to skip a frame
        #     #     return self._read()
        #     self.frameIndexMod = (self.frameIndexMod + 1) % self.skipMod
        return result

    @abstractmethod
    def _read(self):
        pass


class FileReader(FrameIterator):
    def __init__(self, fileInfo: dict, movingAvg):
        self.info = fileInfo
        path = fileInfo['path']

        if path.lower()[path.rfind('.') + 1:] in ['npy']:
            self.fileType = FileType.IMAGE
            self.cap = np.asarray(Image.open(path).convert('RGB').getdata())

        else:
            self.fileType = FileType.VIDEO
            self.cap = cv2.VideoCapture(self.info['path'])
        fps = self.info['fps']
        numFrames = self.info['numFrames']
        super(FileReader, self).__init__(int(numFrames), fps, None, movingAvg)

        self.lastImage = None
        self.isTransition = False

        # second/frame * 1000 millies/second = millis per frame

    def reset(self):
        """
        Resets self.cap to the beginning of the Video Capture for playing the video/image on a loop
        """
        if self.fileType == FileType.VIDEO:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.info['path'])
        elif self.fileType == FileType.GIF:
            del self.cap
            self.cap = getGifFrames(self.info['path'])

    def __next__(self):
        if self.fileType == FileType.VIDEO:
            return self.cap.read()
        elif self.fileType == FileType.GIF:
            try:
                frame = self.cap.__next__()
            except:
                return False, False
            ret = True, frame
            return ret
        else:
            return True, self.cap

    def _read(self):
        ret = self.__next__()
        if ret[0]:
            self.lastImage = ret[1]
        else:
            # At the end of Video/Image. Reset VideoCapture to start reading at beginning again.
            self.reset()
            ret = self.__next__()
            if not ret[0]:
                # Was not able to read image
                raise "Unable to read file"
        return ret, self.millisPerFrame

    def __del__(self):
        if self.fileType == FileType.VIDEO:
            self.cap.release()


class ArrayReader(FrameIterator):
    def __init__(self, arr, duration, movingAvg):
        """
        :param arr:
        :param duration: duration in seconds
        :param movingAvg: For calculating adjusting the speed at which it plays frames to the rate at which the disply
        is capable of
        """

        self.arr = arr
        self.index = 0
        self.isTransition = True
        super(ArrayReader, self).__init__(len(arr), 0, duration, movingAvg)
        if self.millisPerFrame > 0:
            self.arr = arr[::self.millisPerFrame]

    def _read(self):
        if self.index >= len(self.arr):
            # At the end of transition. No need to loop back.
            return (False, None), None
        ret = True, self.arr[self.index]
        self.index += 1
        return ret, self.millisPerFrame


class Reader(object):
    def __init__(self, dislpayName, slideshow: Slideshow, transitionDuration):
        self.transitionDuration = transitionDuration
        self.displayName = dislpayName
        self.slideshow = slideshow
        self.fileIndex = 0
        self._firstImage = True # For displaying the first image
        if not self.slideshow.isUnzipped:
            self.slideshow.unzipAndFormat()
        self.reader = None
        self.movingAvg = MovingAverage(15, 1)
        self.reader, self.fileIndex = self.nextFileReader()

        # Need to keep track of how long it takes to show a frame.

    @property
    def onTransition(self):
        return self.reader.isTransition

    def nextFileReader(self):
        fileIndex = self.fileIndex + 1 if self.reader is not None and self.fileIndex < len(
            self.slideshow.info) - 1 else 0
        reader = FileReader(self.slideshow.info['info'][fileIndex], self.movingAvg)
        return reader, fileIndex

    def transition(self):
        """
        Sets the self.reader to the next the reader for the next part of the slideshow.
        Either a FileReader or an ArrayReader if it is a slide transition
        """

        # Increment self.fileIndex when that file is switched to.
        if self.reader is None or len(self.slideshow.info) == 0:
            self.reader = FileReader(self.slideshow.info[self.fileIndex], self.movingAvg)
        elif isinstance(self.reader, FileReader):
            # The current reader is a FileReader, move to transition between this file and the last file.
            lastImage = self.reader.lastImage
            if lastImage is None:
                # The reader has not read any images. Skip the transition and move to the next file.
                self.reader, self.fileIndex = self.nextFileReader()
            else:
                # Generate a transition and make a reader out of it
                nextReader, nextFileIndex = self.nextFileReader()
                (frameRead, firstFrame), firstFrameMillis = nextReader.read()
                try:
                    transitionArr = self.makeTransition(lastImage, firstFrame)
                    self.reader = ArrayReader(transitionArr, self.transitionDuration, self.movingAvg)
                except:
                    # unable to read first frame from reader. This will likely not happen without other things failing
                    # first, but if it does, just skip the transition.
                    self.reader, self.fileIndex = self.nextFileReader()
        else:
            # The reader is an ArrayReader for a transition, move to next file
            self.reader, self.fileIndex = self.nextFileReader()

    @staticmethod
    def makeTransition(fromPic, toPic):
        """
        Creates and saves a transition sliding-screen animation to transition from one image/video to the next
        :param fromPic: Starting frame
        :param toPic: Ending frame

        The created transition is an array view of the two image frames, thus no additional memory is allocated
        to create the transition, and it can be created very quickly.
        """
        # Combine pictures into one extra wide picture
        combined = np.concatenate([fromPic, toPic], 1)
        # Sliding window view
        transition = sliding_window_view(combined, (combined.shape[0], fromPic.shape[1], combined.shape[-1])).squeeze()
        return transition

    def __iter__(self):
        return self

    def __next__(self):
        if not self.slideshow.isUnzipped:
            self.slideshow.unzipAndFormat()
        (frameRead, nextFrame), millis = self.reader.read()
        if not frameRead:
            # Assumed to be at end of a transition between two files.
            self.transition()
            return self.__next__()
        else:
            return nextFrame, millis

    def read(self):
        nextFrame, millis = self.__next__()
        if self._firstImage:
            self.showFirstImage(self.displayName, nextFrame, millis)
            self._firstImage = False
        else:
            start = time()
            self.showImage(self.displayName, nextFrame, millis)
            duration = time() - start
            self.movingAvg.update(duration)
    @staticmethod
    def showImage(displayName, frame, milis: int):
        cv2.imshow(displayName, frame)
        if cv2.waitKey(milis) & 0xFF == ord('q'):
            return

    def showFirstImage(self, displayName, frame, millis: int):
        """
        Like showImage, except that it positions the window as well.
        """
        monitors = get_monitors()
        if True in [self.slideshow.width == monitor.width and self.slideshow.height == monitor.height for monitor in
                 monitors]:
            cv2.namedWindow(displayName, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(displayName, cv2.WND_PROP_TOPMOST, 1)
            cv2.setWindowProperty(displayName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


        self.showImage(displayName, frame, millis)




    @staticmethod
    def cv2Wait(milis):
        if milis > 30:
            remainingMilis = milis - 30
            if cv2.waitKey(30):
                pass # Allow time to move the window if it is the first time showing the image
        else:
            remiainingMilis = milis
        if cv2.waitKey(milis) & 0xFF == ord('q'):
            return



