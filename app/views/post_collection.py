# -*- coding: utf-8  -*-
# @Author: ty
# @File name: post_collection.py 
# @IDE: PyCharm
# @Create time: 12/28/20 11:16 PM
from bson.json_util import dumps
from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.models import models
from app.extensions import mongo

post_collection = Blueprint('collection', __name__, url_prefix='', static_folder='../../static',
                            template_folder='../../templates')


@post_collection.route('/find/<ObjectId:post_id>', methods=['POST'])
@post_collection.route('/find', methods=['POST'])
@login_required
def collection_find(post_id=None):
    """

    :param post_id:
    :return:
    """
    collections = current_user.user.get('collections', [])
    if not post_id:
        collections = mongo.db.posts.find({'_id': {'$in': collections}})
        data = models.Response.ok().put('rows', collections)
        return dumps(data)
    is_collected = False
    # 帖子被收藏
    if collections and post_id in collections:
        is_collected = True
    return jsonify(models.Response.ok(data={'collection': is_collected}))


@post_collection.route('/<string:action>/<ObjectId:post_id>', methods=['POST'])
@login_required
def collection(action, post_id):
    """
    收藏
    :param action:
    :param post_id:
    :return:
    """
    update_action = '$pull'
    if action == 'add':
        update_action = '$push'
    mongo.db.users.update_one({'_id': current_user.user['_id']}, {update_action: {'collections': post_id}})
    return jsonify(models.Response.ok())
