from flask import Flask, request, Response, json, Blueprint, send_from_directory

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)