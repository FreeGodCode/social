# -*- coding: utf-8  -*-
# @Author: ty
# @File name: oauth_view.py 
# @IDE: PyCharm
# @Create time: 12/28/20 11:16 PM
from flask import Blueprint, url_for, redirect, session, request

from app import oauth

oauth_view = Blueprint('oauth', __name__, url_prefix='', static_folder='../../static',
                       template_folder='../../templates')

oauth_weibo = oauth.remote_app('weibo', )


@oauth_view.route('/weibo/login')
def weibo_login():
    return oauth_weibo.authorize(callback=url_for('oauth.weibo_authorized', _external=True))


@oauth_view.route('/weibo/login/authorized')
def weibo_login_authorized():
    """

    :return:
    """
    resp = oauth_weibo.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s errors=%s' % (request.args['error_reason'], request.args['error_description'])
    session['oauth_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))
