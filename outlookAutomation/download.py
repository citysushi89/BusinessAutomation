from pathlib import Path
from re import sub
import win32com.client as win32
import re

# download.py accesses outlook inbox and prints the subject line of each message

# Create output folder
output_dir = Path.cwd() / "Output"
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to outlook
outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")

# Connect to folder (6 means inbox)
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items

# For properties below, if issues, check the capitlization of the .property
for message in messages:
    subject = message.Subject
    print(subject)


# There is more code for the loop in the tutorial, but too many unicode errors, do not want to download all that anyway
# Resource: https://www.youtube.com/watch?v=oyEMi8sDVOM