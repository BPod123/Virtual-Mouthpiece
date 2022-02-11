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
## v0.1.0
### Features
* Users can now drag and drop images into application's drag-and-drop zone to send images to billboard.
* Users can now click in drag-and-drop zone to browse their file system and select an image without having to leave the application page.
* Users can also now transmit images to Raspberry Pi.
### Bug Fixes
* None this time around (Sprint 1)
### Known Issues
* LED Panels are not responsive, further investigation needed to diagnose issue.