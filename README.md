# **CI**
This project implements a simple continuous integration (CI) server. It is built to be used with the webhook functionality provided by Github when there is a push event. Once the server recieves a request from the webhook it will run the tests of the pushing branch and return a report of the status of the branch. The implementation also provides a web server that hosts the results of the testing/linting.

## Features
### Static analysis on python code (pylint)
### Test automation on python code (pytest)
### Notification via mail and status update on github on push events
Notification is implemented via email by sending a mail from our local email account to the designated email
addresses via an SMTP server. Notification is also implemented via status updates by sending a request to the
Github API to update the commit status.

The email notification implementation is tested by sending a test email to a
local designated receiver and comparing the subject and body of the email sent, and the email received. The status update
test is also implemented similarly, with a test status update being sent to the repository and by comparing the message
that was sent with the one that was received.
### Persistent storage and hosting of test/linting results on http://localhost:81

## How to use:
To install all dependencies and run the server do: 
```
make all
```

A personal access token is also required to update commit statuses. It can be generated [here](https://github.com/settings/tokens) and should be placed in /tmp/auth.


## Requirements
* Python ~= 3.8.5
* Pip ~= 20.0.2
* Make ~= 4.2.1

## Contributions

- **Jakob Berggren**
  - Project Leader / Manager of PR's
  - Authored the README
  - Author of MAKEFILE
- **E-Joon Ko**
  - Work on core CI feature #3: Notification.
  - Wrote and updated requirements.txt
  - Refactoring code.
- **Agnes Forsberg**
  - Set up webhook.
  - Work on core CI feature #3: Notification.
  - Testing for send_notification and clone_repo.
- **Niklas Tomsic**
  - Cloning, linting and testing on the raspberry PI
  - Storing and accessing logs
  - Status update implementation
- **Caroline Borg**
  - Set up Raspberry PI
  - Code refactor
  - Co-author of commit status implementation
  - Idea machine.
