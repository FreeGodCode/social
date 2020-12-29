# -*- coding: utf-8  -*-
# @Author: ty
# @File name: api_view.py 
# @IDE: PyCharm
# @Create time: 12/28/20 11:15 PM
from datetime import datetime
import random

from bson import ObjectId
from bson.json_util import dumps
from flask import Blueprint, request, jsonify, abort, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_uploads import UploadNotAllowed

import code_msg
import models
from app import mongo, upload_img, whoosh_searcher, clear_cache
from utils import db_utils

api = Blueprint('api', __name__, url_prefix='', template_folder='../../templates')


def add_message(user, content):
    """
    添加消息
    :param user:
    :param content:
    :return:
    """
    if user and user['_id'] != current_user.user['_id']:
        message = {
            'user_id': user['_id'],
            'content': content,
            'create_time': datetime.utcnow()
        }
        mongo.db.message.insert_one(message)
        mongo.db.users.update({'_id': user['_id']}, {'$inc': {'unread': 1}})


@api.route('/upload/<string:name>')
@api.route('/upload', methods=['POST'])
def upload(name=None):
    """
    文件上传
    :param name:
    :return:
    """
    if request.method == 'POST':
        # 用户未验证
        if not current_user.is_authenticated:
            return jsonify(code_msg.USER_NOT_LOGIN)
        file = request.files['file']
        # 没有上传文件
        if not file:
            return jsonify(code_msg.FILE_EMPTY)
        try:
            filename = upload_img.save(file)
        except UploadNotAllowed:
            return jsonify(code_msg.UPLOAD_NOT_ALLOWED)
        file_url = '/api/upload/' + filename
        result = models.Response(data={'url': file_url}).put('code', 0)
        return jsonify(result)
    if not name:
        abort(404)
    return redirect(upload_img.url(name))


@api.route('/adopt/<ObjectId:comment_id>', methods=["POST"])
@login_required
def post_adopt(comment_id):
    """
    帖子被采纳
    :param comment_id:
    :return:
    """
    if not comment_id:
        abort(404)
    # 评论
    comment = mongo.db.comments.find_one_or_404({"_id": comment_id})
    # 帖子
    post = mongo.db.posts.find_one_or_404({'_id': comment['post_id']})
    if post['user_id'] != current_user.user['_id']:
        return jsonify(code_msg.USER_NOT_HAD_PERMISSION)
    # 帖子有被采纳的回答
    if post.get('accepted', False):
        return jsonify(code_msg.HAD_ACCEPTED_ANSWER)
    mongo.db.comments.update_one({'_id': comment_id}, {'$set': {'is_adopted': True}})

    post['accepted'] = True
    mongo.db.posts.save(post)

    # 如果悬赏金币不为0,将金币加给回帖的人
    reward = post.get('reward', 0)
    user = mongo.db.users.find_one({'_id': comment['user_id']})
    if reward > 0 and user:
        mongo.db.users.update_one({'_id': comment['user_id']}, {'$inc': {'coin': reward}})
    # 没有悬赏金币, 给回帖人添加一条通知消息
    if user:
        add_message(user, render_template('user_message/adopt_message_html', post=post, comment=comment))
    return jsonify(models.Response.ok())


@api.route('/reply/zan/<ObjectId:comment_id>', methods=['POST'])
@login_required
def reply_zan(comment_id):
    """
    获赞
    :param comment_id:
    :return:
    """
    ok = request.values.get('ok')
    user_id = current_user.user['_id']
    resp = mongo.db.comments.find_one({'_id': comment_id, 'zan': {'$elemMatch': {'$eq': user_id}}})
    # 默认取消点赞
    action = '$pull'
    count = -1
    if ok == 'false' and not resp:
        # 点赞
        action = '$push'
        count = 1

    mongo.db.comments.update_one({'_id': comment_id}, {action: {'zan': user_id}, '$inc': {'zan_count': count}})
    return jsonify(models.Response().ok())


@api.route('/reply', methods=['POST'])
@login_required
def post_reply():
    """
    回帖
    :return:
    """
    post_id = request.values.get('id')
    if not post_id:
        abort(404)
    post_id = ObjectId(post_id)
    post = mongo.db.posts.find_one_or_404({'_id': post_id})
    user = current_user.user
    content = request.values.get('content')
    if not user.get('is_active', False) or user.get('is_disabled', False):
        return jsonify(code_msg.USER_NOT_ACTIVE_OR_DISABLED)
    if not content:
        return jsonify(code_msg.POST_CONTENT_EMPTY)

    comment = {
        'content': content,
        'post_id': post_id,
        'user_id': user['_id'],
        'create_time': datetime.utcnow(),
    }
    # 保存评论
    mongo.db.comments.save(comment)
    # 增加用户回贴和帖子回复数
    mongo.db.users.update_one({'_id': user['_id']}, {'$inc': {'reply_count': 1}})
    mongo.db.posts.update({'_id': post_id}, {'$inc': {'comment_count': 1}})
    if post['user_id'] != current_user.user['_id']:
        # 给发帖人新增一条通知消息
        user = mongo.db.users.find_one({'_id': post['user_id']})
        add_message(user, render_template('user_message/reply_message.html', post=post, user=current_user.user,
                                          comment=comment))
    if content.startswith('@'):
        end = content.index(' ')
        username = content[1: end]
        if username != current_user.user['username']:
            user = mongo.db.users.find_one({'username': username})
            # 给被@的人新增一条通知消息
            add_message(user, render_template('user_message/reply_message.html', post=post, user=current_user.user,
                                              comment=comment))
    return jsonify(code_msg.COMMENT_SUCCESS)


