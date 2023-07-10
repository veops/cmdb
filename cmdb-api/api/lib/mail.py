# -*- coding:utf-8 -*- 

import smtplib
import time
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid

from flask import current_app


def send_mail(sender, receiver, subject, content, ctype="html", pics=()):
    """subject and body are unicode objects"""
    if not receiver:
        return
    if not sender:
        sender = current_app.config.get("DEFAULT_MAIL_SENDER")
    smtpserver = current_app.config.get("MAIL_SERVER")
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
    msg['Message-ID'] = make_msgid()
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

    if current_app.config.get("MAIL_USE_SSL") or current_app.config.get("MAIL_USE_TLS"):
        smtp = smtplib.SMTP_SSL(smtpserver)
    else:
        smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    if current_app.config.get("MAIL_PASSWORD") != "":
        smtp.login(current_app.config.get("MAIL_USERNAME"), current_app.config.get("MAIL_PASSWORD")) 
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
