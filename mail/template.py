from __future__ import annotations
from email.mime.text import MIMEText
import json
import string
from typing import Optional


class Template:
    def __init__(self, subject: str, html: str):
        self.subject = subject
        self.html = html

    def html_attach(self) -> Optional[MIMEText]:
        if self.html:
            return MIMEText(self.html, 'html')
        return None

    def build(self, mappings: dict) -> Template:
        self.html = string.Template(self.html).substitute(**mappings)


class Templates:
    activate_account = Template('activate_account')
    reset_password = Template('reset_password')