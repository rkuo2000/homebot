# To recieve audio file
 
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "hello"

@app.route("/image", methods=['POST'])
def audio():
    if request.method == 'POST':
        imagefile = request.files['image']
        print(imagefile.filename)
        imagefile.save(imagefile.filename)

        return jsonify({"msg": imagefile.filename+" received OK!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
