import os
from rpiRgbLedMatrix.bindings.python.rgbmatrix import RGBMatrix, RGBMatrixOptions

from PIL import Image, ImageSequence
import numpy as np
from time import sleep



if __name__ == '__main__':
    fileName = os.path.abspath("../FileTransfer/ReceivedFile/Blue Angel.jpg")
    options = RGBMatrixOptions()
    # options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'

    matrix = RGBMatrix(options=options)
    testFrame = np.zeros((32, 16, 3), dtype=np.uint8) + 250
    testFrame[0, 0, 0] = 250
    testFrame[0, -1, 1] = 250
    testFrame[-1, 0, 2] = 250
    testFrame[-1, -1, :] = np.array([250, 250, 250])
    testImage = Image.fromarray(testFrame)
    matrix.SetImage(testImage.convert('RGB'))
    z = 3

    #
    # image = Image.open(fileName)
    # if '.gif' in fileName:
    #     frames = np.array(
    #         [np.array(frame.copy().convert('RGB').getdata(), dtype=np.uint8).reshape(frame.size[1], frame.size[0], 3) for
    #          frame in ImageSequence.Iterator(image)])
    #     # image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    #     for frame in frames:
    #         frameImage = Image.fromarray(frame)
    #         frameImage.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    #         matrix.SetImage(frameImage)
    #         sleep(0.5)
    # else:
    #     image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    #     matrix.SetImage(image.convert('RGB'))
    #

        # matrix.SetImage(image.convert('RGB'))
    sleep(5)
    z = 3
