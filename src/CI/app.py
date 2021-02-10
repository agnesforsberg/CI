from flask import Flask, request
import pytest
import os
import subprocess
import json
from pylint import epylint as lint
import notification

demo_payload ="""{
    "after": "5a05bc0238d14645ac0a655850b3462e4e970100",
    "base_ref": null,
    "before": "1f1e999ad71a0140fe83f999466a85e6a722c4c7",
    "commits": [
        {
            "added": [],
            "author": {
                "email": "ntomsic@kth.se",
                "name": "unknown",
                "username": "ntomsic"
            },
            "committer": {
                "email": "ntomsic@kth.se",
                "name": "unknown",
                "username": "ntomsic"
            },
            "distinct": true,
            "id": "5a05bc0238d14645ac0a655850b3462e4e970100",
            "message": "testing",
            "modified": [
                "src/CI/app.py"
            ],
            "removed": [],
            "timestamp": "2021-02-09T12:41:56+01:00",
            "tree_id": "5f9842796121ccddf6d5b047a9397d64f5e7cef5",
            "url": "https://github.com/agnesforsberg/CI/commit/5a05bc0238d14645ac0a655850b3462e4e970100"
        }
    ],
    "compare": "https://github.com/agnesforsberg/CI/compare/1f1e999ad71a...5a05bc0238d1",
    "created": false,
    "deleted": false,
    "forced": false,
    "head_commit": {
        "added": [],
        "author": {
            "email": "ntomsic@kth.se",
            "name": "unknown",
            "username": "ntomsic"
        },
        "committer": {
            "email": "ntomsic@kth.se",
            "name": "unknown",
            "username": "ntomsic"
        },
        "distinct": true,
        "id": "5a05bc0238d14645ac0a655850b3462e4e970100",
        "message": "testing",
        "modified": [
            "src/CI/app.py"
        ],
        "removed": [],
        "timestamp": "2021-02-09T12:41:56+01:00",
        "tree_id": "5f9842796121ccddf6d5b047a9397d64f5e7cef5",
        "url": "https://github.com/agnesforsberg/CI/commit/5a05bc0238d14645ac0a655850b3462e4e970100"
    },
    "pusher": {
        "email": "ccyfzz@gmail.com",
        "name": "ntomsic"
    },
    "ref": "refs/heads/testing",
    "repository": {
        "archive_url": "https://api.github.com/repos/agnesforsberg/CI/{archive_format}{/ref}",
        "archived": false,
        "assignees_url": "https://api.github.com/repos/agnesforsberg/CI/assignees{/user}",
        "blobs_url": "https://api.github.com/repos/agnesforsberg/CI/git/blobs{/sha}",
        "branches_url": "https://api.github.com/repos/agnesforsberg/CI/branches{/branch}",
        "clone_url": "https://github.com/agnesforsberg/CI.git",
        "collaborators_url": "https://api.github.com/repos/agnesforsberg/CI/collaborators{/collaborator}",
        "comments_url": "https://api.github.com/repos/agnesforsberg/CI/comments{/number}",
        "commits_url": "https://api.github.com/repos/agnesforsberg/CI/commits{/sha}",
        "compare_url": "https://api.github.com/repos/agnesforsberg/CI/compare/{base}...{head}",
        "contents_url": "https://api.github.com/repos/agnesforsberg/CI/contents/{+path}",
        "contributors_url": "https://api.github.com/repos/agnesforsberg/CI/contributors",
        "created_at": 1612712686,
        "default_branch": "main",
        "deployments_url": "https://api.github.com/repos/agnesforsberg/CI/deployments",
        "description": null,
        "disabled": false,
        "downloads_url": "https://api.github.com/repos/agnesforsberg/CI/downloads",
        "events_url": "https://api.github.com/repos/agnesforsberg/CI/events",
        "fork": false,
        "forks": 1,
        "forks_count": 1,
        "forks_url": "https://api.github.com/repos/agnesforsberg/CI/forks",
        "full_name": "agnesforsberg/CI",
        "git_commits_url": "https://api.github.com/repos/agnesforsberg/CI/git/commits{/sha}",
        "git_refs_url": "https://api.github.com/repos/agnesforsberg/CI/git/refs{/sha}",
        "git_tags_url": "https://api.github.com/repos/agnesforsberg/CI/git/tags{/sha}",
        "git_url": "git://github.com/agnesforsberg/CI.git",
        "has_downloads": true,
        "has_issues": true,
        "has_pages": false,
        "has_projects": true,
        "has_wiki": true,
        "homepage": null,
        "hooks_url": "https://api.github.com/repos/agnesforsberg/CI/hooks",
        "html_url": "https://github.com/agnesforsberg/CI",
        "id": 336823784,
        "issue_comment_url": "https://api.github.com/repos/agnesforsberg/CI/issues/comments{/number}",
        "issue_events_url": "https://api.github.com/repos/agnesforsberg/CI/issues/events{/number}",
        "issues_url": "https://api.github.com/repos/agnesforsberg/CI/issues{/number}",
        "keys_url": "https://api.github.com/repos/agnesforsberg/CI/keys{/key_id}",
        "labels_url": "https://api.github.com/repos/agnesforsberg/CI/labels{/name}",
        "language": "Python",
        "languages_url": "https://api.github.com/repos/agnesforsberg/CI/languages",
        "license": null,
        "master_branch": "main",
        "merges_url": "https://api.github.com/repos/agnesforsberg/CI/merges",
        "milestones_url": "https://api.github.com/repos/agnesforsberg/CI/milestones{/number}",
        "mirror_url": null,
        "name": "CI",
        "node_id": "MDEwOlJlcG9zaXRvcnkzMzY4MjM3ODQ=",
        "notifications_url": "https://api.github.com/repos/agnesforsberg/CI/notifications{?since,all,participating}",
        "open_issues": 8,
        "open_issues_count": 8,
        "owner": {
            "avatar_url": "https://avatars.githubusercontent.com/u/66953501?v=4",
            "email": "66953501+agnesforsberg@users.noreply.github.com",
            "events_url": "https://api.github.com/users/agnesforsberg/events{/privacy}",
            "followers_url": "https://api.github.com/users/agnesforsberg/followers",
            "following_url": "https://api.github.com/users/agnesforsberg/following{/other_user}",
            "gists_url": "https://api.github.com/users/agnesforsberg/gists{/gist_id}",
            "gravatar_id": "",
            "html_url": "https://github.com/agnesforsberg",
            "id": 66953501,
            "login": "agnesforsberg",
            "name": "agnesforsberg",
            "node_id": "MDQ6VXNlcjY2OTUzNTAx",
            "organizations_url": "https://api.github.com/users/agnesforsberg/orgs",
            "received_events_url": "https://api.github.com/users/agnesforsberg/received_events",
            "repos_url": "https://api.github.com/users/agnesforsberg/repos",
            "site_admin": false,
            "starred_url": "https://api.github.com/users/agnesforsberg/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/agnesforsberg/subscriptions",
            "type": "User",
            "url": "https://api.github.com/users/agnesforsberg"
        },
        "private": false,
        "pulls_url": "https://api.github.com/repos/agnesforsberg/CI/pulls{/number}",
        "pushed_at": 1612870947,
        "releases_url": "https://api.github.com/repos/agnesforsberg/CI/releases{/id}",
        "size": 4,
        "ssh_url": "git@github.com:agnesforsberg/CI.git",
        "stargazers": 0,
        "stargazers_count": 0,
        "stargazers_url": "https://api.github.com/repos/agnesforsberg/CI/stargazers",
        "statuses_url": "https://api.github.com/repos/agnesforsberg/CI/statuses/{sha}",
        "subscribers_url": "https://api.github.com/repos/agnesforsberg/CI/subscribers",
        "subscription_url": "https://api.github.com/repos/agnesforsberg/CI/subscription",
        "svn_url": "https://github.com/agnesforsberg/CI",
        "tags_url": "https://api.github.com/repos/agnesforsberg/CI/tags",
        "teams_url": "https://api.github.com/repos/agnesforsberg/CI/teams",
        "trees_url": "https://api.github.com/repos/agnesforsberg/CI/git/trees{/sha}",
        "updated_at": "2021-02-08T12:41:49Z",
        "url": "https://github.com/agnesforsberg/CI",
        "watchers": 0,
        "watchers_count": 0
    },
    "sender": {
        "avatar_url": "https://avatars.githubusercontent.com/u/9111903?v=4",
        "events_url": "https://api.github.com/users/ntomsic/events{/privacy}",
        "followers_url": "https://api.github.com/users/ntomsic/followers",
        "following_url": "https://api.github.com/users/ntomsic/following{/other_user}",
        "gists_url": "https://api.github.com/users/ntomsic/gists{/gist_id}",
        "gravatar_id": "",
        "html_url": "https://github.com/ntomsic",
        "id": 9111903,
        "login": "ntomsic",
        "node_id": "MDQ6VXNlcjkxMTE5MDM=",
        "organizations_url": "https://api.github.com/users/ntomsic/orgs",
        "received_events_url": "https://api.github.com/users/ntomsic/received_events",
        "repos_url": "https://api.github.com/users/ntomsic/repos",
        "site_admin": false,
        "starred_url": "https://api.github.com/users/ntomsic/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ntomsic/subscriptions",
        "type": "User",
        "url": "https://api.github.com/users/ntomsic"
    }
}
"""

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
    handle_push(json.loads(demo_payload))
    app.run(debug=True, host='0.0.0.0',port=80)
