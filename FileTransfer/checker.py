import time
import os

while True:
    #print("top of while loop")
    time.sleep(5)
    arr = os.listdir('/media/pi') 
    if len(arr) == 1:
        drive_path = '/media/pi/' + arr[0]
        print("drive_path: ",drive_path)
        drive_files = os.listdir(drive_path)
        print("drive_files: ", drive_files)
        if 'BillboardFilesFlashDrive' in drive_files:
            files_folder = drive_path + '/BillboardFilesFlashDrive'
            print("files_folder: ", files_folder)
            copy_folder_string = "cp -r " + files_folder + " ~/Desktop/BillboardFilesRaspberryPi"
            print("copy_folder_string: ", copy_folder_string)
            os.system(copy_folder_string)
            toEjectStr = 'sudo eject ' + drive_path
            print("toEjectStr" + toEjectStr)
            os.system(toEjectStr)
    print(arr)
