from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime
import settings
import smtplib


def exception_log_format(sender, subject, date):
    now = datetime.now()
    filename = settings.LOGS_DIR / f'{datetime.now().date().isoformat()}.log'
    exception_log_template = settings.EXCEPTION_TEMPLATE / f'Exception Log_{now.strftime("%d_%m_%Y")}.csv'

    df = pd.read_csv(filename, delimiter='|', header=None)
    df.columns = ['Date/Time Exception Occurred', 'Exception Reason', 'Date Email Sent', 'Email Subject',
                  'Email Sender']

    df.to_csv(exception_log_template, index=None)

    return df


def send_email(email, pw, recipient):
    now = datetime.now()
    server = smtplib.SMTP('smtp-mail.outlook.com:587')
    server.starttls()
    server.login(email, pw)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = "Failed SilverBack Instructions" + " " + now.strftime("%d/%m/%Y")
    body = "The robot has failed to scrape data from Silverback instructions.\n\n" \
           "For list of the emails which failed to be processed, please see the file attached.\n\n" \
           "Please note this email has been sent by Robotic Process Automation and the mailbox is not monitored.\n\n" \
           "If you have any queries please contact roseagh.terrins@therobotexchange.com"

    msg.attach(MIMEText(body, 'plain'))
    filename = settings.EXCEPTION_TEMPLATE / f'Exception Log_{now.strftime("%d_%m_%Y")}.csv'
    fp = open(filename, 'rb')
    payload = MIMEBase('application', 'octet-stream')
    # Attach an attachment to payload
    payload.set_payload((fp).read())
    encoders.encode_base64(payload)
    # Add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=f'Exception Log_{now.strftime("%d_%m_%Y")}.csv')
    msg.attach(payload)
    message = msg.as_string()
    server.sendmail(email, recipient, message)
