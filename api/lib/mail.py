# -*- coding:utf-8 -*- 


from flask import current_app

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
import smtplib
import time
from email import Utils


def send_mail(sender, receiver, subject, content, ctype="html", pics=()):
    """subject and body are unicode objects"""
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
    msg['Message-ID'] = Utils.make_msgid()
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    # smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
