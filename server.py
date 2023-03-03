#!/usr/bin/python3
from flask import Flask, request
from datetime import datetime
import time
import base64
import hashlib

def hash():
    now = datetime.now()
    hash = hashlib.md5(str(now).encode('utf-8'))
    hash = hash.hexdigest()
    hash = str(hash)
    return hash

def decodefile(filename:str):
    with open(filename, 'r') as f:
        encoded_data = f.read()
        decoded_data = base64.b64decode(encoded_data)
    with open(filename, 'wb') as f:
        f.write(decoded_data)

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post_handler():
    file = (hash()+'.txt')
    with open(file, 'ab') as f:
        for chunk in request.stream:
            f.write(chunk)
    decodefile(file)
    time.sleep(0.5)
    return 'Received POST request with data.\n'

if __name__ == '__main__':
    app.run(debug=True, port=1337, host='0.0.0.0')