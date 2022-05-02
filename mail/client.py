import smtplib, ssl
from mail.message import Message


class Client:
    def __init__(self):
        self.smtp_server = 'smtp.ionos.mx'
        self.tls_port = 587
        self.sender_email = 'info@ultimate-impulse.com'
        self.sender_pass = '5&6#XATx^$+QBrJt'

    def send_email(self, receiver_email, message: Message, mappings: dict):
        content = message.build(self.sender_email, receiver_email, mappings)
        context = ssl.create_default_context()

        with smtplib.SMTP(self.smtp_server, self.tls_port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.sender_pass)
            server.sendmail(self.sender_email, receiver_email, content)
