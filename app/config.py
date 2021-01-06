# -*- coding: utf-8  -*-
# @Author: ty
# @File name: config.py 
# @IDE: PyCharm
# @Create time: 12/27/20 10:45 PM
import os


class Config():
    """全局配置"""
    # MAIL
    # SECRET_KEY = 'tycarry'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 456
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'thechosenone_ty@163.com'
    MAIL_SENDER = '2501160661@qq.com'
    MAIL_PASSWORD = ''
    MAIL_DEBUG = True
    MAIL_SUBJECT_PREFIX = 'TYCARRY'
    # MONGO
    MONGO_URI = 'mongodb://root:123456@127.0.0.1:27017/db_social?charset=utf8'
    # csrf
    WTF_CSRF_ENABLED = False
    # uploads dir path
    UPLOADED_IMG_DEST = os.path.join(os.getcwd(), '../uploads')
    UPLOADED_FILES_DEST = os.path.join(os.getcwd(), '../uploads')
    # whoosh
    WHOOSH_PATH = os.path.join(os.getcwd(), 'whoosh_indexes')
    # cache settings
    USE_CACHE = True
    CACHE_TYPE = 'redis'
    # redis config
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_POST = 6379
    CACHE_REDIS_PASSWORD = '123456'
    CACHE_REDIS_DB = '1'


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