@api.route('/reply/delete/<ObjectId:comment_id>', methods=['POST'])
@login_required
def reply_delete(comment_id):
    # 超级用户
    if not current_user.user['is_admin']:
        abort(403)
    comment = mongo.db.comments.find_one_or_404({'_id': comment_id})
    post_id = comment['post_id']
    # 更新计数
    update_action = {'$inc': {'comment_count': -1}}
    if comment['is_adopted']:
        # 如果删除的是采纳的评论,恢复其他评论状态为可采纳
        update_action['$set'] = {'accepted': False}
    # 更新帖子回帖数,是否更新用户回帖计数
    mongo.db.posts.update_one({'_id': post_id}, update_action)
    mongo.db.comments.delete_one({'_id': comment_id})
    return jsonify(code_msg.DELETE_SUCCESS)


@api.route('/reply/content/<ObjectId:comment_id>', methods=['GET', 'POST'])
@login_required
def get_reply_content(comment_id):
    """
    获取回复的评论
    :param comment_id:
    :return:
    """
    comment = mongo.db.comments.find_one_or_404({'_id': ObjectId(comment_id)})
    return jsonify(models.Response.ok(data=comment['content']))


@api.route('/reply/update/<ObjectId:comment_id>', methods=['POST'])
@login_required
def reply_update(comment_id):
    """
    更新回复
    :param comment_id:
    :return:
    """
    content = request.values.get('content')
    if not content:
        return jsonify(code_msg.POST_CONTENT_EMPTY)
    comment = mongo.db.comments.find_one_or_404({'_id': comment_id})
    if current_user.user['_id'] != comment['user_id']:
        abort(403)
    mongo.db.comments.update_one({'_id': comment_id}, {'#set': {'content': content}})
    return jsonify(models.Response.ok())


@api.route('/post/delete/<ObjectId:post_id>', methods=['POST'])
@login_required
@clear_cache
def post_delete(post_id):
    """
    删除帖子
    :param post_id:
    :return:
    """
    post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})
    if post['user_id'] != current_user.user['_id'] and not current_user.user['is_admin']:
        return jsonify(code_msg.USER_NOT_HAD_PERMISSION)
    mongo.db.posts.delete_one({'_id': post_id})
    mongo.db.users.update_many({}, {'$pull': {'collections': post_id}})

    # 删除检索索引
    whoosh_searcher.delete_document('post', 'obj_id', str(post_id))
    return jsonify(code_msg.DELETE_SUCCESS.put('action', url_for('index.index', catalog_id=post['catalog_id'])))


@api.route('/post/set/<ObjectId:post_id>/<string:field>/<int:value>', methods=['POST'])
@login_required
@clear_cache
def post_set(post_id, field, value):
    """
    帖子
    :param post_id:
    :param field:
    :param value:
    :return:
    """
    post = mongo.db.posts.find_one_or_404({"_id": post_id})
    catalog = mongo.db.catalogs.find_one_or_404({'_id': post['catalog_id']})
    if field != 'is_closed':
        if not current_user.user['is_admin'] and current_user.user['_id'] != catalog['moderator_id']:
            return jsonify(code_msg.USER_NOT_HAD_PERMISSION)
    elif current_user.user['_id'] != post['user_id'] and not current_user.user['is_admin'] and current_user.user[
        '_id'] != catalog['moderator_id']:
        return jsonify(code_msg.USER_NOT_HAD_PERMISSION)
    value = value == 1
    mongo.db.posts.update_one({'_id': post_id}, {'$set': {field: value}})
    return jsonify(models.Response.ok())


@api.route('/posts/<int:pn>', methods=["GET", "POST"])
@api.route('/posts', methods=["GET", 'POST'])
@login_required
def post_list(pn=1):
    """
    获取帖子列表
    :param pn:
    :return:
    """
    # post = mongo.db.posts.find({'user_id': current_user.user['_id']})
    page = db_utils.get_page('posts', page_num=pn, sort_by=('_id', -1), filter_cond={'user_id': current_user.user['_id']})
    data = models.Response.ok().put('rows', page.result).put('count', page.total)
    return dumps(data)


@api.route('/sign', methods=['POST'])
@login_required
def user_sign():
    """
    签到
    :return:
    """
    date = datetime.utcnow().strftime("%Y-%m-%d")
    user = current_user.user
    doc = {
        'user_id': user['_id'],
        'date': date,
    }
    sign_log = mongo.db['user_signs'].find_one(doc)
    # 已签到
    if sign_log:
        return jsonify(code_msg.REPEAT_SIGNED)
    # 随机奖励
    interval = db_utils.get_option('sign_interval', {'value': 1 - 100})['value'].split('-')
    coin = random.randint(int(interval[0]), int(interval[1]))
    doc['coin'] = coin
    # 插入签到记录
    mongo.db['user_signs'].insert_one[doc]
    # 增加金币
    mongo.db.users.update({'_id': user['_id']}, {'$inc': {'coin': coin}})
    return jsonify(models.Response.ok(data={'signed': True, 'coin': coin}))


@api.route('/sign/status', methods=['POST'])
@login_required
def sign_status():
    """
    修改签到状态
    :return:
    """
    user = current_user.user
    sign_log = mongo.db['user_signs'].find_one({'user_id': user['_id'], 'date': datetime.utcnow().strftime('%Y-%m-%d')})
    signed = False
    coin = 0
    if sign_log:
        signed = True
        coin = sign_log.get('coin', 0)

    return jsonify(models.Response.ok(data={'signed': signed, 'coin': coin}))
