# -*- coding: utf-8  -*-
# @Author: ty
# @File name: catalogs.py 
# @IDE: PyCharm
# @Create time: 12/28/20 3:26 PM
from bson import ObjectId

from app import mongo
from app.models.catalogs import CatalogsForm
from app.views.base import BaseModelView, fill_form_choices


class CatalogsModelView(BaseModelView):
    """栏目管理视图类"""
    column_list = ('name', 'sort')
    column_labels = {'name': '栏目名称', 'sort': '排序'}
    column_sortable_list = 'name'
    column_default_sort = ('name', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = CatalogsForm
    permission_name = 'catalogs'

    def create_form(self, obj=None):
        """

        :param obj:
        :return:
        """
        real_form = super(CatalogsModelView, self).create_form(obj)
        fill_form_choices(real_form.moderator_id, 'users', 'username')
        return real_form

    def edit_form(self, obj=None):
        """

        :param obj:
        :return:
        """
        real_form = super(CatalogsModelView, self).edit_form(obj)
        fill_form_choices(real_form.moderator_id, 'users', 'username')
        return real_form

    def on_model_change(self, form, model, is_created):
        """

        :param form:
        :param model:
        :param is_created:
        :return:
        """
        model['moderator_id'] = ObjectId(model['moderator_id'])
        return model

    def after_model_delete(self, model):
        """

        :param model:
        :return:
        """
        catalog_id = ObjectId(model['_id'])
        post_ids = [post['_id'] for post in mongo.db.posts.find({'catalog_id': catalog_id}, {'_id': 1})]
        mongo.db.users.update_many({}, {'$pull': {'collections': {'$in': post_ids}}})
        mongo.db.posts.delete_many({'catalog_id': catalog_id})
