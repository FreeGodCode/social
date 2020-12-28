# -*- coding: utf-8  -*-
# @Author: ty
# @File name: catalogs.py
# @IDE: PyCharm
# @Create time: 12/28/20 3:22 PM
from flask_admin.form import Select2Widget
from wtforms import form, fields


class CatalogsForm(form.Form):
    """栏目管理表单类"""
    name = fields.StringField('栏目名称')
    moderator_id = fields.SelectField('版主', widget=Select2Widget())
    sort = fields.IntegerField('排序', default=0)
    form_columns = ('name', 'sort')
