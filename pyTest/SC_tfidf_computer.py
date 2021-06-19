import datetime
import math
from collections import OrderedDict, Counter

import copy
import numpy as np
import cupy as cp

import pymongo

from pyTest.loadModule_aspectj import LoadModule


# todo 修改数据库report_id


def cosine_sim(a, b):
    """
    计算余弦相似度
    :param a: vector a
    :param b: vector b
    :return: cosine_sim
    """
    a_array = cp.array(a)
    b_array = cp.array(b)
    return a_array.dot(b_array) / (cp.linalg.norm(a_array) * cp.linalg.norm(b_array))


class StructureHandler:
    def __init__(self):
        # 语料库
        self.corpus = []
        # 数据库连接
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.irbl
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_report()
        self.codes = self.loadModule.read_codes()
        # 加载source code 4 个属性
        self.methods = self.loadModule.read_methods()
        self.classes = self.loadModule.read_classes()
        self.comments = self.loadModule.read_comments()
        self.attributes = self.loadModule.read_attributes()
        # 加载report两个属性
        self.summaries = self.loadModule.read_summaries()
        self.descriptions = self.loadModule.read_descriptions()
        # 构建
        self.build_corpus()
        self.zero_vector = self.build_zero_vector()
        self.source_code_len_mean = self.build_source_codes_len_mean()
        # 计算tfidf
        self.build_tfidf()

    def build_corpus(self):
        """
        构建corpus，用所有的词
        :return:
        """
        doc_tokens = []
        for doc in self.methods.values():
            doc_tokens += [sorted(doc.split(' '))]
        for doc in self.classes.values():
            doc_tokens += [sorted(doc.split(' '))]
        for doc in self.attributes.values():
            doc_tokens += [sorted(doc.split(' '))]
        for doc in self.comments.values():
            doc_tokens += [sorted(doc.split(' '))]
        for doc in self.summaries.values():
            doc_tokens += [sorted(doc.split(' '))]
        for doc in self.descriptions.values():
            doc_tokens += [sorted(doc.split(' '))]
        all_doc_tokens = sum(doc_tokens, [])
        self.corpus = sorted(set(all_doc_tokens))

    def build_zero_vector(self):
        """
        从corpus创建全是0的one-hot向量
        :return: zero_vector
        """
        zero_vector = OrderedDict((token, 0) for token in self.corpus)
        return zero_vector

    # docs数据格式 docName:[content]
    def build_codes_tfidf(self, docs, name):
        """
        计算所有codes的tfidf
        :param name: 数据库collection名称
        :param docs: summaries, descriptions
        :return: {codeName: tfidf vector}
        """
        k1 = 1.0
        b = 0.3
        for docName in docs.keys():
            # one-hot 向量的复制
            vec = copy.copy(self.zero_vector)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                # 对所有部分都要计算idf
                for _docName in self.methods.keys():
                    if key in self.methods[_docName]:
                        docs_containing_key += 1
                for _docName in self.comments.keys():
                    if key in self.comments[_docName]:
                        docs_containing_key += 1
                for _docName in self.classes.keys():
                    if key in self.classes[_docName]:
                        docs_containing_key += 1
                for _docName in self.attributes.keys():
                    if key in self.attributes[_docName]:
                        docs_containing_key += 1
                for _docName in self.descriptions.keys():
                    if key in self.descriptions[_docName]:
                        docs_containing_key += 1
                for _docName in self.summaries.keys():
                    if key in self.summaries[_docName]:
                        docs_containing_key += 1
                # todo 修改 report tf公式
                # tf = value / len(self.corpus)
                tf = (k1 * value) / (value + k1 * (1 - b + b * (len(token_counts.items()) / self.source_code_len_mean)))
                # todo 修改 report idf公式
                if docs_containing_key:
                    idf = math.log((len(docs.keys()) + 1) / (docs_containing_key + 0.5))
                else:
                    idf = 0
                vec[key] = tf * idf
            # 存入mongodb
            self.db[name].insert_one({'report_id': docName, 'tf_idf': vec})

    # docs数据格式 docName:[content]
    def build_report_tfidf(self, docs, name):
        """
        计算所有report的tfidf
        :param name: 数据库collection名称
        :param docs: methods, classes, comments, attributes
        :return: {reportName: tfidf vector}
        """
        k3 = 1000
        for docName in docs.keys():
            # one-hot 向量的复制
            vec = copy.copy(self.zero_vector)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                for _docName in docs.keys():
                    if key in docs[_docName]:
                        docs_containing_key += 1
                # todo 修改code tf公式
                tf = (k3 * value) / (value + k3)
                # todo 修改code idf公式
                if docs_containing_key:
                    idf = math.log((len(docs.keys()) + 1) / (docs_containing_key + 0.5))
                else:
                    idf = 0
                vec[key] = tf * idf
            self.db[name].insert_one({'report_id': docName, 'tf_idf': vec})

    def build_source_codes_len_mean(self):
        """
        计算source code内容的平均长度
        :return: source_codes_len_mean
        """
        lens = []
        for codeName in self.codes:
            lens.append(len(self.codes[codeName]))
        return np.mean(lens)

    def build_tfidf(self):
        self.build_codes_tfidf(self.methods, 'methods_tfidf')
        print('succeed1/6')
        self.build_codes_tfidf(self.classes, 'classes_tfidf')
        print('succeed2/6')
        self.build_codes_tfidf(self.comments, 'comments_tfidf')
        print('succeed3/6')
        self.build_codes_tfidf(self.attributes, 'attributes_tfidf')
        print('succeed4/6')
        self.build_report_tfidf(self.summaries, 'summaries_tfidf')
        print('succeed5/6')
        self.build_report_tfidf(self.descriptions, 'descriptions_tfidf')
        print('succeed6/6')


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    print(datetime.datetime.now())
