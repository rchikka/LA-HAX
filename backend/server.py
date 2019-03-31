from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from os import path

app=Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify("Hello World!")

@app.route('/upload', methods = ['POST'])
def upload_file():
    fileD = request.form.get("fileData")
    fileN = request.form.get("fileName")
    print("the file name is: ",fileN)
    fh=open(fileN, "wb")
    fh.write(fileD.decode('base64'))
    fh.close()
    os.rename(fileN,"bananaIMG.jpg")

    return "done"
app.run(port=5000, debug=True)