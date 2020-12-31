# -*- coding: utf-8  -*-
# @Author: ty
# @File name: extensions.py 
# @IDE: PyCharm
# @Create time: 12/30/20 11:31 PM
import functools

from bson import ObjectId
from flask_admin import Admin
from flask_cache import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_oauthlib.client import OAuth
from flask_pymongo import PyMongo
from flask_uploads import UploadSet, All, configure_uploads
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import Schema, ID, TEXT, DATETIME

from app.admin.admin_view import UsersModelView, RolesModelView, CatalogsModelView, PostsModelView, \
    PassagewaysModelView, FriendLinksModelView, PagesModelView, FooterLinksModelView, AdsModelView, OptionsModelView
from app.models.models import User

mail = Mail()
# 初始化后台管理admin
admin = Admin(name='social backend manage')

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'user.login'

# 图片上传
upload_img = UploadSet(extensions=All)

# Cache
cache = Cache()

# OAuth
oauth = OAuth()
# oauth_weibo = oauth.remote_app('weibo', )

from plugins.whoosh import WhooshSearcher

whoosh_searcher = WhooshSearcher()

use_cache = False


@login_manager.user_loader
def load_user(user_id):
    """用户登录"""
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    return User(user)


def init_extensions(app):
    """
    初始化插件
    :param app:
    :return:
    """
    global use_cache
    whoosh_searcher.init_app(app)
    configure_uploads(app, upload_img)
    mail.init_app(app)
    admin.init_app(app)
    mongo.init_app(app, 'MONGO')
    oauth.init_app(app)
    login_manager.init_app(app)
    # use_cache = app.config.get('USE_CHCHE', False)
    # if use_cache:
    #     cache.init_app(app)

    with app.app_context():
        # 添加flask-admin视图
        admin.add_view(UsersModelView(mongo.db['users'], '用户管理'))
        admin.add_view(RolesModelView(mongo.db['roles'], '角色管理'))
        admin.add_view(CatalogsModelView(mongo.db['catalogs'], '栏目管理', category='内容管理'))
        admin.add_view(PostsModelView(mongo.db['posts'], '帖子管理', category='内容管理'))
        admin.add_view(PassagewaysModelView(mongo.db['passageways'], '温馨通道', category='推广管理'))
        admin.add_view(FriendLinksModelView(mongo.db['friend_links'], '友链管理', category='推广管理'))
        admin.add_view(PagesModelView(mongo.db['pages'], '页面管理', category='推广管理'))
        admin.add_view(FooterLinksModelView(mongo.db['footer_links'], '底部链接', category='推广管理'))
        admin.add_view(AdsModelView(mongo.db['ads'], '广告管理', category='推广管理'))
        admin.add_view(OptionsModelView(mongo.db['options'], '系统管理'))

        # 初始化whoosh索引
        chinese_analyzer = ChineseAnalyzer()
        post_schema = Schema(
            obj_id=ID(unique=True, sortable=True),
            title=TEXT(sortable=True, analyzer=chinese_analyzer),
            content=TEXT(sortable=True, analyzer=chinese_analyzer),
            create_at=DATETIME(sortable=True),
            catalog_id=ID(sortable=True),
            user_id=ID(sortable=True)
        )
        whoosh_searcher.add_index('posts', post_schema)


def clear_cache(func):
    """
    清理缓存
    :param f:
    :return:
    """
    global use_cache

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if use_cache:
            cache.clear()
        return func(*args, **kwargs)

    return decorator
