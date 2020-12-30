# -*- coding: utf-8  -*-
# @Author: ty
# @File name: ads.py 
# @IDE: PyCharm
# @Create time: 12/28/20 2:59 PM
from wtforms import form, fields


class AdsForm(form.Form):
    """广告管理表单类"""
    name = fields.StringField('名称')
    url = fields.StringField('链接')
    color = fields.StringField('颜色', default='#ffffff')
    sort = fields.IntegerField('排序', default=0)
    form_column = ('name', 'url')
