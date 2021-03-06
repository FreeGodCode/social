# -*- coding: utf-8  -*-
# @Author: ty
# @File name: utils.py 
# @IDE: PyCharm
# @Create time: 12/27/20 10:09 PM
import json
import random
from threading import Thread

from bson import ObjectId
from flask import session, request, current_app
from flask_mail import Message


from app.code_msg import VERIFY_CODE_ERROR
from app.extensions import mail
from app.models.models import GlobalApiException


class JSONEncode(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def verify_code(code):
    """
    验证码验证
    :param code:
    :return:
    """
    if code != session['verify_code']:
        # raise 'verify_code_error'
        raise GlobalApiException(VERIFY_CODE_ERROR)


def generate_verify_code():
    """
    生成验证码
    :return:
    """
    a = random.randint(-20, 20)
    b = random.randint(0, 50)
    data = {'question': str(a) + '+' + str(b) + '= ?', 'answer': str(a + b)}
    session['verify_code'] = data['answer']
    return data


def generate_cache_key():
    """
    生成缓存key
    :return:
    """
    return 'view//' + request.full_path


def async_send_mail(app, msg):
    """
    异步发送邮件
    :param app:
    :param msg:
    :return:
    """
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, body, is_txt=True):
    """
    发送邮件
    :param to:
    :param subject:
    :param body:
    :param is_txt:
    :return:
    """
    app = current_app._get_current_object()
    msg = Message(subject=app.config.get('MAIL_SUBJECT_PREFIX') + subject, sender=app.config.get('MAIL_USERNAME'),
                  recipients=[to])
    if is_txt:
        msg.body = body
    else:
        msg.body = body
    thread = Thread(target=async_send_mail, args=[app, msg])
    thread.start()
    return thread
