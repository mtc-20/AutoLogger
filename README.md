# AutoLogger
**Autonomous attendance logger designed and developed for the HSRW Robotics lab.** 

**The Raspberry Pi uses face recognition to detect faces and recognise from existing database. Then, uses hand gesture detection to log in/out.**

**This fork presents a GUI that should make it easier to use the autologger with the Touchscreen.**
## Hardware
- [Raspberry Pi 3][pi]
- [Raspberry Pi Camera V2][cam]
- [Raspberry Pi 7" Touchscreen][screen] with enclosure

# Data Logging
- Text files are created daily to store check-in and check out of users with timestamps. The logging directory maintains a hierarchy based on year and month.
- The logbook folder must be created manually, otherwise the code returns an error.
- System requires a virtual keyboard installed for new username input.
```
sudo apt-get install matchbox-keyboard
```

# GUI
- A simple standby menu created using pygame and pygameMenu.
```
pip install pygame-menu
```
- Responds to mouse, keyboard and touch screen.

<p align="center">
  <img width="480" src="https://github.com/mtc-20/AutoLogger/blob/gui/Main_menu.png">
</p>


### TODO
- [x] Automate new user creation process
- [x] Make system "hands-free"; ~~may require more hardware~~
- [ ] ~~Avoid writing images to file: ?~~
- [ ] Need to add code so that database is created if it doesn't exist 
- [ ] Pressing the buttons multiple times sets up the event every time; which needs to be sorted out


[cam]:https://www.raspberrypi.org/products/camera-module-v2/
[screen]:https://www.raspberrypi.org/products/raspberry-pi-touch-display/
[pi]:https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
