# -*- coding: utf-8  -*-
# @Author: ty
# @File name: forms.py 
# @IDE: PyCharm
# @Create time: 12/30/20 11:24 PM
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email

import code_msg


class RegisterForm(FlaskForm):
    """注册表单"""
    email = fields.StringField(validators=[DataRequired(code_msg.EMAIL_EMPTY.get_msg()), Email(
        code_msg.EMAIL_ERROR.get_msg())])
    username = fields.StringField(validators=[DataRequired(code_msg.USERNAME_EMPTY.get_msg())])
    verify_code = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    password = fields.PasswordField(validators=[Length(min=6, max=16, message=code_msg.PASSWORD_LENGTH_ERROR.get_msg())])
    re_password = fields.PasswordField(validators=[EqualTo('password', code_msg.PASSWORD_REPEAT_ERROR.get_msg())])


class LoginFrom(FlaskForm):
    """登录表单"""
    email = fields.StringField(validators=[DataRequired(code_msg.EMAIL_EMPTY.get_msg())])
    verify_code = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    password = fields.PasswordField(validators=[DataRequired(code_msg.PASSWORD_LENGTH_ERROR.get_msg())])


class PostsForm(FlaskForm):
    """"""
    id = fields.StringField()
    title = fields.StringField(validators=[DataRequired(code_msg.POST_TITLE_EMPTY.get_msg())])
    content = fields.StringField(validators=[DataRequired(code_msg.POST_CONTENT_EMPTY.get_msg())])
    catalog_id = fields.StringField(validators=[DataRequired(code_msg.POST_CATALOG_EMPTY.get_msg())])
    reward = fields.IntegerField(validators=[InputRequired(code_msg.POST_COIN_EMPTY.get_msg())])
    verify_code = fields.StringField(validators=[InputRequired(code_msg.POST_CODE_ERROR.get_msg())])


class ForgetPasswordForm(FlaskForm):
    """忘记密码"""
    email = fields.StringField(validators=[DataRequired(code_msg.EMAIL_EMPTY.get_msg())])
    code = fields.StringField(validators=[DataRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    verify_code = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    password = fields.PasswordField(
        validators=[Length(min=5, max=16, message=code_msg.PASSWORD_LENGTH_ERROR.get_msg())])
    re_password = fields.PasswordField(validators=[EqualTo('password', code_msg.PASSWORD_REPEAT_ERROR.get_msg())])


class SendForgetMailForm(FlaskForm):
    """重置密码邮件表单类"""
    email = fields.StringField(validators=[DataRequired(code_msg.EMAIL_EMPTY.get_msg())])
    verify_code = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])


class ChangePasswordForm(FlaskForm):
    """修改密码表单类"""
    now_password = fields.StringField(validators=[DataRequired(code_msg.NOW_PASSWORD_EMPTY.get_msg())])
    new_password = fields.PasswordField(
        validators=[Length(min=6, max=16, message=code_msg.PASSWORD_LENGTH_ERROR.get_msg())])
    re_password = fields.PasswordField(validators=[EqualTo('new_password', code_msg.PASSWORD_REPEAT_ERROR.get_msg())])