from flask import Flask, request
import os
import json

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello :)"


@app.route("/webhook", methods=['POST'])
def github_webhook_handler():
    payload = json.loads(request.form['payload'])
    print(payload)
    return ""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
