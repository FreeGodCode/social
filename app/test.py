# -*- coding: utf-8  -*-
# @Author: ty
# @File name: test.py 
# @IDE: PyCharm
# @Create time: 1/6/21 3:41 PM
from flask_mail import Message

from app import config


def send_email(to, subject):
    """
    邮件发送
    :param to:
    :param subject:
    :return:
    """
    msg = Message(subject=config.from_object.MAIL_SUBJECT_PREFIX + subject, sender=config.from_object.MAIL_SENDER, recipients=[to])
    msg.body = '测试邮件'
    msg.html = "<a href='://baidu.com'>点击打开百度</a>"