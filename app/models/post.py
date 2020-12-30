# -*- coding: utf-8  -*-
# @Author: ty
# @File name: post.py 
# @IDE: PyCharm
# @Create time: 12/28/20 4:23 PM
from bson import ObjectId

from app import mongo
from app.admin.post import PostsForm
from app.models.base import BaseModelView


class PostsModelView(BaseModelView):
    """"""
    column_list = ('title', 'comment_count', 'is_top', 'is_cream', 'is_closed', 'create_time', 'modify_time', 'reward')
    column_labels = {'title': '标题', 'comment_count': '评论数', 'is_top': '是否置顶', 'is_cream': '是否加精', 'is_closed': '是否已结', 'created_time': '创建时间', 'modify_time': '最后编辑时间', 'reward': '悬赏金币值', 'view_count': '查看数'}
    column_sortable_list = 'title'
    column_default_sort = ('title', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = PostsForm
    permission_name = 'posts'

    def after_model_change(self, form, model, is_created):
        pass

    def after_model_delete(self, model):
        post_id = ObjectId(model['_id'])
        mongo.db.users.update_many({}, {'$pull': {'collections': post_id}})
