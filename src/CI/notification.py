# account name: group.19.dd2480@gmail.com
# account password: whyiscisohard

import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "group.19.dd2480@gmail.com"
receiver_email = "group.19.dd2480@gmail.com"
password = "whyiscisohard"


def send_notification(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
