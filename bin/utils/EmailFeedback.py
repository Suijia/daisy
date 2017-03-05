#!/usr/bin/env python
# -*-coding:utf-8-*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import tornado.log
import yaml

mail_user = "pudding_42"  # 用户名
mail_postfix = "163.com"  # 发件箱的后缀
mail_host = "smtp." + mail_postfix  # 设置服务器
mail_address = mail_user + "@" + mail_postfix


def send_mail_feedback(sub, content, pass_word=""):
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = Header(sub, 'utf-8')

    msg['From'] = "DAISY <{0}>".format(mail_address)
    msg['To'] = 'User Feedback <{0}>'.format(mail_address)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.set_debuglevel(5)
        server.login(mail_user, pass_word)
        server.sendmail(mail_address, [mail_address], msg.as_string())
        tornado.log.app_log.info(msg.as_string())
        tornado.log.app_log.info(
            '邮件发送成功：\n\t标题：{0}\n\tFrom：{1}\n\tTO：{2}\n\t正文：\n\t\t{3}'.format(
                sub.encode('utf-8'), msg['From'].encode('utf-8'),
                msg['To'].encode('utf-8'), content.encode('utf-8')))
        server.quit()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__ == '__main__':
    import logging.handlers
    formatter = logging.Formatter("[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s")
    fileHandlerApp = logging.handlers.WatchedFileHandler("logs/app.log")
    fileHandlerApp.setFormatter(formatter)
    tornado.log.app_log.addHandler(fileHandlerApp)
    tornado.log.app_log.setLevel(logging.INFO)
    conf = yaml.load(open('conf/service.yaml', 'r'))

    if send_mail_feedback(u"中文hello", u"中文python send mail test", conf.get('email_password', "")):
        print "发送成功"
    else:
        print "发送失败"
