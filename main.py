from typing import List
import logging

from correo import Correo

logger = logging.getLogger(__name__)


def __read_emails_from_file(file_path) -> List[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def mass_send():
    emails: List[str] = __read_emails_from_file("emails.txt")


def send_email(recipient: str) -> None:
    new_email = Correo(recipient)
    print(f"\n=> {new_email.send()}")


send_email("jamiewixbusiness@gmail.com")
