from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview() 
sleep(3)
# camera.capture('image.jpg') # capture to a .jpg file
camera.stop_preview()
