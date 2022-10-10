"""
save_plaintext_email_to_drafts.py saves a message to drafts, 
message.send() does not work on my machine
"""


import win32com.client as win32
import os
from datetime import datetime, timedelta

outlook = win32.Dispatch("Outlook.Application")
namespace_object = outlook.GetNameSpace("MAPI")
message = outlook.CreateItem(0) 



message.To = "owenpickard89@gmail.com"
message.BCC = "info@vardaconcealedcarry.com"
message.Subject = "Test with Python"
message.BodyFormat = 1
message.Body = "Body of the email"
message.Sender = "info@vardaconcealedcarry.com"

# Selecting the correct outlook account
message._oleobj_.Invoke(*(64209, 0, 8, 0, namespace_object.Accounts.Item("info@vardaconcealedcarry.com")))

message.Display()
# To save to drafts
message.save()  
# To send the message
message.send()