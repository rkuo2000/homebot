# RoboCar with Web UI
# running http server (port 8080)
# open PC browser at http://192.168.xxx.xxx:8080 to use WebUI remote control robocar
from bottle import Bottle, request
import RPi.GPIO as GPIO
import time

app = Bottle()

webpage = " <!DOCTYPE html><html lang=\"en\"><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, user-scalable=no\"/><title>RoboCar</title><style>.c{text-align: center;} div,input{padding:5px;font-size:1em;}  input{width:90%;}  body{text-align: center;font-family:verdana;} button{border:0;border-radius:0.6rem;background-color:#1fb3ec;color:#fdd;line-height:2.4rem;font-size:1.2rem;width:100%;} .q{float: right;width: 64px;text-align: right;} .button2 {background-color: #008CBA;} .button3 {background-color: #f44336;} .button4 {background-color: #e7e7e7; color: black;} .button5 {background-color: #555555;} .button6 {background-color: #4CAF50;} </style><script>function c(l){document.getElementById('s').value=l.innerText||l.textContent;document.getElementById('p').focus();}</script></head><body><div style='text-align:left;display:inline-block;min-width:260px'><table><caption>RoboCar</caption><tr><td></td><td><form action=\"/forward\" method=\"get\"><button class=\"button1\">Forward</button></form></td><td></td></tr><tr><td><form action=\"/left\" method=\"get\"><button class=\"button4\">Left</button></form></td><td><form action=\"/stop\" method=\"get\"><button class=\"button5\">Stop</button></form></td><td><form action=\"/right\" method=\"get\"><button class=\"button3\">Right</button></form></td></tr><tr><td></td><td><form action=\"/backward\" method=\"get\"><button class=\"button2\">Backward</button></form></td><td></td></tr></table></body></hmtl>"

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
    pwmA.stop()
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
    pwmA.start(100) # pwm duty cycle =100%
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwmB.start(100) # pwm duty cycle =100%
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)

def robo_right():
    GPIO.output(STBY,GPIO.HIGH)
    pwmA.start(100) # pwm duty cycle =100%
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwmB.start(100) # pwm duty cycle =100%
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)

# Web API
@app.get('/')
def root():
    return webpage
@app.get('/hello')
def hello():
    return "RoboCar: Hello!!!"

@app.get('/stop')
def stop():
    robo_stop()
    return webpage

@app.get('/forward')
def forward():
    robo_forward()
    return webpage

@app.get('/backward')
def backward():
    robo_backward()
    return webpage

@app.get('/left')
def left():
    robo_left()
    return webpage

@app.get('/right')
def right():
    robo_right()
    return webpage

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
