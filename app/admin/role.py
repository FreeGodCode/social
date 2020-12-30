# -*- coding: utf-8  -*-
# @Author: ty
# @File name: role.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from flask_admin.form import Select2Widget
from wtforms import form, fields
from wtforms.validators import DataRequired


class RolesForm(form.Form):
    """角色管理表单类"""
    name = fields.StringField('角色名', validators=[DataRequired('角色名不能为空')])
    permissions = fields.SelectMultipleField('权限', widget=Select2Widget(multiple=True), validators=[DataRequired('权限不能为空')])
