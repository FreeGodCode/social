# -*- coding: utf-8  -*-
# @Author: ty
# @File name: install_init.py 
# @IDE: PyCharm
# @Create time: 12/30/20 11:53 PM
import os
from datetime import datetime

from werkzeug.security import generate_password_hash

from extensions import mongo


def install_init():
    """

    :return:
    """
    lock_file = os.path.join(os.getcwd(), 'installed.lock')
    if os.path.exists(lock_file):
        return
    options = [
        {
            'name': '网站标题',
            'code': 'title',
            'value': 'tycarry'
        },
        {
            'name': '网站描述',
            'code': 'description',
            'value': 'tycarry'
        },
        {
            'name': '网站关键字',
            'code': 'key_words',
            'value': 'tycarry'
        },
        {
            'name': '网站LOGO',
            'code': 'LOGO',
            'value': 'tycarry'
        },
        {
            'name': '签到奖励区间(格式: 1-100)',
            'code': 'sign_interval',
            'value': '1-100'
        },
        {
            'name': '开启用户注册(0关闭, 1开启)',
            'code': 'open_user',
            'value': '1'
        },
        {
            'name': '管理员邮箱(申请好友链接用到)',
            'code': 'email',
            'value': '2501160661@qq.com'
        },
        {
            'name': '底部信息(支持html代码)',
            'code': 'footer',
            'value': 'tycarry'
        },
    ]
    result = mongo.db.options.insert_many(options)
    mongo.db.users.insert_one({
        'email': 'admin',
        'username': 'admin',
        'password': generate_password_hash('admin'),
        'is_admin': True,
        'authentication': '社区超级管理员',
        'vip': 5,
        'coin': 9999,
        'avatar': '/static/images/avatar/head.jpg',
        'is_activate': True,
        'created_time': datetime.utcnow(),
    })
    if len(result.inserted_ids) > 0:
        with open(lock_file, 'wb')as f:
            f.write('1')