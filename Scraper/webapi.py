from bottle import Bottle

app = Bottle()

@app.get('/hello')
def hello():
    return('Hello !!!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
