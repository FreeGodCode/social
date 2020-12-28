# -*- coding: utf-8  -*-
# @Author: ty
# @File name: footer.py 
# @IDE: PyCharm
# @Create time: 12/28/20 3:10 PM
from app.models.footer import FooterLinksForm
from app.views.base import BaseModelView


class FooterLinksModelView(BaseModelView):
    """底部链接管理视图类"""
    column_list = ('name', 'url', 'sort')
    column_labels = {'name':'名称', 'url': '链接', 'sort': '排序'}
    column_sortable_list = 'name'
    column_default_sort = ('name', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = FooterLinksForm
    permission_name = 'footer_links'

