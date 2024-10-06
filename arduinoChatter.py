from pyfirmata import Arduino, util, SERVO
import time

board = Arduino('COM6')

head = board.get_pin('d:9:s')
beak = board.get_pin('d:8:s')

def mouthOpen():
    head.write(180)
    beak.write(0)

def mouthClose():
    head.write(0)
    beak.write(180)

def talking():
    mouthOpen()
    time.sleep(1.25)
    mouthClose()
    time.sleep(1.25)

mouthClose()
num = int(input("How long do you want him to talk?"))

for x in range(num):
    talking()