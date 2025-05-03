from typing import List, Dict
import logging
import time
import sys

from correo import Correo

logger = logging.getLogger(__name__)


UNUSED_EMAILS_FILE_PATH = "unused-emails.txt"
USED_EMAILS_FILE_PATH = "used-emails.txt"


def __read_emails_from_file(file_path: str, num_emails: int = None) -> List[str]:
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if num_emails is not None:
        return lines[:num_emails]
    return lines


from typing import List, Dict


def send_multiple(num_emails: int) -> Dict[str, str]:
    """
    Reads from emails.txt, sends specified number of emails to the first x, 
    removes those emails from that file and writes them to an unused-emails.txt file
    """
    emails: List[str] = __read_emails_from_file(UNUSED_EMAILS_FILE_PATH, num_emails)
    successful_sends = 0

    for i, email in enumerate(emails):
        if (i + 1) % 50 == 0:
            print(f"\n=> Number of requests has reached {i + 1}. Will resend in 24 hours.")
            sys.stdout.flush()
            time.sleep(86400)
        try:
            new_email = Correo(email)
            response = new_email.send()

            if response.get("id"):
                print(f"\n=> Sent email #{i + 1} to {email}")
                successful_sends += 1
                time.sleep(2)
            else:
                print(f"\n=> Couldn't send email #{i + 1} to {email}")
                break

        except Exception as e:
            print(f"\n=> Exception sending email #{i + 1} to {email}: {e}")
            break

    if successful_sends > 0:
        # Update the files
        with open(UNUSED_EMAILS_FILE_PATH, "r") as f:
            all_emails = [line.strip() for line in f if line.strip()]

        # Remove the first 'successful_sends' emails
        remaining_emails = all_emails[successful_sends:]

        with open(UNUSED_EMAILS_FILE_PATH, "w") as f:
            f.write("\n".join(remaining_emails) + "\n")

        # Append the used emails to used-emails.txt
        with open(USED_EMAILS_FILE_PATH, "a") as f:
            for used_email in emails[:successful_sends]:
                f.write(used_email + "\n")

        print(
            f"\nMoved {successful_sends} emails to {USED_EMAILS_FILE_PATH} successfully."
        )

    return {"status": "completed", "emails_sent": successful_sends}


def send_email(recipient: str) -> None:
    new_email = Correo(recipient)
    print(f"\n=> {new_email.send()}")
