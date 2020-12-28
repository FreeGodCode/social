# -*- coding: utf-8  -*-
# @Author: ty
# @File name: db_utils.py
# @IDE: PyCharm
# @Create time: 12/27/20 11:33 PM
from bson import ObjectId

from app import mongo


def _process_filter(filter_cond):
    """

    :param filter_cond:
    :return:
    """
    if filter_cond is None:
        return
    _id = filter_cond.get('_id')
    if _id and not isinstance(_id, ObjectId):
        filter_cond['_id'] = ObjectId(_id)


def get_option(name, default=None):
    """

    :param name:
    :param default:
    :return:
    """
    return mongo.db.options.find_one({'code': name}) or default


def get_page(collection_name, page_num=1, per_page=10, sort_by=None, filter_cond=None):
    """
    获取一页数据
    :param collection_name:  查询数据集
    :param page_num:  页码数
    :param per_page:  每页显示条数
    :param sort_by:  排序方式
    :param filter_cond:
    :return:
    """
    _process_filter(filter_cond)
    if per_page <= 0:
        per_page = 10
    total = mongo.db[collection_name].count(filter_cond)
    # 跳过条目数
    offset = (page_num - 1) * per_page
    result = []
    has_more = total > page_num * per_page
    if total - offset > 0:
        result = mongo.db[collection_name].find(filter_cond, limit=per_page)
        if sort_by:
            result = result.sort(sort_by[0], sort_by[1])

        if offset >= 0:
            result.skip(offset)
    total_page = int(total / per_page)
    if total % per_page > 0:
        total_page = total_page + 1
    page = Page(page_num, per_page, sort_by, filter_cond, result, has_more, total_page, total)
    return page


def get_list(collection_name, sort_by=None, filter_cond=None, size=None):
    """
    获取数据集列表
    :param collection_name: 数据集名称
    :param sort_by:  排序方式
    :param filter_cond:  过滤条件
    :param size:  查询条数
    :return:  返回查询结果集
    """
    _process_filter(filter_cond)
    result = mongo.db[collection_name].find(filter_cond)
    if sort_by:
        result = result.sort(sort_by[0], sort_by[1])
    if size:
        result = result.limit(size)
    result = list(result)
    return result


def find_one(collection_name, filter_cond=None):
    """
    查询一条数据
    :param collection_name: 数据集名称
    :param filter_cond:  过滤条件
    :return:
    """
    _process_filter(filter_cond)
    return mongo.db[collection_name].find_one(filter_cond)
