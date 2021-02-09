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
    event_type = request.headers["X-Github-Event"]
    if event_type == "push":
        handle_push(payload)


    return ""

def handle_push(payload):
    repo_id = payload["repository"]["id"]
    if not os.path.isdir("testrepo_"+str(repo_id)):
        os.system("git clone {} testrepo_{}".format(payload["repository"]["clone_url"],repo_id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
