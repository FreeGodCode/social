# -*- coding: utf-8  -*-
# @Author: ty
# @File name: front.py 
# @IDE: PyCharm
# @Create time: 12/28/20 11:15 PM
from datetime import datetime

import pymongo
from bson import ObjectId
from flask import Blueprint, request, render_template, jsonify, url_for, session, abort, redirect
from flask_login import login_required, current_user
from whoosh import qparser, sorting

from app import models, code_msg
from app.extensions import cache, clear_cache, mongo, whoosh_searcher
from app.forms import PostsForm

from app.utils import db_utils, utils

index = Blueprint('index', __name__, url_prefix='', static_folder='../../static', template_folder='../../templates')


@index.route('/')
@index.route('/page/<int:pn>')
@index.route('/page/<int:pn>/size/<int:size>')
@index.route('/catalog/<ObjectId:catalog_id>')
@index.route('/catalog/<ObjectId:catalog_id>/page/<int:pn>')
@index.route('/catalog/<ObjectId:catalog_id>/page/<int:pn>/size/<int:size>')
@cache.cached(timeout=60, key_prefix=utils.generate_cache_key)
def index(pn=1, size=10, catalog_id=None):
    """

    :param pn:
    :param size:
    :param catalog_id:
    :return:
    """
    sort_key = request.values.get('sort_key', '_id')
    sort_by = (sort_key, pymongo.DESCENDING)
    post_type = request.values.get('type')
    filter_cond = {}
    if post_type == 'not_closed':
        filter_cond['is_closed'] = {'$ne': True}
    if post_type == 'is_closed':
        filter_cond['is_closed'] = True
    if post_type == 'is_cream':
        filter_cond['is_cream'] = True
    if catalog_id:
        filter_cond['catalog_id'] = catalog_id

    page = db_utils.get_page('posts', page_num=pn, filter_cond=filter_cond, per_page=size, sort_by=sort_by)
    return render_template('post_list.html', is_index=catalog_id is None, page=page, sort_key=sort_key,
                           catalog_id=catalog_id, post_type=post_type)


@index.route('/add', methods=['GET', 'POST'])
@index.route('/edit/<ObjectId:post_id>', methods=['GET', 'POST'])
@login_required
@clear_cache
def add(post_id=None):
    """

    :param post_id:
    :return:
    """
    posts_form = PostsForm()
    if posts_form.is_submitted():
        if not posts_form.validate():
            return jsonify(models.BaseResult(1, str(posts_form.errors)))
        utils.verify_code((posts_form.verify_code.data))
        user = current_user.user
        if not user.get('is_active', False) or user.get('is_disabled', False):
            return jsonify(code_msg.USER_NOT_ACTIVE_OR_DISABLED)

        user_coin = user.get('coin', 0)
        if posts_form.reward.data > user_coin:
            return jsonify(models.Response.ok('悬赏金币不能大于拥有的金币,当前帐号的金币为:' + str(user_coin)))
        posts = {
            'title': posts_form.title.data,
            'catalog_id': ObjectId(posts_form.catalog_id.data),
            'is_closed': False,
            'content': posts_form.content.data,
        }
        post_index = posts.copy()
        post_index['catalog_id'] = str(posts['catalog_id'])
        msg = '发帖成功'
        reward = posts_form.reward.data
        if post_id:
            posts['modify_time'] = datetime.now()
            mongo.db.posts.update_one({'_id': post_id}, {'$set': posts})
            msg = '修改成功!'
        else:
            posts['create_time'] = datetime.utcnow()
            posts['reward'] = reward
            posts['user_id'] = user['_id']
            # 扣除用户发帖悬赏
            if reward > 0:
                mongo.db.users.update_one({'_id': user['_id']}, {'$inc': {'coin': -reward}})
            mongo.db.posts.save(posts)
            post_id = posts['_id']
        # 更新索引文档
        update_index(mongo.db.posts.find_one_or_404({'_id': post_id}))
        return jsonify(models.Response.ok(msg).put('action', url_for('index.index')))
    else:
        verify_code = utils.generate_verify_code()
        session['verify_code'] = verify_code['answer']
        posts = None
        if post_id:
            posts = mongo.db.posts.find_one_or_404({'_id': post_id})
        title = "发帖" if post_id is None else "编辑帖子"
        return render_template('jie/add.html', page_name='jie', verify_code=verify_code['question'], form=posts_form,
                               is_add=post_id is None, post=posts, title=title)


