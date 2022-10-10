"""
auto_send_followup.py checks through emails in one's inbox against a csv of user-created followup reminders, 
if today's date matches the recorded followup date, and no response email is found in the inbox,
opens and saves a draft with a pre-written followup message
"""

from re import sub
import win32com.client as win32
import csv
import datetime
import os

CSV_PATH = "followUps.csv"
USER_EMAIL = os.getenv("USER_EMAIL") 
# get access to outlook
outlook = win32.Dispatch("Outlook.Application")


def logFollowUp():
    # TODO do not allow any input to be blank
    # have user craft a response message when sending another message
    message_to_follow_up_on = input("What is the subject of the message you would like to follow up on?")
    # TODO add check to make sure input is in the correct format
    day_to_follow_up_on = input("What is the date you want to follow up on? (MM/DD/YY)")
    follow_up_email_address = input("What email do you want the follow up message sent to?")
    content_of_follow_up_message = input("What do you want the body of the follow up message to be?")
    csv_row = (message_to_follow_up_on, day_to_follow_up_on, follow_up_email_address, content_of_follow_up_message)
    # Store inputs in a csv
    with open(CSV_PATH, "a", encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_row)


# Get data from csv 
follow_up_subject_lines = []
follow_up_dates = []
follow_up_body_text = []
follow_up_to_email = []
csv_row_to_remain = []
with open("followUps.csv", "r") as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        temp_tuple = ()
        follow_up_subject_lines.append(line[0])
        follow_up_dates.append(line[1])
        follow_up_to_email.append(line[2])
        follow_up_body_text.append(line[3])
        temp_tuple = (line[0], line[1], line[2], line[3])
        csv_row_to_remain.append(temp_tuple)

# Gets subjects of all messages in the inbox 
olNS = outlook.GetNameSpace("MAPI")
inbox = olNS.GetDefaultFolder(6)
messages = inbox.Items


# Check if the dates Match
now = datetime.datetime.now()
todays_date = now.strftime("%x")
for message in messages:
    subject = message.Subject
    for date in follow_up_dates:
        # Check if there is a reply to the message 
        index_in_list = follow_up_dates.index(date)
        # print(follow_up_subject_lines[index_in_list])
        if subject == "RE: " + follow_up_subject_lines[index_in_list] and todays_date == date:
            print(subject)
            # TODO send email to remind self that follow up is canceled because program found a reply, follow up email
            message = outlook.CreateItem(0) 
            message.To = USER_EMAIL
            message.Subject = f"Follow up on {subject} NOT sent, response found in inbox"
            message.BodyFormat = 1
            message.Body = "Body of the email"
            message.Sender = USER_EMAIL
            message.save()
            print("Message to self saved to drafts, send not working rn")

            # delete entry from the csv
            csv_row_to_remain.remove(csv_row_to_remain[index_in_list])
        elif subject == follow_up_subject_lines[index_in_list] and todays_date == date:
            # TODO email out follow up
            message = outlook.CreateItem(0) 
            # TODO include email to send this to
            message.To = follow_up_to_email[index_in_list]
            message.BCC = USER_EMAIL
            message.Subject = f"Follow up on {subject}"
            message.BodyFormat = 1
            message.Body = follow_up_body_text[index_in_list]
            message.Sender = USER_EMAIL
            message.save()
            print("Message saved to drafts, and record removed from CSV. Go to drafts and proof then send.")

            # delete entry from the csv
            csv_row_to_remain.remove(csv_row_to_remain[index_in_list])
        # TODO add an option if the date has passed and program has not been run


# rewrite to csv after loop completes
with open(CSV_PATH, "w", encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_row_to_remain)


# TODO Later: include other folders other than the inbox?
# other folders to check for return message = input("What folders other than the inbox should be checked before sending the follow up?")

# Running for testing purposes
if __name__ == "__main__":
    logFollowUp()
