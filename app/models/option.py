# -*- coding: utf-8  -*-
# @Author: ty
# @File name: option.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from app.admin.option import OptionsForm
from app.models.base import BaseModelView


class OptionsModelView(BaseModelView):
    """系统管理视图类"""
    column_list = ('name', 'code', 'value')
    column_labels = dict(name='名称', code='代码', value='值')
    column_sortable_list = 'name'
    column_default_sort = ('name', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = OptionsForm
    permission_name = 'options'
