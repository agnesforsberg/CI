# **CI**
This project implements a simple continuous integration (CI) server. It is built to be used with the webhook functionality provided by Github when there is a push event. Once the server recieves a request from the webhook it will run the tests of the pushing branch and return a report of the status of the branch.

# Features
* Static analysis on python code (pylint)
* Test automation on python code (pytest)
* Notification via mail and status update on github on push events 

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
