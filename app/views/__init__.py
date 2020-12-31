# -*- coding: utf-8  -*-
# @Author: ty
# @File name: __init__.py 
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
# 蓝图默认配置:(蓝图, 前缀)
from app.views.api_view import api_view
from app.views.exception_view import exception_view
from app.views.front import index
from app.views.post_collection import post_collection
from app.views.user_view import user

DEFAULT_BLUEPRINT = [
    (index, ''),
    (user, '/user'),
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
