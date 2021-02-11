"""contains the function for sending a notification email to the receiver email"""
# account name: group.19.dd2480@gmail.com
# account password: whyiscisohard

import smtplib
import ssl

PORT = 465  # For SSL
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "group.19.dd2480@gmail.com"
RECEIVER_EMAIL = "group.19.dd2480@gmail.com"
PASSWORD = "whyiscisohard"


def send_notification(message):
    """Sends an email to the receiver email using a smtp server"""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
