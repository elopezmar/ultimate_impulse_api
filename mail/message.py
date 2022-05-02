from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Message:
    def __init__(self, subject: str, html: str):
        self.subject = subject
        self.html = Template(html)

    def build(self, sender: str, receiver: str, mappings: str) -> str:
        content = MIMEMultipart('alternative')
        content['Subject'] = self.subject
        content['From'] = sender
        content['To'] = receiver
        content.attach(MIMEText(self.html.substitute(mappings), 'html'))
        return content.as_string()
