# Web API
from bottle import Bottle, request

app = Bottle()

@app.get('/hello')
def hello():
    return "Hello World!"

@app.get('/stop')
def stop():
    return "Stop!"

@app.get('/forward')
def forward():
    return "Moving Forward!"

@app.get('/backward')
def backward():
    return "Moving Backward!" 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
