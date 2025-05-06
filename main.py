from typing import List
import logging
import time
import sys
import random

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


def send_multiple(num_emails: int) -> None:
    """
    Reads from unused-emails.txt, sends specified number of emails to random entries,
    removes them after each successful send, and writes to used-emails.txt.
    """
    successful_sends = 0

    with open(UNUSED_EMAILS_FILE_PATH, "r") as f:
        all_unused = [line.strip() for line in f if line.strip()]

    if len(all_unused) < num_emails:
        print(f"Not enough unused emails: requested: {num_emails}, available: {len(all_unused)}")
        num_emails = len(all_unused)

    for i in range(num_emails):
        if not all_unused:
            print("No more unused emails available.")
            break

        if (i + 1) % 80 == 0:
            print(f"\n=> Number of requests has reached {i + 1}. Will sleep for 24 hours.")
            sys.stdout.flush()
            time.sleep(86400)

        try:
            email = random.choice(all_unused)
            new_email = Correo(email)
            response = new_email.send()

            if response.get("id"):
                print(f"\nSent email #{i + 1} to {email}")
                successful_sends += 1
                time.sleep(2)

                all_unused.remove(email)

                with open(UNUSED_EMAILS_FILE_PATH, "w") as f:
                    f.write("\n".join(all_unused) + "\n")

                with open(USED_EMAILS_FILE_PATH, "a") as f:
                    f.write(email + "\n")

            else:
                print(f"\nCouldn't send email #{i + 1} to {email}")
                break

        except Exception as e:
            print(f"\nException sending email #{i + 1} to {email}: {e}")
            break

    result = {"status": "completed", "emails_sent": successful_sends}
    print(result)


def send_email(recipient: str) -> None:
    new_email = Correo(recipient)
    print(f"\n=> {new_email.send()}")


# send_email("jamiewells528@gmail.com")
send_multiple(5)
