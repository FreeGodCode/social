# -*- coding: utf-8  -*-
# @Author: ty
# @File name: passageways.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from app.models.passageways import PassagewaysForm
from app.views.base import BaseModelView


class PassawaysModelView(BaseModelView):
    """温馨通道管理视图类"""
    column_list = ('url', 'name', 'sort')
    column_labels = dict(name='通道名称', url='网站链接', sort='排序')
    column_sortable_list = 'name'
    column_default_sort = ('name', False)
    can_create = True
    can_delete = True
    can_edit = True
    form = PassagewaysForm
    permission_name = 'passageways'
