# -*- coding: utf-8  -*-
# @Author: ty
# @File name: option.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from wtforms import form, fields


class OptionsForm(form.Form):
    """系统管理表单类"""
    name = fields.StringField('名称')
    code = fields.StringField('代码', )
    value = fields.StringField('值')
    form_colums = ('name', 'code', 'value')
