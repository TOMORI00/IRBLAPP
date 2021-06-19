import datetime
import json
import math
from collections import OrderedDict, Counter

import copy
import numpy as np

from loadModule import LoadModule


# todo 添加新来一个报告的结果
# todo 添加结果持久化

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
        # 计算相似度 reportName{source code: sim}
        self.result = {}
        self.build_sim()
        # 实际code
        self.real_codes = self.loadModule.read_fixedfiles()

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
    def build_codes_tfidf(self, docs):
        """
        计算所有codes的tfidf
        :param docs: summaries, descriptions
        :return: {codeName: tfidf vector}
        """
        k1 = 1.0
        b = 0.3
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
                # todo 修改 report tf公式
                # tf = value / len(self.corpus)
                tf = (k1 * value) / (value + k1 * (1 - b + b * (len(token_counts.items()) / self.source_code_len_mean)))
                # todo 修改 report idf公式
                if docs_containing_key:
                    idf = math.log((len(docs.keys()) + 1) / (docs_containing_key + 0.5))
                else:
                    idf = 0
                vec[key] = tf * idf
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
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

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
        self.methods_tfidf = self.build_codes_tfidf(self.methods)
        print('ok')
        self.classes_tfidf = self.build_codes_tfidf(self.classes)
        print('ok')
        self.comments_tfidf = self.build_codes_tfidf(self.comments)
        print('ok')
        self.attributes_tfidf = self.build_codes_tfidf(self.attributes)
        print('ok')
        self.summaries_tfidf = self.build_report_tfidf(self.summaries)
        print('ok')
        self.descriptions_tfidf = self.build_report_tfidf(self.descriptions)
        print('ok')

    def build_sim(self):
        # one-hot，对于每一个source code都是0
        zero_vector = OrderedDict((token, 0) for token in self.codes.keys())
        for reportName in self.reports.keys():
            vec = copy.copy(zero_vector)
            # 每一个source code都算相似度 （8个）
            for codeName in self.codes.keys():
                sim = 0
                sim += cosine_sim(self.summaries_tfidf[reportName], self.methods_tfidf[codeName])
                sim += cosine_sim(self.summaries_tfidf[reportName], self.classes_tfidf[codeName])
                sim += cosine_sim(self.summaries_tfidf[reportName], self.attributes_tfidf[codeName])
                sim += cosine_sim(self.summaries_tfidf[reportName], self.comments_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.methods_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.classes_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.attributes_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.comments_tfidf[codeName])
                vec[codeName] = sim
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
    with open('SC_Eclipse.json', 'w') as file_obj:
        json.dump(handler.result, file_obj)
    # print("Top1: " + str(handler.computeTopK(1)))
    # print("Top5: " + str(handler.computeTopK(5)))
    # print("Top10: " + str(handler.computeTopK(10)))
    print(datetime.datetime.now())
