import websocket

websocket.enableTrace(True)
ws = websocket.create_connection("ws://192.168.1.7/webserialws")

print("Sending 'Hello from Taiwan'...")
ws.send("Hello from Taiwan")

i = 0
result = ws.recv()
while(result):
   result =  ws.recv()
   print("Received: ", result)
   ws.send("Hello "+str(i)+" from Taiwan")
   i+=1
   
ws.close()