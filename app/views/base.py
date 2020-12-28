# -*- coding: utf-8  -*-
# @Author: ty
# @File name: base.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from flask import redirect, url_for, request
from flask_admin.contrib.pymongo import ModelView
from flask_login import current_user


from app import mongo

admin_permissions = [
    ('roles', '角色管理'),
    ('users', '用户管理'),
    ('catalogs', '栏目管理'),
    ('passageways', '温馨通道'),
    ('friend_links', '友情链接管理'),
    ('pages', '页面管理'),
    ('footer_links', '底部链接'),
    ('ads', '广告管理'),
    ('options', '系统管理'),
]


class BaseModelView(ModelView):
    """视图基类"""
    permission_name = ''

    def is_accessible(self):
        # return True
        return current_user.is_authenticated and current_user.user[
            'is_admin'] or self.permission_name in get_user_permissions(current_user.user)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user.login', next=request.url))


def fill_form_choices(form_field, collection_name, db_field_name):
    """

    :param form_field:
    :param collection_name:
    :param db_field_name:
    :return:
    """
    form_field.choices = [(str(item['_id']), item[db_field_name]) for item in mongo.db[collection_name].find()]


def get_user_permissions(user):
    """
    根据用户名,获取用户权限
    :param user:
    :return:
    """
    if user['is_admin']:
        return set([permission[0] for permission in admin_permissions])
    if 'role_ids' not in user:
        return set()
    roles = mongo.db.roles.find({'_id': user['role_ids']})
    permissions = []
    for role in roles:
        permissions += role['permissions']
    return set(permissions)
