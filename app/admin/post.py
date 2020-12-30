# -*- coding: utf-8  -*-
# @Author: ty
# @File name: post.py 
# @IDE: PyCharm
# @Create time: 12/28/20 4:17 PM
from wtforms import form, fields
from wtforms.validators import DataRequired


class PostsForm(form.Form):
    """"""
    title = fields.StringField('标题', validators=[DataRequired('标题不能为空')])
    reward = fields.IntegerField('悬赏金币')
    comment_count = fields.IntegerField('评论数')
    is_top = fields.BooleanField('是否置顶')
    is_cream = fields.BooleanField('是否加精')
    is_closed = fields.BooleanField('是否已结')
    form_columns = ('title', 'reward', 'comment_count', 'is_top', 'is_cream', 'is_closed')
