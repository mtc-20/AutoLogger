# AutoLogger
**Autonomous attendance logger designed and developed for the HSRW Robotics lab.** 

**The Raspberry Pi uses face recognition to detect faces and recognise from existing database. Then, uses hand gesture detection to log in/out.**

## Hardware
- [Raspberry Pi 3][pi]
- [Raspberry Pi Camera V2][cam]
- [Raspberry Pi 7" Touchscreen][screen] with enclosure

# Data Logging
Text files are created daily to store check-in and check out of users with timestamps. The logging directory maintains a hierarchy based on year and month.

System currently requires keyboard to accept input/awake from sleep.

### TODO
- [x] Automate new user creation process
- [ ] Make system completely hands-free; may require more hardware
- [ ] Avoid writing images to file: ?
- [ ] Need to add code so that database is created if it doesn't exist 


[cam]:https://www.raspberrypi.org/products/camera-module-v2/
[screen]:https://www.raspberrypi.org/products/raspberry-pi-touch-display/
[pi]:https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
