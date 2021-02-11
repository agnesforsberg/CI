import unittest
import imaplib
import email
from email.header import decode_header
from src.CI import app
from src.CI import notification


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_index(self):
        self.assertEqual("Hello :)", app.index())

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

