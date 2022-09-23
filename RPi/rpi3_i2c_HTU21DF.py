### $sudo apt install pigpio python3-pigpio
### $sudo pigpiod
### $sudo killall pigpiod

import HTU21DF

HTU21DF.reset_HTU21DF()

temp = HTU21DF.read_temperature()
print("Temperature:", temp)

humid = HTU21DF.read_humidity()
print("Humidity   :", humid)
