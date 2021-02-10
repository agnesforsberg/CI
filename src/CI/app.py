from flask import Flask, request
import os
import subprocess
import json
from pylint import epylint as lint
import requests
import notification

auth_token = '5b206135ed78930e1d8516619bb641734ea5229c'

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

def parse_pylint(string):
    """Parses the pylint stdout string returns the result.
        returns None if no output found."""
    lines = string.split('\n')

    for line in lines[::-1]:
        result = parse.parse(' Your code has been rated at {:F}/10 (previous run: {:F}/10, +{:F})', line)
        if result is None:
            continue

        return result[0]

def parse_pytest(string):
    """Parses the pytest output string and returns passed and failed test counts.
    If no counts are found, None is returned instead for that case.
    """
    lines = string.split('\n')

    for line in lines[::-1]:
        if not parse.parse('========================={}=========================', line):
            continue
        passed = parse.search('{:d} passed', line)
        failed = parse.search('{:d} failed', line)
        errors = parse.search('errors', line)
        if passed:
            passed = passed[0]
        if failed:
            failed = failed[0]
        if errors:
            errors = True

        return passed, failed, errors

    return None, None

def clone_repo(payload, target_dir):
    """Clones the repo declared in 'payload' into 'target_dir'"""
    os.system("git clone {} {} --depth=1 --no-single-branch".format(payload["repository"]["clone_url"], target_dir))
    os.system("git -C {} pull".format(target_dir))
    os.system("git -C {} checkout {}".format(target_dir, payload["after"]))

def remove_repo(target_dir):
    """Removes 'target_dir' dir from file system"""
    os.system("rm -rf {}".format(target_dir))

def exec_pylint(target_dir):
    """Executes pylint on 'target_dir'"""
    (pylint_stdout, pylint_stderr) = lint.py_run(target_dir, return_std=True)
    pylint_output = pylint_stdout.read()
    return pylint_output

def exec_pytest(target_dir):
    """Executes pyte4st on 'target_dir'"""
    pytest_output = subprocess.run(["python3","-m","pytest"],text=True,capture_output=True,cwd=target_dir).stdout
    return pytest_output

def send_email(payload, target_dir, pylint_output, pytest_output):
    """Sends an email with payload-, pylint-, and pytest content"""
    subject = '[{}] {} "{}"'.format(payload["repository"]["full_name"], target_dir, payload["commits"][0]["message"])
    notification.send_notification('Subject: {}\n\n{}'.format(subject, str(pylint_output) + "\n" + str(pytest_output)))

def handle_push(payload):
    repo_id = payload["repository"]["id"]
    commit_sha = payload["after"]
    repo_directory = "/tmp/testrepo_{}{}".format(repo_id,commit_sha)

    update_status(payload,"pending")

    clone_repo(payload, repo_directory)

    pylint_output = exec_pylint(repo_directory)
    pytest_output = exec_pytest(repo_directory)

    send_email(payload, repo_directory, pylint_output, pytest_output)

    remove_repo(repo_directory)

    print(pylint_output)
    print(pytest_output)

    with open("/tmp/CILogs/{}.txt".format(commit_sha),"w") as log:
        log.write(pylint_output+"\n"+pytest_output)

    if "ERRORS" in pytest_output:
        update_status(payload,"error","The commit testing resulted in some errors")
    elif "FAILURES" in pytest_output:
        update_status(payload,"failure","The commit testing failed")
    else:
        update_status(payload,"success","The commit testing succeded")


def update_status(payload, status="success", description="CI"):
    repo_name = payload["repository"]["full_name"]
    sha = payload["after"]
    url = 'https://api.github.com/repos/{repo_name}/statuses/{sha}.txt'.format(
        repo_name=repo_name,
        sha=sha
    )

    headers = {
        'Authorization': 'Bearer ' + auth_token
    }

    json = {
        "state": status,
        "target_url": "http://145.14.102.143/" + sha,
        "description": description,
        "context": "continuous-integration/dd2480"
    }
    requests.post(url, json=json, headers=headers)

if __name__ == '__main__':
    #   Used for testing only
    #
    #   with open("src/CI/data/demo_payload.json") as f:
    #       payload = json.load(f)
    #   
    #       handle_push(payload)
        
    if not os.path.isdir("/tmp/CILogs"):
        os.mkdir("/tmp/CILogs")

    #TODO: change port 81 to different port when webhook can be changed. Webserver should be 80 and webhook somthing else :)
    subprocess.Popen(["python3","-m","http.server","81","-d","/tmp/CILogs"])
    app.run(debug=True, host='0.0.0.0',port=80) 
    