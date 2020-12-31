# -*- coding: utf-8  -*-
# @Author: ty
# @File name: models.py
# @IDE: PyCharm
# @Create time: 12/28/20 4:40 PM
from json import JSONEncoder

from werkzeug.security import check_password_hash


class Page():
    def __init__(self, page_num, per_page, sort_by=None, filter_cond=None, result=None, has_more=False, total_page=0,
                 total=0):
        """
        分页
        :param page_num:
        :param per_page:
        :param sort_by:
        :param filter_cond:
        :param result:
        :param has_more:
        :param total_page:
        :param total:
        """
        self.page_num = page_num
        self.per_page = per_page
        self.sort_by = sort_by
        self.result = result
        self.filter_cond = filter_cond
        self.has_more = has_more
        self.total_page = total_page
        self.total = total

    def __repr__(self):
        return JSONEncoder().encode(o=self.__dict__)


class Response(dict):

    @staticmethod
    def ok(msg=None, data=None):
        res = Response()
        res.put('status', 0)
        res.put('msg', msg)
        res.put('data', data)
        return res

    @staticmethod
    def fail(code=404, msg=None):
        res = Response()
        res.put('status', code)
        res.put('msg', msg)
        return res

    def put(self, key, value):
        self.__setitem__(key, value)
        return self

    def get_status(self):
        return self.get('status')

    def get_msg(self):
        return self.get('msg')


class BaseResult(Response):
    def __init__(self, code=0, msg='', data=None):
        self.put('status', code)
        self.put('msg', msg)
        self.put('data', data)


class User():
    user = None
    is_authenticated = True
    is_anonymous = False
    is_active = False

    def __init__(self, user):
        self.user = user
        self.is_active = user['is_active']

    def get_id(self):
        return str(self.user['_id'])

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


class GlobalApiException(Exception):

    def __init__(self, code_msg):
        self.code_msg = code_msg
