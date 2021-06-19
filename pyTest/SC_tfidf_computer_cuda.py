import copy
import datetime
import json
import math
from collections import OrderedDict, Counter

import cupy as cp
import numpy as np

from loadModule_aspectj import LoadModule


# todo one-hot向量去除key

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
        self.corpus = {}
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
        self.doc_num = len(self.descriptions) + len(self.summaries) + len(self.attributes) + len(self.comments) + len(
            self.classes) + len(self.methods)
        print(self.doc_num)
        # 构建corpus
        self.build_corpus()
        self.methods_len_mean = self.build_source_codes_len_mean(self.methods)
        self.classes_len_mean = self.build_source_codes_len_mean(self.classes)
        self.attributes_len_mean = self.build_source_codes_len_mean(self.attributes)
        self.comments_len_mean = self.build_source_codes_len_mean(self.comments)
        # 计算tfidf
        self.build_tfidf()

    def build_corpus(self):
        """
        构建corpus，{word:index}
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
        # 所有词的list
        self.corpus_list = list(sorted(set(all_doc_tokens)))
        # 构建corpus，{word:在corpur_list中的下标}
        for i, word in enumerate(self.corpus_list):
            self.corpus[word] = i

    # docs数据格式 docName:[content]
    def build_codes_tfidf(self, docs, len_mean):
        """
        计算所有codes的tfidf
        :param docs: summaries, descriptions
        :return: {codeName: tfidf vector}
        """
        k1 = 1.0
        b = 0.3
        document_tfidf_vectors = {}
        for docName in docs.keys():
            # one-hot 只需要value不需要key，key就是corpus_list
            vec = [0] * len(self.corpus)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                # idf对于全局都要计算
                for _docName in self.methods.keys():
                    if key in self.methods[_docName]:
                        docs_containing_key += 1
                for _docName in self.classes.keys():
                    if key in self.classes[_docName]:
                        docs_containing_key += 1
                for _docName in self.attributes.keys():
                    if key in self.attributes[_docName]:
                        docs_containing_key += 1
                for _docName in self.comments.keys():
                    if key in self.comments[_docName]:
                        docs_containing_key += 1
                for _docName in self.descriptions.keys():
                    if key in self.descriptions[_docName]:
                        docs_containing_key += 1
                for _docName in self.summaries.keys():
                    if key in self.summaries[_docName]:
                        docs_containing_key += 1
                # todo 修改 report tf公式
                tf = math.log(value) + 1
                # tf = (k1 * value) / (value + k1 * (1 - b + b * (len(tokens) / len_mean)))
                # todo 修改 report idf公式
                if docs_containing_key:
                    idf = math.log(self.doc_num / (docs_containing_key + 1))
                else:
                    idf = 0
                vec[self.corpus[key]] = tf * idf
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

    # docs数据格式 docName:[content]
    def build_report_tfidf(self, docs):
        """
        计算所有report的tfidf
        :param docs: methods, classes, comments, attributes
        :return: {reportName: tfidf vector}
        """
        k3 = 1000
        document_tfidf_vectors = {}
        for docName in docs.keys():
            # one-hot 只需要value不需要key，key就是corpus_list
            vec = [0] * len(self.corpus)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                # idf对于全局都要计算
                for _docName in self.methods.keys():
                    if key in self.methods[_docName]:
                        docs_containing_key += 1
                for _docName in self.classes.keys():
                    if key in self.classes[_docName]:
                        docs_containing_key += 1
                for _docName in self.attributes.keys():
                    if key in self.attributes[_docName]:
                        docs_containing_key += 1
                for _docName in self.comments.keys():
                    if key in self.comments[_docName]:
                        docs_containing_key += 1
                for _docName in self.descriptions.keys():
                    if key in self.descriptions[_docName]:
                        docs_containing_key += 1
                for _docName in self.summaries.keys():
                    if key in self.summaries[_docName]:
                        docs_containing_key += 1
                # todo 修改code tf公式
                tf = math.log(value) + 1
                # tf = (k3 * value) / (value + k3)
                # todo 修改code idf公式
                if docs_containing_key:
                    idf = math.log(self.doc_num / (docs_containing_key + 1))
                else:
                    idf = 0
                vec[self.corpus[key]] = tf * idf
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

    def build_tfidf(self):
        with open('./tfidfForAspectJ/corpus_AspectJ.json', 'w') as file_obj:
            json.dump(self.corpus, file_obj)
        print('corpus ok')
        self.methods_tfidf = self.build_codes_tfidf(self.methods, self.methods_len_mean)
        with open('./tfidfForAspectJ/methods_AspectJ.json', 'w') as file_obj:
            json.dump(self.methods_tfidf, file_obj)
        print('ok')
        self.classes_tfidf = self.build_codes_tfidf(self.classes, self.classes_len_mean)
        with open('./tfidfForAspectJ/classes_AspectJ.json', 'w') as file_obj:
            json.dump(self.classes_tfidf, file_obj)
        print('ok')
        self.comments_tfidf = self.build_codes_tfidf(self.comments, self.comments_len_mean)
        with open('./tfidfForAspectJ/comments_AspectJ.json', 'w') as file_obj:
            json.dump(self.comments_tfidf, file_obj)
        print('ok')
        self.attributes_tfidf = self.build_codes_tfidf(self.attributes, self.attributes_len_mean)
        with open('./tfidfForAspectJ/attributes_AspectJ.json', 'w') as file_obj:
            json.dump(self.attributes_tfidf, file_obj)
        print('ok')
        self.summaries_tfidf = self.build_report_tfidf(self.summaries)
        with open('./tfidfForAspectJ/summaries_AspectJ.json', 'w') as file_obj:
            json.dump(self.summaries_tfidf, file_obj)
        print('ok')
        self.descriptions_tfidf = self.build_report_tfidf(self.descriptions)
        with open('./tfidfForAspectJ/descriptions_AspectJ.json', 'w') as file_obj:
            json.dump(self.descriptions_tfidf, file_obj)
        print('ok')

    def build_source_codes_len_mean(self, codes):
        """
        计算source code内容的平均长度
        :return: source_codes_len_mean
        """
        lens = []
        for codeName in codes:
            lens.append(len(codes[codeName]))
        return np.mean(lens)


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    mean_lens = {}
    mean_lens['methods_len_mean'] = handler.build_source_codes_len_mean(handler.methods)
    mean_lens['classes_len_mean'] = handler.build_source_codes_len_mean(handler.classes)
    mean_lens['attributes_len_mean'] = handler.build_source_codes_len_mean(handler.attributes)
    mean_lens['comments_len_mean'] = handler.build_source_codes_len_mean(handler.comments)
    print(handler.doc_num)
    with open('./tfidfForAspectJ/mean_lens_AspectJ.json', 'w') as file_obj:
        json.dump(mean_lens, file_obj)
    print(datetime.datetime.now())
