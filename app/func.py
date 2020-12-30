# -*- coding: utf-8  -*-
# @Author: ty
# @File name: func.py 
# @IDE: PyCharm
# @Create time: 12/30/20 11:58 PM
from datetime import timedelta, datetime

from utils.db_utils import get_option, get_page, get_list, find_one


def date_calculate(dt, num, is_add=True):
    """
    计算时间
    :param d1:
    :param num:
    :param is_add:
    :return:
    """
    delta = timedelta(num)
    if is_add:
        return dt + delta
    else:
        return dt - delta


def utc2local(utc_str):
    """
    utc时间转换为本地时间
    :param utc_str:
    :return:
    """
    now_stamp = datetime.now().timestamp()
    local_time = datetime.fromtimestamp(now_stamp)
    utc_time = datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_str = utc_str + offset
    return local_str


def mongo_date_str(date):
    """
    保存到数据库的时间戳
    :param date:
    :return:
    """
    if not date:
        return ''
    return utc2local(date).strftime('%Y-%m-%d %H:%M:%S')


def init_func(app):
    """
    初始化函数
    :param app:
    :return:
    """
    app.add_template_global(get_option, 'get_option')
    app.add_template_global(get_page, 'get_page')
    app.add_template_global(get_list, 'get_list')
    app.add_template_global(datetime.now, 'now')
    app.add_template_global(date_calculate, 'date_calculate')
    app.add_template_global(find_one, 'find_one')
    app.add_template_global(mongo_date_str, 'mongo_date_str')