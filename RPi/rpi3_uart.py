import serial
ser = serial.Serial('/dev/ttyS0',115200)
#ser = serial.Serial('/dev/ttyAMA0',115200)
ser.write(b'RPi3 sending\n\r')

while 1:
    ser.write(b'RPi3 readline\n\r')
    line = ser.readline()
    print(line)
