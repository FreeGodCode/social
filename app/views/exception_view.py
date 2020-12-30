# -*- coding: utf-8  -*-
# @Author: ty
# @File name: exception_view.py 
# @IDE: PyCharm
# @Create time: 12/28/20 11:15 PM
from flask import Blueprint, jsonify

from app.models import GlobalApiException

exception_view = Blueprint('exception', __name__, url_prefix='', static_folder='../../static',
                           template_folder='../../templates')


@exception_view.app_errorhandler(GlobalApiException)
def api_exception(ex):
    return jsonify(ex.code_msg)
