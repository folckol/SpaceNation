import time
import imap_tools.errors
from imap_tools import MailBox

from bs4 import BeautifulSoup

providers = {
    "imap.rambler.ru": [
        'rambler.ru',
        'lenta.ru',
        'autorambler.ru',
        'myrambler.ru',
        'ro.ru',
        'rambler.ua'],
    "imap.firstmail.ltd": ["firstmailler.net",
                            "raymanmail.com",
                            "fmaild.com",
                            "dfirstmail.com",
                            "firstmailler.com",
                            "sfirstmail.com"],
    "outlook.office365.com": ['outlook.com'],
    "imap.mail.ru": ['mail.ru', 'internet.ru', 'bk.ru', 'inbox.ru', 'list.ru'],
    # "imap.gmail.com": 'gmail.com',
    "imap.yandex.ru": 'yandex.ru'
}


def get_provider(mails: str):
    pr = mails.split("@")[-1]
    for key, value in providers.items():
        if pr in value:
            return key
    return f"imap.{pr}"


def check_mail(mail, psw, _from):
    provider = get_provider(mail)
    retry_count = 0
    confirmation_code = None  # Initialize to None
    email_found = False  # Flag to indicate if the email is found

    while retry_count < 4 and not email_found:
        try:
            with MailBox(provider).login(mail, psw) as mailbox:
                for msg in mailbox.fetch(limit=20, reverse=True):  # Only fetch the most recent 20 emails

                    if msg.from_ == _from:
                        page = msg.html
                        # print(page)
                        soup = BeautifulSoup(page, 'html.parser')
                        # print(soup)
                        # extract verification link
                        verification_link_tag = soup.find('p', {'class': 'code'})
                        verification_link = verification_link_tag.text if verification_link_tag else None
                        if verification_link is not None:
                            # print(verification_link)
                            # print("The verification code is: ", confirmation_code)
                            email_found = True  # Set flag to True
                            break
                        else:
                            # print("Could not find verification code.")
                            pass
                if not email_found:  # Only check spam if email not found

                    try:
                        mailbox.folder.set('Spam')
                        for msg in mailbox.fetch(limit=20, reverse=True):  # Only fetch the most recent 20 spam emails

                            if msg.from_ == _from:
                                page = msg.html
                                # print(page)
                                soup = BeautifulSoup(page, 'html.parser')
                                # print(soup)
                                # extract verification link
                                verification_link_tag = soup.find('p', {'class': 'code'})
                                verification_link = verification_link_tag.text if verification_link_tag else None
                                if verification_link is not None:
                                    # print(verification_link)
                                    # print("The verification code is: ", confirmation_code)
                                    email_found = True  # Set flag to True
                                    break
                                else:
                                    # print("Could not find verification code.")
                                    pass
                    except:
                        pass

                if not email_found:  # Only retry if email not found
                    retry_count += 1
                    if retry_count < 4:
                        # logger.warning(f'Письмо не найдено, пробую еще раз, попытка {retry_count}/3')
                        time.sleep(15)
                    else:
                        return "no_mail"
        except imap_tools.errors.MailboxLoginError:
            return "error_login"

    if verification_link:
        # Return only the first match as a string
        return verification_link
    else:
        return "no_link"
