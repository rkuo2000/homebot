import serial
ser = serial.Serial('COM6', 9600)
ser.write(b'start   ')

while 1:
    ser.write(b'readline')
    line = ser.readline()
    print(line)
