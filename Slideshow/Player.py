import Slideshow.Slideshow
from Slideshow.Reader import Reader, showImage
from enum import Enum
from threading import Thread
from time import time, sleep


class PlayerState(Enum):
    STOPPED = 0
    STOPPING = 1
    PLAYING = 2
    CHANGING_SLIDE = 3


class Player(object):
    def __init__(self, displayName, transitionDuration):
        self._slideshowName = None
        self._thisDisplayName = displayName
        self.transitionDuration = transitionDuration
        self.reader = None
        self._state = PlayerState.STOPPED
        self.nextStopCallbacks = []
        self._playThread = None
        self._slideshow = None
        self._playStartTime = None
        self.curSlide = 0
    @property
    def slideshowName(self):
        if self.slideshow is not None and self.slideshow.info['title'] is not None:
            return self.slideshow.info['title']
        else:
            return self._thisDisplayName

    @property
    def isStopped(self):
        return self.state == PlayerState.STOPPED

    @property
    def slideshow(self):
        return self._slideshow

    def setSlideshow(self, value):
        self.slideshow = value


    @slideshow.setter
    def slideshow(self, value):
        # Stop the current slideshow if not stopped
        currState = self._state
        if not self.isStopped:
            self.nextStopCallbacks.append(lambda: self.setSlideshow(value))
            self.stop()
            return
        # Collapse the current slideshow, if unzipped
        if self._slideshow is not None and self._slideshow.isUnzipped:
            self._slideshow.collapse()

        self._slideshow = value
        self.slideshow.unzipAndFormat()
        self.reader = Reader(self.slideshowName, self.slideshow, self.transitionDuration)
        if currState == PlayerState.PLAYING:
            self.playThread.start()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        if self.state != newState and not (self.state == PlayerState.STOPPED and newState == PlayerState.STOPPING):
            self._state = newState
            if newState == PlayerState.STOPPED:
                while len(self.nextStopCallbacks) > 0:
                    self.playThread = None
                    # Call everything that was waiting for the player to stop
                    self.nextStopCallbacks.pop(0)()


    @property
    def playThread(self):
        if self._playThread is None:
            self._playThread = Thread(target=self.play)
        return self._playThread

    @playThread.setter
    def playThread(self, newValue):
        self._playThread = newValue

    def transition(self):
        self.state = PlayerState.CHANGING_SLIDE
        self.curSlide = self.reader.fileIndex
        self.reader.transition()
        self.state = PlayerState.PLAYING

    def waitForTransitionThread(self, waitTime):
        wait_playStartTime = self._playStartTime
        sleep(waitTime)
        if self._playStartTime != wait_playStartTime or self.state != PlayerState.PLAYING:
            # The player stopped since this thread went to sleep. Do nothing
            return
        else:
            self.transition()
            # # Notify the reader to transition to the next image/video.
            # # del waitTime
            # self.reader.transition()
            # # currFileIndex = self.reader.fileIndex
            # # nextFileIndex = currFileIndex + 1 if currFileIndex < len(self.slideshow.info) - 1 else 0
            # # nextSleepDuration = self.transitionDuration + self.slideshow.info[nextFileIndex]['seconds']
            # # del currFileIndex, nextFileIndex
            #
            # # self.waitForTransitionThread(nextSleepDuration)

    def stop(self):
        if not self.isStopped:
            self.state = PlayerState.STOPPING

    def play(self):
        """
        The function for playing the slideshow
        """

        self.state = PlayerState.PLAYING
        self._playStartTime = time()
        if len(self.slideshow.info['info']) > 1:
            Thread(target=self.waitForTransitionThread,
                   args=(self.reader.slideshow.info['info'][self.reader.fileIndex]['seconds'],)).start()
        while self.state == PlayerState.PLAYING or self.state == PlayerState.CHANGING_SLIDE:
            while self.state == PlayerState.CHANGING_SLIDE:
                sleep(0.001)
            if self.curSlide != self.reader.fileIndex:
                # Transition has taken place. Time to start the next wait
                self.curSlide = self.reader.fileIndex
                if len(self.slideshow.info['info']):
                    Thread(target=self.waitForTransitionThread,
                           args=(self.reader.slideshow.info['info'][self.reader.fileIndex]['seconds'],)).start()
            if self.state == PlayerState.PLAYING:
                self.reader.read()

        self._playThread = None
        self.state = PlayerState.STOPPED

    def changeDims(self, width, height):
        if self.reader is None:
            return
        self.reader.slideshow.width = width
        self.reader.slideshow.height = height
        if self.reader.slideshow.dimsChanged:
            if self.state == PlayerState.PLAYING:
                self.state = PlayerState.STOPPING
            if self.state == PlayerState.STOPPED:
                self.reader.slideshow.reset()
            else:
                # The slideshow is stopping. Wait for it to stop.
                self.nextStopCallbacks.append(lambda: self.reader.slideshow.reset())
