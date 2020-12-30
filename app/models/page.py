# -*- coding: utf-8  -*-
# @Author: ty
# @File name: page.py 
# @IDE: PyCharm
# @Create time: 12/28/20 3:16 PM
from app.admin.page import PagesForm
from app.models.base import BaseModelView


class PagesModelView(BaseModelView):
    """页面管理视图类"""
    column_list = ('name', 'url', 'icon_code', 'sort')
    column_labels = {'name': '名称', 'url': '链接', 'icon_code': '图标代码', 'sort': '排序'}
    column_sortable_list = 'name'
    column_default_sort = ('name', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = PagesForm
    permission_name = 'pages'
