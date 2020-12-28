# -*- coding: utf-8  -*-
# @Author: ty
# @File name: footer.py 
# @IDE: PyCharm
# @Create time: 12/28/20 3:08 PM
from wtforms import form, fields


class FooterLinksForm(form.Form):
    """底部链接表单类"""
    name = fields.StringField('名称')
    url = fields.StringField('链接')
    sort = fields.IntegerField('排序', default=0)
    form_column = ('name', 'url')
