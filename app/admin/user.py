# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from flask_admin.form import Select2Widget
from wtforms import form, fields
from wtforms.validators import DataRequired, Email


class UserForm(form.Form):
    """用户管理表单类"""
    username = fields.StringField('昵称', validators=[DataRequired('昵称不能为空')])
    email = fields.StringField('用户邮箱', validators=[DataRequired('邮箱不能为空'), Email('邮箱格式不正确')])
    is_active = fields.BooleanField('激活状态')
    is_disabled = fields.BooleanField('禁用')
    is_admin = fields.BooleanField('超级用户')
    vip = fields.IntegerField('vip等级')
    avatar = fields.StringField('头像')
    coin = fields.IntegerField('金币')
    description = fields.TextAreaField('描述')
    city = fields.StringField('城市')
    auth_msg = fields.StringField('认证信息')
    role_ids = fields.SelectMultipleField('角色', widget=Select2Widget(multiple=True))
    form_columns = ('username', 'email', 'is_active', 'is_admin', 'avatar', 'coin', 'description', 'city')
