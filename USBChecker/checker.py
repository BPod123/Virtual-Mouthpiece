import time
import os
import shutil
def copyFilesToDirectory(dest, checkVariable, src='/media/pi'):
    """
    Args:
        dest: The destination directory to copy the files to
        checkVariable: A list variable with a single boolean in it. [True]. While the boolean inside the list is true,
        the thread will continue checking the directory
        src: The directory to be checking.
    """
    while checkVariable[0]:
        contents = os.listdir(src)
        for fName in contents:
            path = src + "/" + fName
            destPath = dest + "/" + fName
            shutil.copy2(path, destPath)
        time.sleep(2)


if __name__ == '__main__':
    # To test the function
    copyFilesToDirectory('temp', [True], src='tempSrc')
