# -*- coding:utf-8 -*- 


import requests

from flask import current_app
from flask.ext.mail import Message

from extensions import mail
from models.account import User


def sendmail(users, subject, message, html=False, app=None):
    if app:
        mail.app = app
    else:
        app = current_app
    recipients = [x.email for x in users if isinstance(x, User)]
    recipients.extend(
        [x for x in users if isinstance(x, basestring) and '@' in x])
    sender = app.config.get('DEFAULT_MAIL_SENDER')
    if html:
        msg = Message(recipients=recipients,
                      html=message,
                      subject=subject,
                      sender=sender)
    else:
        msg = Message(recipients=recipients,
                      body=message,
                      subject=subject,
                      sender=sender)
    mail.send(msg)


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
import smtplib
import time
from email import Utils


def send_mail(sender, receiver, subject, content, ctype="html", pics=(),
              smtpserver='mail.51ping.com',
              username="networkbench@51ping.com", password="12qwaszx"):
    """subject and body are unicode objects"""
    if ctype == "html":
        msg = MIMEText(content, 'html', 'utf-8')
    else:
        msg = MIMEText(content, 'plain', 'utf-8')

    if len(pics) != 0:
        msgRoot = MIMEMultipart('related')
        msgText = MIMEText(content, 'html', 'utf-8')
        msgRoot.attach(msgText)
        i = 1
        for pic in pics:
            fp = open(pic, "rb")
            image = MIMEImage(fp.read())
            fp.close()
            image.add_header('Content-ID', '<img%02d>' % i)
            msgRoot.attach(image)
            i += 1
        msg = msgRoot

    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)
    msg['Message-ID'] = Utils.make_msgid()
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def send_sms(mobile, content):
    sms_uri = current_app.config.get("SMS_URI") % (mobile, content)
    try:
        current_app.logger.info(sms_uri)
        requests.get(sms_uri)
    except Exception as e:
        current_app.logger.error("send sms error, %s" % str(e))