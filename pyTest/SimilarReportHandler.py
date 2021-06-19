import copy
import datetime
import json
import math
from collections import OrderedDict, Counter

import numpy as np
from loadModule import LoadModule


def cosine_sim(a, b):
    """
    计算余弦相似度
    :param a: vector a
    :param b: vector b
    :return: cosine_sim
    """
    a_array = np.array(list(a.values()))
    b_array = np.array(list(b.values()))
    return a_array.dot(b_array) / (np.linalg.norm(a_array) * np.linalg.norm(b_array))


class StructureHandler:
    def __init__(self):
        # 语料库
        self.corpus = []
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_report()
        self.codes = self.loadModule.read_codes()
        # 构建
        self.build_corpus()
        self.zero_vector = self.build_zero_vector()
        # 计算tfidf
        self.build_tfidf()
        # 实际code
        self.real_codes = self.loadModule.read_fixedfiles()
        # 计算相似度 reportName{source code: sim}
        self.result = {}
        self.build_sim()

    def build_corpus(self):
        """
        构建corpus，用所有的词s
        :return:
        """
        doc_tokens = []
        for doc in self.reports.values():
            doc_tokens += [sorted(doc.split(' '))]
        for doc in self.codes.values():
            doc_tokens += [sorted(doc.split(' '))]
        all_doc_tokens = sum(doc_tokens, [])
        self.corpus = sorted(set(all_doc_tokens))

    def build_zero_vector(self):
        """
        从corpus创建全是0的one-hot向量
        :return: zero_vector
        """
        zero_vector = OrderedDict((token, 0.0) for token in self.corpus)
        return zero_vector

    # docs数据格式 docName:[content]
    def build_report_tfidf(self, docs):
        """
        计算所有report的tfidf
        :param docs: methods, classes, comments, attributes
        :return: {reportName: tfidf vector}
        """
        document_tfidf_vectors = {}
        for docName in docs.keys():
            # one-hot 向量的复制
            vec = copy.copy(self.zero_vector)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                #
                for _docName in docs.keys():
                    if key in docs[_docName]:
                        docs_containing_key += 1
                # todo 修改 report tf公式
                tf = math.log(value / len(self.corpus)) + 1
                # todo 修改 report idf公式
                if docs_containing_key:
                    idf = math.log((len(docs.keys())) / (docs_containing_key + 1))
                else:
                    idf = 0
                vec[key] = tf * idf
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

    # docs数据格式 docName:[content]
    def build_codes_tfidf(self, docs):
        """
        计算所有codes的tfidf
        :param docs: summaries, descriptions
        :return: {codeName: tfidf vector}
        """
        document_tfidf_vectors = {}
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
                tf = math.log(value / len(self.corpus)) + 1
                # todo 修改code idf公式
                if docs_containing_key:
                    idf = math.log((len(docs.keys())) / (docs_containing_key + 1))
                else:
                    idf = 0
                vec[key] = tf * idf
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

    def build_tfidf(self):
        self.codes_tfidf = self.build_codes_tfidf(self.codes)
        self.reports_tfidf = self.build_report_tfidf(self.reports)

    def build_sim(self):
        # one-hot，对于每一个source code都是0
        zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())
        for reportName in self.reports.keys():
            vec = copy.copy(zero_vector)
            # 每一个source code都算相似度 （8个）
            for codeName in self.codes.keys():
                sim = 0
                for old_report in self.reports.keys():
                    # 如果在这个report的fixedFiles里面
                    if codeName in self.real_codes[old_report] and old_report != reportName:
                        sim += (cosine_sim(self.reports_tfidf[reportName], self.reports_tfidf[old_report]) / len(
                            self.real_codes[old_report]))
                vec[codeName] = float(sim)
            vec = OrderedDict(sorted(vec.items(), reverse=True, key=lambda x: x[1]))
            self.result[reportName] = vec

    # 计算topK指标
    def computeTopK(self, k):
        # 命中次数
        shot = 0
        # 判断reportSimilarity的前k个是不是至少含有一个realBugs里面的元素
        for reportName in self.result.keys():
            # 取computedCodes前K个,即相似度最高的K个,这里不一定能取到k个，注意判断
            topK = list(self.result[reportName].keys())[0:k]
            real_bug = self.real_codes[reportName]
            for i in range(len(topK)):
                if real_bug.count(topK[i]) != 0:
                    shot += 1
                    break
        return shot / len(self.reports)


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    print(handler.result)
    with open('SIM_Eclipse.json', 'w') as file_obj:
        json.dump(handler.result, file_obj)
    print(datetime.datetime.now())
