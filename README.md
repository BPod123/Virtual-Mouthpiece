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
