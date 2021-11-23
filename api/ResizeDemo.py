import os
from PIL import Image, ImageSequence
import numpy as np
import sys
def getFrames(gif:Image):
    """
    :param gif: The gif as a PIL Image
    :param targetDim: The desired dimensions of the image
    :return: An array of images of the desired dimension
    """
    gifFrames = np.array(
        [np.array(frame.copy().convert('RGB').getdata(), dtype=np.uint8).reshape(frame.size[1], frame.size[0], 3) for
         frame in ImageSequence.Iterator(gif)])
    return gifFrames

def resizeFile(fileName, newName, targetDim):

    nameDimDivide = fileName.find("_")
    nameFormatDivide = fileName.rindex(".")
    name = fileName[:nameDimDivide]
    format = fileName[nameFormatDivide:].lower().replace(" ", "")
    del nameFormatDivide, nameDimDivide
    # newName = "Resized Files/" + name + "Resized{0}".format(format)
    if 'gif' in format:
        resize_gif(fileName, newName, targetDim)
    else:
        im = Image.open(fileName).resize(targetDim)
        im.save(newName)
    # if format == 'gif':



def resize_gif(path, save_as=None, resize_to=None):
    """
    Resizes the GIF to a given length:

    Args:
        path: the path to the GIF file
        save_as (optional): Path of the resized gif. If not set, the original gif will be overwritten.
        resize_to (optional): new size of the gif. Format: (int, int). If not set, the original GIF will be resized to
                              half of its size.
    """
    all_frames = extract_and_resize_frames(path, resize_to)

    if not save_as:
        save_as = path

    if len(all_frames) == 1:
        print("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=5000)


def analyseImage(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    """
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(path, resize_to=None):
    """
    Iterate the GIF, extracting each frame and resizing them

    Returns:
        An array of all frames
    """
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    if not resize_to:
        resize_to = (im.size[0], im.size[1])

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    try:
        while True:
            # print("saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile))

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            # new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            new_frame = new_frame.resize(resize_to)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames

def main(src, dest, width, height):
    resizeFile(src, dest, (width, height))

if __name__ == '__main__':
    """
    Args:
    source file
    new file name for resized file
    width
    height
    """
    if "Resize Demo" in os.listdir():
        os.chdir("Resize Demo")

    args = sys.argv
    if len(args) >= 5:
        src, dest, width, height = args[1], args[2], int(args[3]), int(args[4])
        targetDimensions = (width, height)
        resizeFile(src, dest, targetDimensions)
        # for fileName in os.listdir(src):
        #     resizeFile(fileName, dest + "/" + fileName, targetDimensions)
    # targetDimensions = (600, 200)#(600, 200) # Width x Height
    # for fileName in os.listdir("Sample Files"):
    #     resizeFile(fileName, "Resized Files/" + fileName, targetDimensions)

