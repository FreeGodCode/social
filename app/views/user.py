# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py 
# @IDE: PyCharm
# @Create time: 12/28/20 4:01 PM
from bson import ObjectId

from app.models.user import UserForm
from app.views.base import BaseModelView, fill_form_choices


class UsersModelView(BaseModelView):
    """用户管理视图类"""
    column_list = ('username', 'email', 'is_active', 'is_disabled', 'is_admin', 'vip', 'avatar', 'coin', 'description', 'city', 'auth_msg')
    column_labels = {'username': '用户昵称', 'email': '邮箱', 'is_active': '激活状态', 'vip': 'vip等级', 'is_disabled': '禁用', 'is_admin': '超级用户', 'avatar': '头像', 'coin': '金币', 'description': '描述', 'city': '城市', 'auth_msg': '认证信息'}
    column_sortable_list = 'username'
    column_default_sort = ('username', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = UserForm
    permission_name = 'users'

    def create_form(self, obj=None):
        real_form = super(UsersModelView, self).create_form(obj)
        fill_form_choices(real_form.role_ids, 'roles', 'username')
        return real_form

    def edit_form(self, obj=None):
        real_form = super(UsersModelView, self).edit_form(obj)
        fill_form_choices(real_form.role_ids, 'roles', 'username')
        return real_form

    # def delete_form(self):
    #     pass

    # def delete_model(self, model):
    #     pass

    # def delete_view(self):
    #     pass

    def on_model_change(self, form, model, is_created):
        model['role_ids'] = [ObjectId(role_id) for role_id in model['role_ids']]
        return model

    # def on_model_delete(self, model):
    #     pass

    # def on_form_prefill(self, form, id):
    #     pass