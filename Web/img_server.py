# receive image file and return image size
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return "hello"

@app.route("/im_size", methods=["POST"])
def image_size():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

@app.route("/im_read", methods=["POST"])
def image_read():
    file = request.files['image']
    img = Image.open(file.stream)
    img.show();
    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
