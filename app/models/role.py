# -*- coding: utf-8  -*-
# @Author: ty
# @File name: role.py
# @IDE: PyCharm
# @Create time: 12/28/20 10:43 AM
from flask_login import current_user

from app.admin.role import RolesForm
from app.models.base import BaseModelView, get_user_permissions, admin_permissions


class RolesModelView(BaseModelView):
    """角色管理视图类"""
    column_list = ('name',)
    column_labels = dict(name='角色名')
    column_sortable_list = 'name'
    column_default_sort = ('name', False)
    column_filters = 'name'
    # column_choices =
    # column_descriptions =
    # column_details_list =
    # column_details_exclude_list =
    # column_display_pk =
    # column_display_actions =
    # column_editable_list =
    # column_exclude_list =
    # column_export_exclude_list =
    # column_extra_row_actions =
    # column_export_list =
    # column_formatters =
    # column_formatters_detail =
    # column_formatters_export =
    # column_searchable_list =
    # column_type_formatters =
    # column_type_formatters_detail =
    # column_type_formatters_export =

    can_create = True
    can_delete = True
    can_edit = True
    # can_export = ''
    # can_set_page_size = ''
    # can_view_details = ''

    form = RolesForm
    permission_name = 'roles'

    def create_form(self, obj=None):
        """

        :param obj:
        :return:
        """
        real_form = super(RolesModelVIew, self).create_form(obj)
        user_permissions = get_user_permissions(current_user.user)
        real_form.permissions.choices = filter(lambda permission: permission[0] in user_permissions, admin_permissions)
        return real_form

    def edit_form(self, obj=None):
        """

        :param obj:
        :return:
        """
        real_form = super(RolesModelVIew, self).edit_form(obj)
        user_permissions = get_user_permissions(current_user.user)
        real_form.permissions.choices = filter(lambda permission: permission[0] in user_permissions, admin_permissions)
        return real_form
