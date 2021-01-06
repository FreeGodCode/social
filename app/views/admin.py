# -*- coding: utf-8  -*-
# @Author: ty
# @File name: admin.py 
# @IDE: PyCharm
# @Create time: 1/6/21 3:27 PM
from bson import ObjectId
from flask import url_for, redirect, request
from flask_admin.contrib.pymongo import ModelView
from flask_admin.form import Select2Widget
from flask_login import current_user
from wtforms import form, fields
from wtforms.validators import DataRequired, Email

from app.admin.admin_config import admin_permissions
from app.admin.admin_utils import get_user_permissions, fill_form_choices
from app.extensions import mongo


class BaseModelView(ModelView):
    """视图基类"""
    permission_name = ''

    def is_accessible(self):
        # return True
        return current_user.is_authenticated and current_user.user[
            'is_admin'] or self.permission_name in get_user_permissions(current_user.user)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('user.login', next=request.url))


class UserForm(form.Form):
    """用户管理表单类"""
    username = fields.StringField('昵称', validators=[DataRequired('昵称不能为空')])
    email = fields.StringField('用户邮箱', validators=[DataRequired('邮箱不能为空'), Email('邮箱格式不正确')])
    is_active = fields.BooleanField('激活状态')
    is_disabled = fields.BooleanField('禁用')
    is_admin = fields.BooleanField('超级用户')
    vip = fields.IntegerField('vip等级')
    avatar = fields.StringField('头像')
    coin = fields.IntegerField('金币')
    description = fields.TextAreaField('描述')
    city = fields.StringField('城市')
    auth_msg = fields.StringField('认证信息')
    role_ids = fields.SelectMultipleField('角色', widget=Select2Widget(multiple=True))
    form_columns = ('username', 'email', 'is_active', 'is_admin', 'avatar', 'coin', 'description', 'city')


class UsersModelView(BaseModelView):
    """用户管理视图类"""
    column_list = (
        'username', 'email', 'is_active', 'is_disabled', 'is_admin', 'vip', 'avatar', 'coin', 'description', 'city',
        'auth_msg')
    column_labels = {'username': '用户昵称', 'email': '邮箱', 'is_active': '激活状态', 'vip': 'vip等级', 'is_disabled': '禁用',
                     'is_admin': '超级用户', 'avatar': '头像', 'coin': '金币', 'description': '描述', 'city': '城市',
                     'auth_msg': '认证信息'}
    column_sortable_list = 'username'
    column_default_sort = ('username', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = UserForm
    permission_name = 'users'

    def create_form(self, obj=None):
        real_form = super(UsersModelView, self).create_form(obj)
        fill_form_choices(real_form.role_ids, 'roles', 'username')
        return real_form

    def edit_form(self, obj=None):
        real_form = super(UsersModelView, self).edit_form(obj)
        fill_form_choices(real_form.role_ids, 'roles', 'username')
        return real_form

    # def delete_form(self):
    #     pass

    # def delete_model(self, model):
    #     pass

    # def delete_view(self):
    #     pass

    def on_model_change(self, form, model, is_created):
        model['role_ids'] = [ObjectId(role_id) for role_id in model['role_ids']]
        return model

    # def on_model_delete(self, model):
    #     pass

    # def on_form_prefill(self, form, id):
    #     pass


class RolesForm(form.Form):
    """角色管理表单类"""
    name = fields.StringField('角色名', validators=[DataRequired('角色名不能为空')])
    permissions = fields.SelectMultipleField('权限', widget=Select2Widget(multiple=True),
                                             validators=[DataRequired('权限不能为空')])


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
        real_form = super(RolesModelView, self).create_form(obj)
        user_permissions = get_user_permissions(current_user.user)
        real_form.permissions.choices = filter(lambda permission: permission[0] in user_permissions, admin_permissions)
        return real_form

    def edit_form(self, obj=None):
        """

        :param obj:
        :return:
        """
        real_form = super(RolesModelView, self).edit_form(obj)
        user_permissions = get_user_permissions(current_user.user)
        real_form.permissions.choices = filter(lambda permission: permission[0] in user_permissions, admin_permissions)
        return real_form


class PostsForm(form.Form):
    """"""
    title = fields.StringField('标题', validators=[DataRequired('标题不能为空')])
    reward = fields.IntegerField('悬赏金币')
    comment_count = fields.IntegerField('评论数')
    is_top = fields.BooleanField('是否置顶')
    is_cream = fields.BooleanField('是否加精')
    is_closed = fields.BooleanField('是否已结')
    form_columns = ('title', 'reward', 'comment_count', 'is_top', 'is_cream', 'is_closed')


class PostsModelView(BaseModelView):
    """"""
    column_list = ('title', 'comment_count', 'is_top', 'is_cream', 'is_closed', 'create_time', 'modify_time', 'reward')
    column_labels = {'title': '标题', 'comment_count': '评论数', 'is_top': '是否置顶', 'is_cream': '是否加精', 'is_closed': '是否已结',
                     'created_time': '创建时间', 'modify_time': '最后编辑时间', 'reward': '悬赏金币值', 'view_count': '查看数'}
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


class PassagewaysForm(form.Form):
    """温馨通道管理表单类"""
    name = fields.StringField('通道名称')
    url = fields.StringField('网站链接')
    sort = fields.IntegerField('排序', default=0)
    # 表单字段
    form_columns = ('name', 'url')


class PassagewaysModelView(BaseModelView):
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


class PagesForm(form.Form):
    """页面管理表单类"""
    name = fields.StringField('名称')
    url = fields.StringField('链接')
    sort = fields.IntegerField('排序', default=0)
    icon_code = fields.StringField('图标代码(http://www.layui.com/doc/element/icon.html)')
    form_column = ('name', 'url', 'icon_code')


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


class FriendLinksForm(form.Form):
    """友情链接表单类"""
    name = fields.StringField('网站名称')
    url = fields.StringField('网站链接')
    sort = fields.IntegerField('排序', default=0)
    # 表单字段
    form_columns = ('name', 'url')


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


class CatalogsForm(form.Form):
    """栏目管理表单类"""
    name = fields.StringField('栏目名称')
    moderator_id = fields.SelectField('版主', widget=Select2Widget())
    sort = fields.IntegerField('排序', default=0)
    form_columns = ('name', 'sort')


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


class AdsForm(form.Form):
    """广告管理表单类"""
    name = fields.StringField('名称')
    url = fields.StringField('链接')
    color = fields.StringField('颜色', default='#ffffff')
    sort = fields.IntegerField('排序', default=0)
    form_column = ('name', 'url')


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


class FooterLinksForm(form.Form):
    """底部链接表单类"""
    name = fields.StringField('名称')
    url = fields.StringField('链接')
    sort = fields.IntegerField('排序', default=0)
    form_column = ('name', 'url')


class FooterLinksModelView(BaseModelView):
    """底部链接管理视图类"""
    column_list = ('name', 'url', 'sort')
    column_labels = {'name': '名称', 'url': '链接', 'sort': '排序'}
    column_sortable_list = 'name'
    column_default_sort = ('name', False)

    can_create = True
    can_delete = True
    can_edit = True

    form = FooterLinksForm
    permission_name = 'footer_links'


class OptionsForm(form.Form):
    """系统管理表单类"""
    name = fields.StringField('名称')
    code = fields.StringField('代码', )
    value = fields.StringField('值')
    form_colums = ('name', 'code', 'value')


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
