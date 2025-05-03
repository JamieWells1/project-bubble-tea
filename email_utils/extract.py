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


import re


def save_filtered_emails(email_list, output_file):
    """
    Filters out duplicates and domains containing blocked patterns (.ac, .edu, .co.uk, .org, .net, etc.).
    """
    # List of blocked domain patterns (you can easily extend this)
    blocked_keywords = ["ac", "edu", "co.uk", "org", "net"]

    # Dynamically build the regex
    blocked_pattern = re.compile(
        r"@[\w.-]*("
        + "|".join(re.escape(kw) for kw in blocked_keywords)
        + r")(\.\w+)?$",
        re.IGNORECASE,
    )

    unique_emails = {
        email.strip().lower()
        for email in email_list
        if not blocked_pattern.search(email)
    }

    with open(output_file, "w") as f:
        for email in sorted(unique_emails):
            f.write(email + "\n")

    print(f"{len(unique_emails)} emails saved to '{output_file}'.")


source_file = "unused-emails.txt"
emails = extract_emails_from_file(source_file)
save_filtered_emails(emails, source_file)
