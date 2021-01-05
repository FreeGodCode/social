# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py.py 
# @IDE: PyCharm
# @Create time: 12/27/20 9:41 PM
from flask import Flask

from app.views import config_blueprint
from app.config import config
from app.extensions import init_extensions
from app.func import init_func
from app.install_init import install_init
from app.utils import db_utils


# 结构会出现循环引用,使用懒加载的方式处理
def create_app(config_name):
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config['SECRET_KEY'] = 'TYCARRY'
    app.config.from_object(config[config_name])
    init_extensions(app)
    init_func(app)
    config_blueprint(app)
    with app.app_context():
        app.config['MAIL_SUBJECT_PREFIX'] = db_utils.get_option('mail_prefix') or app.config['MAIL_SUBJECT_PREFIX']
        install_init()
    return app
