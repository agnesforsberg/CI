import unittest

import os
import json
import imaplib
import email
from email.header import decode_header
from src.CI import app
from src.CI import notification
import random, string


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_index(self):
        self.assertEqual("Hello :)", app.index())


    def test_clone_repo(self):
        # Run clone_repo with demo_payload.json and check the 3 functionalities
        with open('./src/CI/data/demo_payload.json') as json_file:
            content = json.load(json_file)
        app.clone_repo(content, 'testrepo')
        output = os.popen("git -C testrepo status").read()


        # 1 - Repo was cloned, checked by lack of error message
        self.assertFalse("fatal" in output)

        # 2 - git pull has been performed, and therefore "Your branch is up to date in output"
        self.assertTrue("up to date" in output)

        # 3 - on correct branch, should be main
        self.assertTrue("On branch main" in output)

        # cleanup
        os.system("rm -r testrepo")

    # Tests the send_notification function by sending a test email and asserting that the correct email arrived.
    def test_notification(self):
        message = "Test1"
        notification.send_notification(message)

        email_address = "group.19.dd2480@gmail.com"
        password = "whyiscisohard"
        mailbox = imaplib.IMAP4_SSL("imap.gmail.com")
        mailbox.login(email_address, password)
        mailbox.select("inbox")

        # Find latest email
        _, mail_data = mailbox.search(None, 'ALL')
        mail_ids = mail_data[0]
        latest_email_id = mail_ids.split()[-1]

        # Fetch the latest email (last in list)
        _, data = mailbox.fetch(latest_email_id, '(RFC822)')
        if isinstance(data[0], tuple):
            msg = email.message_from_bytes(data[0][1])
            # Assert body is correct
            body = msg.get_payload(decode=True).decode()
            self.assertEqual(str(body).strip(), "Test1")

            # Assert sender is correct
            sender, _ = decode_header(msg.get("From"))[0]
            self.assertEqual(str(sender), "group.19.dd2480@gmail.com")

    def test_pytest_if_no_tests_in_dir(self):
    	"""Pytest should not raise an exception if the target directory is empty.
    	"""
    	try:
    		path = './a' + ''.join([e for e in random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])
    		os.mkdir(path)
    		app.exec_pytest(path)
    	except:
    		assert False

    def test_pylint_if_no_python_in_dir(self):
    	"""Pylint should not raise an exception if the target directory is empty.
    	"""
    	try:
    		path = './a' + ''.join([e for e in random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])
    		os.mkdir(path)
    		app.exec_pylint(path)
    	except:
    		assert False
