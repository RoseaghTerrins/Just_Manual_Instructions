import imaplib
from email import message_from_bytes
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64


def get_email(username, password):
    # Connect to imap server
    username = 'inbound@justdebt.co.uk'
    password = 'Cot53069'
    mail = imaplib.IMAP4_SSL('outlook.office365.com')
    mail.login(username, password)

    # retrieve a list of the mailboxes and select one
    result, mailboxes = mail.list()
    mail.select("inbox")

    # retrieve a list of the UIDs for all of the messages in the select mailbox
    result, numbers = mail.uid('search', None, 'UnSeen')
    uids = numbers[0].split()

    # retrieve the headers (without setting the 'seen' flag) of the last 10 messages
    # in the list of UIDs

    unread_messages = []
    raw_email_message = []

    for item in uids:
        result, messages = mail.uid('fetch', item, '(RFC822)')
        raw_email = messages[0][1]
        email_message = message_from_bytes(raw_email)
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                msg = part.get_payload()
                msg = msg.encode('ascii')
                msg = base64.b64decode(msg)
                msg = message_from_bytes(msg)
                unread_messages.append(msg)
                unread_messages.append(msg)
            else:
                pass
        raw_email_message.append(email_message)
        copy_result = mail.uid('COPY', item, "Processed_Items")

        if result == 'OK' and copy_result[0] == 'OK':
            mail.uid('STORE', item, '+FLAGS', '(\\Deleted)')
            mail.expunge()
        else:
            raise ValueError("Bot could not move email into processed items folder")

    return unread_messages, raw_email_message


def is_silverback(from_) -> bool:
    if "silverback" in from_:
        var = True
    else:
        var = False

    return var


def is_instruction(subject):
    if "Instructions to Issue Writ of Fi Fa" in subject:
        var = True
    else:
        var = False
    return var


def read_text(email) -> str:
    return str([part for part in email if email.part.get_content_type() == 'text/plain'][0])


def get_value(marker, email):
    for line in read_text().splitlines():
        if line.startswith(marker):
            return line.replace(marker, '').strip()
    raise Exception(f'Unable to find {marker.replace(":", "")}')


def get_text_between(start: str, end: str, text) -> str:
    """Helper to extract text between two markers from the pdf."""

    text = str(text)

    idx_1 = text.find(start)

    if idx_1 < 0:
        raise ValueError(f'Unable to locate "{start}" in email body text.')

    text = text[idx_1 + len(start):]
    idx_2 = text.find(end)

    if idx_2 < 0:
        raise ValueError(f'Unable to locate "{end}" in email body text')

    return text[:idx_2].strip()


def send_notification_email(email, pw, recipient):
    now = datetime.now()
    server = smtplib.SMTP('smtp-mail.outlook.com:587')
    server.starttls()
    server.login(email, pw)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = "SilverBack Instructions For Review" + " " + now.strftime("%d/%m/%Y")
    body = "Silverback instructions have been uploaded to Salesforce for your review.\n\n" \
           "Please do not reply as this email has been sent by Robotic Process Automation.\n\n" \
           "If you have any queries please contact roseagh.terrins@therobotexchange.com"
    msg.attach(MIMEText(body, 'plain'))
    message = msg.as_string()
    server.sendmail(email, recipient, message)
