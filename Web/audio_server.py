# To recieve audio file
 
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/hello", methods=['GET'])
def hello():
    return "hello"

@app.route("/audio", methods=['POST'])
def audio():
    if request.method == 'POST':
        audiofile = request.files['audio']
        print(audiofile.filename)
        audiofile.save(audiofile.filename)

        return jsonify({"msg": audiofile.filename+" received OK!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
