from typing import List

from email import Email


def read_emails_from_file(file_path) -> List[str]:
    with open(file_path, "r") as f:
        emails = [line.strip() for line in f if line.strip()]


def mass_send():
    emails: List[str] = read_emails_from_file("emails.txt")


def main():
    mass_send()
