from mailersend import emails
from dotenv import load_dotenv
import logging
import os

from typing import List

load_dotenv()


logger = logging.getLogger(__name__)

MAIL_FROM = {
    "name": "StudentVault",
    "email": "MS_OQ9L5U@studentvault.co.uk",
}

SUBJECT = "New Login On Your Account"


class Email:
    """
    New instance of this class will need to be created every time a new email is sent.
    """

    def __init__(self, recipient):
        self.mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))
        self.mail_body = {}
        self.mail_from = MAIL_FROM
        self.subject = SUBJECT
        self.recipients = [{"email": recipient}]

        self.__set_attributes()

    def __set_attributes(self):
        self.mailer.set_mail_from(self.mail_from, self.mail_body)
        self.mailer.set_mail_to(self.recipients, self.mail_body)
        self.mailer.set_subject(self.subject, self.mail_body)
        self.mailer.set_html_content("<h1>This is a H1</h1>", self.mail_body)

    def read_emails_from_file(file_path) -> List[str]:
        with open(file_path, "r") as f:
            emails = []

    def send(self):
        logger.info(self.mailer.send(self.mail_body))

    def mass_send(self):
        emails: List[str] = self.read_emails_from_file()
