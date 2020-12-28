# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py.py 
# @IDE: PyCharm
# @Create time: 12/27/20 9:41 PM
import functools
import os
from datetime import timedelta, datetime

from bson import ObjectId
from flask import Flask
from flask_cache import Cache
from flask_mail import Mail
from flask_admin import Admin
from flask_oauthlib.client import OAuth
from flask_pymongo import PyMongo
from flask_login import LoginManager

# 初始化邮件
from flask_uploads import UploadSet, configure_uploads, All
from jieba.analyse import ChineseAnalyzer
from werkzeug.security import generate_password_hash

from config import config
from utils import db_utils
from utils.db_utils import get_option, get_page, get_list, find_one

mail = Mail()
# 初始化后台管理admin
admin = Admin(name='social backend manage')
mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'user.login'

# 图片上传
upload_img = UploadSet(extensions=All)

# Cache
cache = Cache()

# OAuth
oauth = OAuth()
# oauth_weibo = oauth.remote_app('weibo', )

from plugins.whoosh import WhooshSearcher

whoosh_searcher = WhooshSearcher()

use_cache = False


@login_manager.user_loader
def load_user(user_id):
    """用户登录"""
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    return User(user)


def init_extensions(app):
    """
    初始化插件
    :param app:
    :return:
    """
    global use_cache
    whoosh_searcher.init_app(app)
    configure_uploads(app, upload_img)
    mail.init_app(app)
    admin.init_app(app)
    mongo.init_app(app, 'MONGO')
    oauth.init_app(app)
    login_manager.init_app(app)
    use_cache = app.config.get('USE_CHCHE', False)
    if use_cache:
        cache.init_app(app)

    with app.app_context():
        # 添加flask-admin视图
        admin.add_view(admin_view.UserModelView(mongo.db['user'], '用户管理'))

        # 初始化whoosh索引
        chinese_analyzer = ChineseAnalyzer()
        post_schema = Schema(

        )
        whoosh_searcher.add_index('posts', post_schema)


def date_calculate(dt, num, is_add=True):
    """
    计算时间
    :param d1:
    :param num:
    :param is_add:
    :return:
    """
    delta = timedelta(num)
    if is_add:
        return dt + delta
    else:
        return dt - delta


def utc2local(utc_str):
    """
    utc时间转换为本地时间
    :param utc_str:
    :return:
    """
    now_stamp = datetime.now().timestamp()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_str = utc_str + offset
    return local_str


def mongo_date_str(date):
    """
    保存到数据库的时间戳
    :param date:
    :return:
    """
    if not date:
        return ''
    return utc2local(date).strftime('%Y-%m-%d %H:%M:%S')


def init_func(app):
    """
    初始化函数
    :param app:
    :return:
    """
    app.add_template_global(get_option, 'get_option')
    app.add_template_global(get_page, 'get_page')
    app.add_template_global(get_list, 'get_list')
    app.add_template_global(datetime.now, 'now')
    app.add_template_global(date_calculate, 'date_calculate')
    app.add_template_global(find_one, 'find_one')
    app.add_template_global(mongo_date_str, 'mongo_date_str')


def clear_cache(func):
    """
    清理缓存
    :param f:
    :return:
    """
    global use_cache

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if use_cache:
            cache.clear()
        return func(*args, **kwargs)

    return decorator


# 蓝图默认配置:(蓝图, 前缀)
DEFAULT_BLUEPRINT = [
    (index, ''),
    (user_view, '/user'),
    (post_collection, '/collection'),
    (api_view, '/api'),
    (exception_view, '/error'),
]


def config_blueprint(app):
    """
    蓝图配置
    :param app:
    :return:
    """
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


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

def create_app(config_name):
    app = Flask(__name__, static_folder='../satatic', template_folder='../templates')
    app.config['SECRET_KEY'] = 'tycarry'
    app.config.from_object(config[config_name])
    init_extensions(app)
    init_func(app)
    config_blueprint(app)
    with app.app_context():
        app.config['MAIL_SUBJECT_PREFIX'] = db_utils.get_option('mail_prefix') or app.config['MAIL_SUBJECT_PREFIX']
        install_init()
    return app
