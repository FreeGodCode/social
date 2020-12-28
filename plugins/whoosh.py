# -*- coding: utf-8  -*-
# @Author: ty
# @File name: whoosh.py
# @IDE: PyCharm
# @Create time: 12/27/20 10:15 PM
import os

from whoosh import writing
from whoosh.index import exists_in, open_dir, create_in


class WhooshSearcher():
    """whooshSearcher搜索引擎"""

    def __init__(self, app=None):
        self.initialized = False
        self.whoosh_path = 'whoosh_indexes'
        self.indexes = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        """

        :param app:
        :return:
        """
        if 'whoosh_searcher' not in app.extensions:
            app.extensions['whoosh_searcher'] = self
        if app.config['WHOOSH_PATH'] is not None:
            self.whoosh_path = app.config['WHOOSH_PATH']
        if not os.path.exists(self.whoosh_path):
            os.mkdir(self.whoosh_path)
        self.initialized = True

    def add_index(self, index_name, schema):
        """

        :param index_name:
        :param schema:
        :return:
        """
        if not self.initialized:
            raise Exception('not initialized')
        if exists_in(self.whoosh_path, index_name):
            index = open_dir(self.whoosh_path, index_name)
        else:
            index = create_in(self.whoosh_path, schema, index_name)
        self.indexes[index_name] = index

    def get_index(self, index_name):
        if not exists_in(self.whoosh_path, index_name):
            raise Exception('this index is not exists')
        index = self.indexes[index_name]
        if index is None:
            index = open_dir(self.whoosh_path, index_name)
            self.indexes[index_name] = index
        return index

    def get_writer(self, index_name):
        """

        :param index_name:
        :return:
        """
        return self.get_index(index_name).writer()

    def get_searcher(self, index_name):
        """
        搜索
        :param index_name:
        :return:
        """
        return self.get_index(index_name).searcher()

    def add_document(self, index_name, doc):
        """
        增加文档
        :param index_name:
        :param doc:
        :return:
        """
        writer = self.get_writer(index_name)
        writer.add_document(**doc)
        writer.commit()

    def update_document(self, index_name, unique_field, doc):
        """
        更新文档
        :param index_name:
        :param unique_field:
        :param doc:
        :return:
        """
        writer = self.get_writer(index_name)
        writer.update_document(**unique_field, **doc)
        writer.commit()

    def delete_document(self, index_name, field_name, term_text):
        """

        :param index_name:
        :param field_name:
        :param term_text:
        :return:
        """
        writer = self.get_writer(index_name)
        writer.delete_by_term(fieldname=field_name, text=term_text)
        writer.commit()

    def clear(self, index_name):
        """

        :param index_name:
        :return:
        """
        writer = self.get_writer(index_name)
        writer.commit(mergetype=writing.CLEAR)
