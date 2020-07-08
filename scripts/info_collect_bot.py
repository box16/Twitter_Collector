import tweepy
import datetime
from config import create_api
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os

users = [
"yuchrszk",
"gigazine",
]

from_email = os.getenv("FROM_EMAIL")
to_email = os.getenv("TO_EMAIL")
password = os.getenv("FROM_EMAIL_PASSWORD")

def collect_info():
    api = create_api()
    body = ""
    for user in users:
        for tweet in api.user_timeline(user):
            diff_today = abs((tweet.created_at - datetime.datetime.now()).days)
            if diff_today <= 1:
                body += "-----\n" + tweet.text + "\n-----\n\n"
    return body

def create_massege(body):
    msg = MIMEText(body)
    msg['Subject'] = "collect" + str(datetime.datetime.now())
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Bcc'] = to_email
    msg['Date'] = formatdate()
    return msg

def send(msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_email, password)
    smtpobj.sendmail(from_email, to_email, msg.as_string())
    smtpobj.close()

if __name__ == "__main__":
    body = collect_info()
    msg = create_massege(body)
    send(msg)