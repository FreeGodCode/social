# -*- coding: utf-8  -*-
# @Author: ty
# @File name: admin_utils.py 
# @IDE: PyCharm
# @Create time: 12/31/20 9:42 PM
from app.admin.admin_config import admin_permissions
from app.extensions import mongo


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