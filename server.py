from flask import Flask, jsonify, request
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify("Hello World!")

@app.route('/upload', methods = ['POST'])
def upload_file():
    file = request.args.get('file')
    print(file)
    return "done"
app.run(port=5000, debug=True)
