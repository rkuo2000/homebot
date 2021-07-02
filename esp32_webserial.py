# WebSocket work with [ESP32 WebSerial](https://github.com/rkuo2000/arduino/tree/master/examples/ESP32_WebSerial)
import websocket #pip install websocket-client

websocket.enableTrace(True)
ws = websocket.create_connection("ws://192.168.1.7/webserialws")

print("Sending 'Hello from Taiwan'...")
ws.send("Hello from Taiwan")

i = 0
while(True):
   result =  ws.recv() # receive message from ESP32 WebSerial
   print("Received: ", result) 
   ws.send("Hello "+str(i)+" from Taiwan") # keep sending message to ESP32 WebSerial
   i+=1
   
ws.close()