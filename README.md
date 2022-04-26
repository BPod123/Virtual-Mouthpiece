# 🦅 Welcome to Virtual Mouthpiece 👋

<p>
  <img alt="Version" src="https://img.shields.io/badge/TEAM-1354-blue" />
  <img alt="Version" src="https://img.shields.io/badge/version-0.5.0-yellow.svg?cacheSeconds=2592000" />
  <a href="https://spdx.org/licenses/MIT.html" target="_blank"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>
</p>

# 👥 About The Project

We are team JIF 1354, supporting Project Virtual Mouthpiece for Colonel Green of the Dobbins Air Reserve Base and Dr. Reynolds of NSIN. Together, we are building a unified control system for existing electronic billboards across Dobbins Air Reserve Base. These billboards often have deprecated software and are in dire need of updates. That’s where we come in! Our solution allows for remote control of these billboards while maintaining the necessary information security policies for an air reserve base. Our solution is universal, and doesn’t rely on billboard manufacturer support.

# 📚 Stack Summary

Our solution has a ReactJS web application front end that will be hosted on a computer in a control room. There, the Dobbins Air Reserve Base's Base Ops Team (our users) will upload images and set metadata from the web application. Additionally, each billboard will have a computer connected to it, which will reformat the aspect ratios of the images/videos to match the billboard they are being sent to. The images/videos are sent via ethernet from the control room computer to the selected billboards' computers. This constraint allows us to maintain information security by closing the network to external bad actors that could hack or conduct malicious activity wirelessly. The billboards play the images/videos on a loop until new instructions are sent to them.

**TLDR**;

- Web App - React (JS)
- API - Flask (Python 3)
- Slideshow Display - Python 3
- Billboard Config - Python 3

### 🏠 [Homepage](https://github.com/BPod123/Virtual-Mouthpiece)

## Authors

👤 **JIF 1354** - Pablo Correa, Rahul Deshpande, Subbarao Garlapati, Ben Podrazhansky, Dhyey Shah, Yoana Zaharieva

## Show your support

Give a ⭐️ if this project helped you, or if you found our work interesting!

## 📝 License

This project is [MIT](https://github.com/BPod123/Virtual-Mouthpiece/blob/master/LICENSE) licensed.

# Installation

Virtual-Mouthpiece can be installed in three simple steps.

1. Install [Python](https://www.python.org/downloads/) 3.9 or higher by following directions online.
2. Install [Node.js](https://nodejs.org/en/) 16 or higher by following directions online.
3. Clone this repository to each computer you plan on using (client and server computers alike)
4. Navigate to the project via the terminal and run `python install_dependencies.py` or on linux, `sudo python install_dependencies.py`. Depending on your python installation, you may need to use `python3` instead of `python` in the aforementioned commands (and if so, anywhere else throughout this guide).

This file will install all necessary python and node dependencies needed to run Virtual-Mouthpiece.

## Running the Server

The server is the computer that you will use to create slideshows on and choose displays to send to.
To start the server, execute the following commands from the terminal/command prompt in the `Virtual-Mouthpiece` directory:

`python Server_Main.py` or on linux, `sudo python Server_Main.py`.

on the command prompt in the Virtual-Mouthpiece directory.

After running this command, a browser window should open with the main Virtual-Mouthpiece screen.
Also, in the terminal, you should see a message that says

`Project is running at http://###.##.###.###`

where `###.##.###.###` is your computer's IP address.

📝 _Make a note of this for starting client instances._

## Running a Display Client

The display client is the computer that is directly connected to the display.
To run an instance of the client,

1. Run `Display_Client_Main.py` by executing the following commands from the terminal/command prompt in the `Virtual-Mouthpiece` directory: `python Server_Main.py`. Or, on linux, `sudo python Server_Main.py`.
2. You will next be prompted to choose a configuration option.
   - If this is not your first time connecting to the current server computer, you have the option to use the last used configuration option.
   - If this is the first time connecting to a server computer, choose the option to create a new configuration.
     - When selecting your configuration options, the server ip address from the previous section will be necessary for the display client to know which computer to connect to.

Once a configuration has been set, the display client should be running. If the server is already running and you do not see the display client's name, refresh the browser window on the server computer.

# 🗂 Project Structure

A summary of various folders in the project:

- `api/` contains python files relevant to the Flask API.
- `BACKEND_TESTS/` contains various testing configurations to simulate connected displays.
- `Display Working Directory/` contains the unzipped files for the display to show (post file transfer).
- `Slideshow/` contains the necessary python files for playing the slideshow.
- `Test Manager Working Directory/` contains the uploaded files before they are zipped and sent to the displays.
- `USBChecker/` contains python scripts to facilitate automatic USB checking in Raspberry Pi client computers.
- Various other files in the root directory contain explanations of their content within themselves.

# Release Notes

## 0.5.0

### Features

- Project as defined in scope is completed.

### Bug Fixes

- Raspberry Pi is no longer needed as scope has narrowed.
- Slideshow runtimes and titles send through API.

### Known Issues

- None!

## 0.4.0

### Features

- Users are now able to add images to slideshow with an improved UI/UX.
- Users can see API Success/Error/Loading responses in a Toast

### Bug Fixes

- React App does not crash
- Continued figuring out hardware issues

### Known Issues

- The Raspberry Pi is not working ideally due to hardware issues.
- Slideshow runtimes and titles are not sending through API.

## v0.3.0

### Features

- Users can now create a slideshow utilizing the add to slideshow button that pops up when an image is uploaded.
- Users can now preview the slideshow with a slideshow preview component under the image uploader.
- Users have the ability to set a designated runtime for each image in the slideshow using the time text box underneath each image preview in the slideshow preview component.

### Bug Fixes

- Continued figuring out some of the hardware problems and put in order to get another version of a Raspberry Pi

### Known Issues

- If image uploading is canceled for any image after first image that is uploaded, the React web app crashes.
- The Raspberry Pi is not working ideally due to hardware issues.

## v0.2.0

### Features

- Ability to manually transmit data at actual physical location so that the user can move files utilizing a USB.
- Transmits data by transferring files from USB to Raspberry Pi utilizing a Python script running on the Raspberry Pi
- Ability to select multiple billboards on the frontend and then send data to the multiple locations if multiple are selected

### Bug Fixes

- Fixed some issues with testing LED panels through soldering and new hardware

### Known Issues

- LED Panels still don't behave ideally, currently investigating possible solutions.

## v0.1.0

### Features

- Users can now drag and drop images into application's drag-and-drop zone to send images to billboard.
- Users can now click in drag-and-drop zone to browse their file system and select an image without having to leave the application page.
- Users can also now transmit images to Raspberry Pi.

### Bug Fixes

- None this time around (Sprint 1)

### Known Issues

- LED Panels are not responsive, further investigation needed to diagnose issue.
