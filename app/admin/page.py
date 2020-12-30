# -*- coding: utf-8  -*-
# @Author: ty
# @File name: page.py 
# @IDE: PyCharm
# @Create time: 12/28/20 3:16 PM
from wtforms import form, fields


class PagesForm(form.Form):
    """页面管理表单类"""
    name = fields.StringField('名称')
    url = fields.StringField('链接')
    sort = fields.IntegerField('排序', default=0)
    icon_code = fields.StringField('图标代码(http://www.layui.com/doc/element/icon.html)')
    form_column = ('name', 'url', 'icon_code')