def update_index(post):
    """

    :param post:
    :return:
    """
    _id = str(post['_id'])

    post_index = dict()
    post_index['catalog_id'] = str(post['catalog_id'])
    post_index['user_id'] = str(post['user_id'])
    post_index['create_time'] = post['create_time']
    post_index['content'] = post['content']
    post_index['title'] = post['title']
    whoosh_searcher.update_document('posts', {'obj_id': _id}, post_index)


@index.route('/post/<ObjectId:post_id>/')
@index.route('/post/<ObjectId:post_id>/page/<int:pn>')
def post_detail(post_id, pn=1):
    """

    :param post_id:
    :param pn:
    :return:
    """
    post = mongo.db.posts.find_one_or_404({"_id": post_id})
    if post:
        post['view_count'] = post.get('view_count', 0) + 1
        mongo.db.posts.save(post)
    post['user'] = db_utils.find_one('users', {'_id': post['user_id']}) or {}

    page = db_utils.get_page('comments', page_num=pn, per_page=10, filter_cond={'post_id': post_id},
                             sort_by=('is_adopted', -1))
    return render_template('jie/detail.html', post=post, title=post['title'], page_name='jie', comment_page=page,
                           catalog_id=post['catalog_id'])


@index.route('/jump')
def user_jump():
    """
    切换用户
    :return:
    """
    username = request.values.get('username')
    if not username:
        abort(404)
    user = mongo.db.users.find_one_or_404({'username': username})
    return redirect('/user/' + str(user['_id']))


@index.route('/comment/<ObjectId:comment_id>/', methods=['POST'])
def comment_jump(comment_id):
    """
    跳转评论
    :param comment_id:
    :return:
    """
    comment = mongo.db.comments.find_one_or_404({"_id": comment_id})
    post_id = comment['post_id']
    pn = 1
    # 评论未被采纳
    if not comment.get('is_adopted', False):
        comment_count = mongo.db.comments.count({"post_id": post_id, '_id': {'$lt': comment_id}})
        pn = comment_count / 10
        # 评论数为0或不是10的整数
        if pn == 0 or pn % 10 != 0:
            pn += 1
    return redirect(url_for('index.post_detail', post_id=post_id, pn=pn) + '#item-' + str(comment_id))


@index.route('/search')
@index.route('/search/page/<int:pn>/')
def post_search(pn=1, size=10):
    """

    :param pn:
    :param size:
    :return:
    """
    keyword = request.values.get('kw')
    if keyword is None:
        return render_template('search/list.html', title='搜索', message='搜索关键字不能为空')
    with whoosh_searcher.get_searcher('posts') as searcher:
        parser = qparser.MultifieldParser(['title', 'content'], whoosh_searcher.get_index('posts').schema)
        q = parser.parser(keyword)
        result = searcher.search_page(q, pagenum=pn, pagelen=size, sortedby=sorting.ScoreFacet())
        result_list = [x.fields() for x in result.results]
        page = models.Page(page_num=pn, per_page=size, result_list=result_list, has_more=result.pagecount > pn,
                           total_page=result.pagecount, total=result.total)
    return render_template('search/list.html', title=keyword + '搜索结果', page=page, kw=keyword)


@index.route('/refresh/indexes')
def refresh_indexes():
    name = request.values.get('name')
    whoosh_searcher.clear(name)
    writer = whoosh_searcher.get_writer(name)
    for item in mongo.db[name].find({}, ['_id', 'title', 'content', 'create_time', 'user_id', 'catalog_id']):
        item['obj_id'] = str(item['_id'])
        item['user_id'] = str(item['user_id'])
        item['catalog_id'] = str(item['catalog_id'])
        item.pop('_id')
        writer.add_document(**item)
    writer.commit()
    return ''
