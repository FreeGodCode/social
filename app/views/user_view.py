# -*- coding: utf-8  -*-
# @Author: ty
# @File name: user_view.py 
# @IDE: PyCharm
# @Create time: 12/28/20 11:16 PM
from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

import code_msg
import models
from app import mongo
from utils import db_utils, utils

user = Blueprint('user', __name__, url_prefix='', static_folder='../../static', template_folder='../../templates')

@user.route('/<ObjectId:user_id>', methods=['GET'])
def user_home(user_id):
    """
    用户首页
    :param user_id:
    :return:
    """
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    return render_template('user/home.html', user=user)

@user.route('/posts', methods=['GET'])
@login_required
def user_posts():
    return render_template('user/index.html', user_page='posts', page_name='user')

@user.route('/message', methods=['GET', 'POST'])
@user.route('/message/page/<int:pn>', methods=['GET, POST'])
@login_required
def user_message(pn=1):
    """
    用户信息
    :param pn:
    :return:
    """
    user = current_user.user
    if user.get('unread', 0) > 0:
        mongo.db.users.update({'_id': user['_id']}, {'$set': {'unread': 0}})
    message_page = db_utils.get_page('message', page_num=pn, filter_cond={'user_id': user['_id']}, sort_by=('_id', -1))
    return render_template('user/message.html', user_page='message', page_name='user', page=message_page)

@user.route('/message/remove', methods=['POST'])
@login_required
def remove_message():
    """
    删除消息
    :return:
    """
    user = current_user.user
    if request.values.get('all') == 'true':
        mongo.db.messages.delete_many({'user_id': user['_id']})
    elif request.values.get('id'):
        msg_id = ObjectId(request.values.get('id'))
        mongo.db.messages.delete_one({'_id': msg_id})
    return jsonify(models.BaseResult())

@user.route('/set', methods=['GET', 'POST'])
@login_required
def user_set():
    """
    设置用户基本信息
    :return:
    """
    if request.method == 'POST':
        include_keys = ['username', 'avatar', 'desc', 'city','sex']
        data = request.values
        update_data = {}
        for key in data.keys():
            if key in include_keys:
                update_data[key] = data.get(key)
        mongo.db.users.update({'_id': current_user.user['_id']}, {'$set': data})
        return jsonify(models.BaseResult())
    return render_template('user/set.html', user_page='set', page_name='user', title='基本设置')

@user.route('/repass', methods=['POST'])
@login_required
def user_repass():
    """
    用户更新密码
    :return:
    """
    if 'email' in request.values:
        # 忘记密码对象实例化
        pwd_form = models.ForgetPasswordForm()
        # 参数验证
        if not pwd_form.validate():
            return jsonify(models.Response.fail(code_msg.PARAM_ERROR.get_msg(), str(pwd_form.errors)))
        # 邮箱
        email = pwd_form.email.data
        # 验证码
        verify_code = pwd_form.verify_code.data
        # 邮件激活码
        code = pwd_form.code.data
        # 密码
        password = pwd_form.password.data
        # 验证码校验
        utils.verify_code(verify_code)
        # 检查,删除邮箱激活码
        active_code = mongo.db.active_codes.find_one_or_404({'_id': ObjectId(code)})
        mongo.db.active_codes.delete_one({'_id': ObjectId(code)})
        # 更新用户密码
        user = mongo.db.users.update({'_id': active_code['user_id'], 'email': email}, {'$set': {'password': generate_password_hash(password)}})
        if user['nModified'] == 0:
            return jsonify(code_msg.CHANGE_PASSWORD_FAIL.put('action', url_for('user.login')))

        return jsonify(code_msg.CHANGE_PASSWORD_SUCCESS.put('action', url_for('user.login')))
    # 用户未验证,重定向到登录页面
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    # 修改密码
    pwd_form = models.ChangePasswordForm()
    if not pwd_form.validate():
        return jsonify(models.Response.fail(code_msg.PARAM_ERROR.get_msg(), str(pwd_form.errors)))
    now_password = pwd_form.now_password.data
    new_password = pwd_form.new_password.data
    user = current_user.user
    if not models.User.validate_login(user['password'], now_password):
        raise models.GlobalApiException(code_msg.PASSWORD_ERROR)
    mongo.db.users.update({'_id': user['_id']}, {'$set': {'password': generate_password_hash(new_password)}})
    return jsonify(models.Response.ok())

@user.route('/forget', methods=['POST'])
@user.route('/forget/<ObjectId:code>', methods=['POST'])
def user_forget_password(code=None):
    """

    :param code:
    :return:
    """
    if request.method == 'POST':
        mail_form = models.SendForgetMailForm()
        if not mail_form.validate():
            return jsonify(models.Response.fail(code_msg.PARAM_ERROR.get_msg(), str(mail_form.errors)))

        email = mail_form.email.data
        verify_code = mail_form.verify_code.data

        utils.verify_code(verify_code)
        user = mongo.db.users.find_one({'email': email})
        if not user:
            return jsonify(code_msg.USER_NOT_EXIST)
        send_active_email(user['username'], user_id=user['_id'], email=email, is_forget=True)
        return jsonify(code_msg.SEND_RESET_PASSWORD_MAIL.put('action', url_for('user.login')))

    has_code = False
    user = None
    if code:
        active_code = mongo.db.active_codes.find_one({'_id': code})
        has_code = True
        if not active_code:
            return render_template('user/forget.html', page_name='user', has_code=True, code_invalid=True)
        user = mongo.db.users.find_one({'_id': active_code['user_id']})

    verify_code = utils.generate_verify_code()
    # session['verify_code'] = verify_code['answer']
    return render_template('user/forget.html', page_name='user', verify_code=verify_code['question'], code=code, has_code=has_code, user=user)

def send_active_email(username, user_id, email, is_forget=False):
    """
    发送激活邮件
    :param username:
    :param user_id:
    :param email:
    :param is_forget:
    :return:
    """
    active_code = mongo.db.active_codes.insert_one({'user_id': user_id})
    # 忘记密码
    if is_forget:
        # pass
        body = render_template('email/user_reset_pwd.html', url=url_for('user.user_forget_password', active_code=active_code.inserted_id, _external=True))
        utils.send_email(email, '重置密码', body=body)
    body = render_template('email/user_activate.html', username=username, url=url_for('user.user_active', active_code=active_code.inserted_id, _external=True))
    utils.send_email(email, '帐号激活', body = body)