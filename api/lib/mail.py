# -*- coding:utf-8 -*- 


import smtplib
import time
from email import Utils
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


def send_mail(sender, receiver, subject, content, ctype="html", pics=()):
    """subject and body are unicode objects"""
    if not sender:
        sender = current_app.config.get("DEFAULT_MAIL_SENDER")
    smtp_server = current_app.config.get("MAIL_SERVER")
    if ctype == "html":
        msg = MIMEText(content, 'html', 'utf-8')
    else:
        msg = MIMEText(content, 'plain', 'utf-8')

    if len(pics) != 0:
        msg_root = MIMEMultipart('related')
        msg_text = MIMEText(content, 'html', 'utf-8')
        msg_root.attach(msg_text)
        i = 1
        for pic in pics:
            fp = open(pic, "rb")
            image = MIMEImage(fp.read())
            fp.close()
            image.add_header('Content-ID', '<img%02d>' % i)
            msg_root.attach(image)
            i += 1
        msg = msg_root

    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)
    msg['Message-ID'] = Utils.make_msgid()
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

    smtp = smtplib.SMTP()
    smtp.connect(smtp_server, 25)
    username, password = current_app.config.get("MAIL_USERNAME"), current_app.config.get("MAIL_PASSWORD")
    if username and password:
        smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
