# -*- coding: utf-8  -*-
# @Author: ty
# @File name: ads.py 
# @IDE: PyCharm
# @Create time: 12/28/20 3:04 PM
from app.models.ads import AdsForm
from app.views.base import BaseModelView


class AdsModelView(BaseModelView):
    """广告管理视图类"""
    column_list = ('name', 'url', 'color', 'sort')
    column_labels = dict(name='名称', url='链接', color='颜色', sort='排序')
    column_sortable_list = 'name'
    column_default_sort = ('name', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = AdsForm
    permission_name = 'ads'
