#!/usr/bin/python3
from flask import Flask, request
from datetime import datetime
import argparse
import time
import base64
import hashlib
import os

def hash():
    now = datetime.now()
    print(now)
    hash = hashlib.md5(str(now).encode('utf-8'))
    hash = str(hash.hexdigest())
    return hash

def decodefile(filename:str):
    print(filename)
    with open(filename, 'r') as f:
        encoded_data = f.read()
        decoded_data = base64.b64decode(encoded_data)
    with open(filename, 'wb') as f:
        f.write(decoded_data)

app = Flask(__name__)
@app.route('/post', methods=['POST'])
def post_handler():
    temph = hash()
    file = os.path.join(output_directory, f'{temph}.txt')
    with open(file, 'ab') as f:
        for chunk in request.stream:
            f.write(chunk)
    decodefile(file)
    time.sleep(0.5)
    return f'The server received your data. [{temph}]\n'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic python server built in Flask to receive data and save it to a file. Used normally on Pentesting and Red Team stuff in order to exfiltrate some files fast.",epilog="""Created by: Xen00rw""")
    parser.add_argument("-p", "--port", action="store", type=int, required=True, dest='port', help='TCP port to be used')
    parser.add_argument("-o", "--output", type=str, default="./exfil_output", dest='output', help='Output directory')
    args = parser.parse_args()

    tcp_port = args.port
    output_directory = args.output

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    app.run(debug=False, port=tcp_port, host='0.0.0.0')