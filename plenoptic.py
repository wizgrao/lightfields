import serial
from picamera import PiCamera
import time


def init():
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    time.sleep(2)
    ser.write(b"G90 ;\r\n")
    ser.write(b"G28\r\n")
    time.sleep(45)
    return ser

def goToPos(ser, x, z):
  ser.write("G0 X{} Y0 Z{} ;\r\n".format(x, z).encode()) 

def takePic(cam, ser, x, z, wait, xo=0, zo=0):
    print("moving")
    goToPos(ser, x, z)
    time.sleep(wait)
    print("capturing")
    cam.capture("plen{:03d}_{:03d}.png".format(x-xo, z - zo))

def lightfield(cam, ser, x0, z0, w, h, xs, zs):
    for z in range (z0, h+z0, zs):

        if z % 2 == 0:
            goToPos(ser, x0, z)
            time.sleep(1)
            for x in range(x0, w+x0, xs):
                takePic(cam, ser, x, z, 0.05, xo=x0, zo=z0)
        else:
            goToPos(ser, x0 +w-xs, z)
            time.sleep(1)
            for x in reversed(range(x0, w+x0, xs)):
                takePic(cam, ser, x, z, 0.05, xo=x0, zo=z0)
ser = init()
goToPos(ser, 50, 50)
print("Going to Start Position")
for i in range (20):
    time.sleep(1)
    print(".")
print("Initializing Camera")

camera = PiCamera(resolution=(640, 480), framerate=90)
# Set ISO to the desired value
camera.iso =1600
# Wait for the automatic gain control to settle
time.sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
print("starting Lightfield")

lightfield(camera, ser, 50, 50, 100, 100, 5, 5)
