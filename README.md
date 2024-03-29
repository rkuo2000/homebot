# Homebot 

## Chatbot

### DNN 
* **intents.json** - *chatting intents*
* **chatbot_dnn.h5** - *model file*
* **data.pickle** - *data file*
* **chatbot_dnn.py** - *train chatbot, then inference*

* **chatbot_server.py** - *chatbot server using chatbot_dnn.h5*
* **chatbot_client.py** - *calling to server to chat*

### FaceBook
* **fbchat_basic.py** - *login FB to find owner uid* <br />
* **fbchat_echobot.py** - *messenger auto echo to message* <br />
* **fbchat_fetchid.py** - *list all FB friend's id* <br />
* **fbchat_send.py** - *send text, emoji, local image, remote image* <br />

### Messenger
* **messengerbot_chat.py** - *Chatbot for Messenger* <br />
* **messengerbot_echo.py** - *Echobot for Messenger* <br />

### Line
* **linebot_chat.py** - *Chatbot for Line* <br />
* **linebot_echo.py** - *Echobot for Line* <br />

---
## Html
* **QRcode_generator.html** - input text to generate QR code
* **robocar_dialogflow.html** - webpage for connecting to dialogflow chatbot

---
## mp3 
.mp3 files<br>
* $`mpg123 Cat_Meowing0.mp3`<br>

---
## Plot

### examples to plot 3D
* plot3d_curve.py
* plot3d_dots.py
* plot3d_surface.py
* plot3d_vectorfield.py
* plot3d_wireframe.py

---
## RPi (Raspberry Pi)

### UART
* esp32_webserial.py
* uart.py

### sensors
* **vl53l0x.py** - using vl53l0x_python.so
* **mpu9250_test.py**
* **PID.py** - PID controller example
* **testPID.py** - test PID control
* **AHRS_madgwick.py** - *AHRS algorith*

### I2C devices
* **rpi3_alexa_gpio.py** - *RPi3 as Alexa app with GPIO control*
* **rpi3_i2c_HTU21DF.py** - *RPi3 I2C to read HTU21DF temperature and humidity*
* **rpi3_i2c_MLX90614.py** - *RPi3 I2C to read MLX90614 IR ranger*
* **rpi3_i2c_VL53L0X.py**  - *RPi3 I2C to read VL53L0X IR ranger*
* **rpi3_mpu6050.py**  - *read MPU6050 rawdata*
* **rpi3_mpu9250.py**  - *read MPU9250 rawdata*

---
### RoboCar
* **rpi3_robocar_gpio.py**  - *RPi3 GPIO control a robot car* <br>
* **rpi3_robocar_webui.py** - *RPi3 WebUI to control a robot car* <br>
* **rpi3_robocar_webui_sensors.py** - *RPi3 WebUI to read sensors on a robot car* <br>
* **rpi3_uart.py**          - *RPi3 uart in python*<br>

---
## Scraper (Web scraper)
* read_json.py (read ex.json)
* scrape_accuweather.py
* scrape_anime.py
* scrape_applenews.py
* scrape_hsimuren.py
* scrape_imdb.py
* scrape_quotes.py
* scrape_wikipedia.py
* scrape_yahoo_finance.py
* scrape_youtube.py

---
## Speech 

### Google SR/TTS
* Speech-to-Text (Speech Recognition)
  - $`python3 gSR.py en`        *(Speech to Text)*<br>
  - $`winpty python gSR.py en`  *(in Gitbash)*<br>
  
* Text-to-Speech
  - $`python3 gTTS.py hello en` *(outputr is gTTS.mp3)*<br>
  - $`winpty gTTS.py hello en` *(in Gitbash)*<br>
  
### Dialogflow
* $`python3 dialogflow_test.py hello en` - *test Dialogflow agent*<br>
* $`python3 dialogflow_gSR.py en` - *Dialogflow with SR*<br>
* $`python3 dialogflow_gSTT.py en` - *Dialogflow with SR & TTS*<br>

### parse KML (Google Earth pro as Mission Planner)
* $`python3 parse_kml.py test.kml`<br>

### Others
* **vstock.py** - *download stock .csv file*
