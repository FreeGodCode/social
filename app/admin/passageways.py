# -*- coding: utf-8  -*-
# @Author: ty
# @File name: passageways.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from wtforms import form, fields


class PassagewaysForm(form.Form):
    """温馨通道管理表单类"""
    name = fields.StringField('通道名称')
    url = fields.StringField('网站链接')
    sort = fields.IntegerField('排序', default=0)
    # 表单字段
    form_columns = ('name', 'url')