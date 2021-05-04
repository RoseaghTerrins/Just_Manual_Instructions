from email_account import get_email, is_silverback, send_notification_email, is_instruction
from data_collector import write_to_sf
from datetime import datetime
from silverback import silverback
import logging
import settings as settings
from exception_logging import exception_log_format, send_email

logging.basicConfig(
    filename=settings.LOGS_DIR / f'{datetime.now().date().isoformat()}.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def main():
    global date, subject, sender
    unread_emails, unread_raw_emails = get_email(settings.OUTLOOK_EMAIL, settings.OUTLOOK_PASSWORD)
    success_counter = 0
    exception_counter = 0
    email_list = ["roseagh.terrins@therobotexchange.com", "william.watson@justdebt.co.uk",  "daniel.woolley@justdebt.co.uk", "donna.draycott@justdebt.co.uk"]
    for (unread_email, unread_raw_email) in zip(unread_emails, unread_raw_emails):
        try:
            sender = unread_raw_email['From']
            subject = unread_raw_email['Subject']
            date = unread_raw_email['Date']
            print(subject)
            if is_silverback(sender) and is_instruction(subject):
                data = silverback(unread_email, sender, subject)
                print(data)
                write_to_sf("misterrobot@justdebt.co.uk", "RobotEx6754!!", "A75grTVJGbPIz0aBjWemUIFFU", data)
                success_counter = success_counter + 1
            else:
                pass
        except Exception as e:
            logger.error("|An error has occurred scraping email" + ' ' + str(e) + '|' + str(date) + '|' + str(subject) + '|' + str(sender))
            exception_log_format(sender, subject, date)
            exception_counter = exception_counter + 1

    if success_counter >= 1:
        for email in email_list:
            send_notification_email("inbound@justdebt.co.uk", "Cot53069", email)
    else:
        pass
    if exception_counter >= 1:
        for email in email_list:
            send_email("inbound@justdebt.co.uk", "Cot53069", email)
    else:
        pass


if __name__ == '__main__':
    main()
