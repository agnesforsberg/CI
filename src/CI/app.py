from flask import Flask, request
import pytest
import os
import subprocess
import json
from pylint import epylint as lint
import notification


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
    repo_name = "testrepo_{}".format(repo_id)
    if not os.path.isdir(repo_name):
        os.system("git clone {} {}".format(payload["repository"]["clone_url"],repo_name))
    else:
        os.system("git pull {}".format(repo_name))

    #Switch to branch
    os.system("git -C {} checkout {}".format(repo_name,payload["after"]))

    #Run pylint
    (pylint_stdout, pylint_stderr) = lint.py_run(repo_name, return_std=True)
    #print(pylint_stdout.read())

    #Run pytest
    pytest_stdout = subprocess.run("python -m pytest {}".format(repo_name),text=True,capture_output=True).stdout
    #print(pytest_stdout)

    subject = '[{}] {} "{}"'.format(payload["repository"]["full_name"], repo_name, payload["commits"][0]["message"])
    notification.send_notification('Subject: {}\n\n{}'.format(subject, pylint_stdout.read() + "\n" + pytest_stdout))


if __name__ == '__main__':

    with open("data/demo_payload.json") as f:
        payload = json.load(f)

    handle_push(payload)
    app.run(debug=True, host='0.0.0.0',port=80)
