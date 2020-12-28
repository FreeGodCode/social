# -*- coding: utf-8  -*-
# @Author: ty
# @File name: friend_links.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from wtforms import form, fields


class FriendLinksForm(form.Form):
    """友情链接表单类"""
    name = fields.StringField('网站名称')
    url = fields.StringField('网站链接')
    sort = fields.IntegerField('排序', default=0)
    # 表单字段
    form_columns = ('name', 'url')