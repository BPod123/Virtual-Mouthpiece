import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
if __name__ == '__main__':
    fileName = os.path.abspath('FileTransfer/RecievedFile/FirstWin.gif')
    options = RGBMatrixOptions()
    options.rows = 16
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    matrix = RGBMatrix(options=options)
    image = Image.open(fileName)
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    matrix.SetImage(image.convert('RGB'))
    z = 3
