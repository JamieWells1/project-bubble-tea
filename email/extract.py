"""Gets rid of emails that are:

- Duplicate
- .edu
- .ac
"""

import os
import re


def extract_emails_from_file(file_path):
    """
    Extracts all valid emails from the given file.
    Returns a list of email strings.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, content)

    return emails


def save_filtered_emails(email_list, output_file):
    """
    Filters out duplicates and .ac/.edu domains and their subdomains.
    """
    # Regex: ends with .ac, .edu or any .ac.* / .edu.*
    blocked_pattern = re.compile(
        r"@[\w.-]*\.ac(\.\w+)?$|@[\w.-]*\.edu(\.\w+)?$", re.IGNORECASE
    )

    unique_emails = {
        email.strip().lower()
        for email in email_list
        if not blocked_pattern.search(email)
    }

    with open(output_file, "w") as f:
        for email in sorted(unique_emails):
            f.write(email + "\n")

    print(f"✅ {len(unique_emails)} emails saved to '{output_file}'.")


source_file = "unused-emails.txt"
emails = extract_emails_from_file(source_file)
save_filtered_emails(emails, source_file)
