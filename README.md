<h1 align="center">Welcome to Virtual-Mouthpiece 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://spdx.org/licenses/MIT.html" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> Our team is currently working on making Dobbins Air Force Base’s two electronic billboards operational again. Our client is Dobbins Air Force Base ops team and more specifically Colonel Terence Green and Dr. Patrick Reynolds. One of the project restrictions is that we cannot use wi-fi to transmit messages due to the fact that we are implementing a solution for the Air Force Base.  
Our solution has a web application front end that will be hosted on a Raspberry Pi in a control room. There, billboard operators will load images/videos onto the Raspberry Pi via a usb drive from which they can insert the files into the web application. The Raspberry Pi in the control room, will then reformat the aspect ratios of the images/videos to match the billboard they are being sent to. Then, the images/videos are sent via ethernet to a second Raspberry Pi that is connected directly to, and controlling, the billboard. This second Raspberry Pi will play the images/videos on a loop until new instructions are sent to it.

### 🏠 [Homepage](https://github.com/BPod123/Virtual-Mouthpiece)

## Authors

👤 **JIF 1354** - Pablo Correa, Rahul Deshpande, Subbarao Garlapati, Ben Podrazhansky, Dhyey Shah, Yoana Zaharieva

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

This project is [MIT](https://spdx.org/licenses/MIT.html) licensed.

# Release Notes
## 0.5.0
### Features
* Project as defined in scope is completed.
### Bug Fixes
* Raspberry Pi is no longer needed as scope has narrowed.
* Slideshow runtimes and titles send through API.
### Known Issues
* None!

## 0.4.0
### Features
* Users are now able to add images to slideshow with an improved UI/UX.
* Users can see API Success/Error/Loading responses in a Toast
### Bug Fixes
* React App does not crash
* Continued figuring out hardware issues
### Known Issues
* The Raspberry Pi is not working ideally due to hardware issues.
* Slideshow runtimes and titles are not sending through API.

## v0.3.0
### Features
* Users can now create a slideshow utilizing the add to slideshow button that pops up when an image is uploaded.
* Users can now preview the slideshow with a slideshow preview component under the image uploader.
* Users have the ability to set a designated runtime for each image in the slideshow using the time text box underneath each image preview in the slideshow preview component.
### Bug Fixes
* Continued figuring out some of the hardware problems and put in order to get another version of a Raspberry Pi
### Known Issues
* If image uploading is canceled for any image after first image that is uploaded, the React web app crashes.
* The Raspberry Pi is not working ideally due to hardware issues.

## v0.2.0
### Features
* Ability to manually transmit data at actual physical location so that the user can move files utilizing a USB.
* Transmits data by transferring files from USB to Raspberry Pi utilizing a Python script running on the Raspberry Pi
* Ability to select multiple billboards on the frontend and then send data to the multiple locations if multiple are selected
### Bug Fixes
* Fixed some issues with testing LED panels through soldering and new hardware
### Known Issues
* LED Panels still don't behave ideally, currently investigating possible solutions.

## v0.1.0
### Features
* Users can now drag and drop images into application's drag-and-drop zone to send images to billboard.
* Users can now click in drag-and-drop zone to browse their file system and select an image without having to leave the application page.
* Users can also now transmit images to Raspberry Pi.
### Bug Fixes
* None this time around (Sprint 1)
### Known Issues
* LED Panels are not responsive, further investigation needed to diagnose issue.

# Installation
Virtual-Mouthpiece can be installed in three simple steps.
1. Install [Python](https://www.python.org/downloads/) 3.9 or higher
2. Install [Node.js](https://nodejs.org/en/) 16 or higher.
3. Run install_dependencies.py by executing the command ```python install_dependencies.py``` or on linux, ```sudo python install_dependencies.py```

on the command prompt in the Virtual-Mouthpiece directory.

This file will install all necessary python and node dependencies needed to run Virtual-Mouthpiece.
## Running the Server
The server is the computer that you will use to create slideshows on and choose which display to send them to.
To start the server, execute the following commands from the terminal/command prompt in the `Virtual-Mouthpiece` directory:

```python Server_Main.py```
or on linux, ```sudo python Server_Main.py```.

on the command prompt in the Virtual-Mouthpiece directory.
After running this command, a browser window should open with the main Virtual-Mouthpiece screen.
Also, in the terminal, you should see a message that says

```Project is running at http://###.##.###.###```

where `###.##.###.###` is your computer's IP address.

📝 *Make a note of this for starting client instances.*

## Running a Display Client
The display client is the computer that is directly connected to the display.
To run an instance of the client,
1. Run `Display_Client_Main.py` by executing the following commands from the terminal/command prompt in the `Virtual-Mouthpiece` directory: ```python Server_Main.py```. Or, on linux, ```sudo python Server_Main.py```.
2. You will next be prompted to choose a configuration option.
   1. If this is not your first time connecting to the current server computer, you have the option to use the last used configuration option.
   2. If this is the first time connecting to a server computer, choose the option to create a new configuration.
      1. When selecting your configuration options, the server ip address from the previous section will be necessary for the display client to know which computer to connect to.

Once a configuration has been set, the display client should be running. If the server is already running and you do not see the display client's name, refresh the page.