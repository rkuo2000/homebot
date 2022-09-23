# Two-wheel Robo Car : GPIO control test
import RPi.GPIO as GPIO
import time
import sys

# define control pins of TB6612FNG
STBY = 4
PWMA = 13
AIN2 = 27
AIN1 = 17
BIN1 = 23
BIN2 = 24
PWMB = 18

# GPIO setup for motor control pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
# initial value
GPIO.output(STBY,GPIO.LOW)
GPIO.output(AIN1,GPIO.LOW)
GPIO.output(AIN2,GPIO.LOW)
GPIO.output(BIN1,GPIO.LOW)
GPIO.output(BIN2,GPIO.LOW)

# set PWM frequency
pwmA = GPIO.PWM(PWMA, 0.5) 
pwmB = GPIO.PWM(PWMB, 0.5)

# Robo functions
def robo_stop():
    GPIO.output(STBY,GPIO.LOW)
    pwmA.stop()
    GPIO.output(AIN1,GPIO.LOW)
    GPIO.output(AIN2,GPIO.LOW)
    pwmB.stop()
    GPIO.output(BIN1,GPIO.LOW)
    GPIO.output(BIN2,GPIO.LOW)

def robo_forward(): 
    GPIO.output(STBY,GPIO.HIGH)
    pwmA.start(100) # pwm duty cycle =100%
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwmB.start(100) # pwm duty cycle =100%
    GPIO.output(BIN1,GPIO.HIGH)
    GPIO.output(BIN2,GPIO.LOW)

def robo_backward(): 
    GPIO.output(STBY,GPIO.HIGH)
    pwmA.start(100) # pwm duty cycle =100%
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwmB.start(100) # pwm duty cycle =100%
    GPIO.output(BIN1,GPIO.LOW)
    GPIO.output(BIN2,GPIO.HIGH)

def robo_left():
    GPIO.output(STBY,GPIO.HIGH)
    pwmA.start(50) # pwm duty cycle =50%
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwmB.start(50) # pwm duty cycle =50%
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

def robo_right():
    GPIO.output(STBY,GPIO.HIGH)
    pwmA.start(50) # pwm duty cycle =50%
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwmB.start(50) # pwm duty cycle =50%
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

## RoboCar control test
#
robo_forward()
time.sleep(0.5)
robo_stop()
time.sleep(1)
#
robo_backward()
time.sleep(0.5)
robo_stop()
time.sleep(1)
#
robo_right()
time.sleep(1)
robo_stop()
time.sleep(1)
#
robo_left()
time.sleep(1)
robo_stop()
time.sleep(1)
