# -*- coding: utf-8  -*-
# @Author: ty
# @File name: friend_links.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from app.admin.friend_links import FriendLinksForm
from app.models.base import BaseModelView


class FriendLinksModelView(BaseModelView):
    """友情链接管理视图类"""
    column_list = ('url', 'name', 'sort')
    column_labels = dict(name='网站名称', url='网站链接', sort='排序')
    column_sortable_list = 'name'
    column_default_sort = ('name', False)
    can_create = True
    can_delete = True
    can_edit = True
    form = FriendLinksForm
    permission_name = 'friend_links'

