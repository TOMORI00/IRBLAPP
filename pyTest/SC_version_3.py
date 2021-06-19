import copy
import datetime
import json
import math
import sys
from collections import OrderedDict, Counter

import cupy as cp
import numpy as np
from loadModule_swt import LoadModule


def normalize(x, min, max):
    if min == max:
        return 0
    else:
        return 6 * (x - min) / (max - min)


class StructureHandler:
    def __init__(self):
        # 语料库
        self.corpus = {}
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_report()
        self.codes = self.loadModule.read_codes()
        self.max_len_codes = self.build_max_len(self.codes)
        self.min_len_codes = self.build_min_len(self.codes)
        # 加载source code 4 个属性
        self.methods = self.loadModule.read_methods()
        self.classes = self.loadModule.read_classes()
        self.comments = self.loadModule.read_comments()
        self.attributes = self.loadModule.read_attributes()
        # 加载report两个属性
        self.summaries = self.loadModule.read_summaries()
        self.descriptions = self.loadModule.read_descriptions()
        self.min_len_summary = self.build_min_len(self.summaries)
        self.min_len_description = self.build_min_len(self.descriptions)
        self.max_len_summary = self.build_max_len(self.summaries)
        self.max_len_description = self.build_max_len(self.descriptions)
        # 构建corpus
        self.build_corpus()
        self.methods_len_mean = self.build_source_codes_len_mean(self.methods)
        self.classes_len_mean = self.build_source_codes_len_mean(self.classes)
        self.attributes_len_mean = self.build_source_codes_len_mean(self.attributes)
        self.comments_len_mean = self.build_source_codes_len_mean(self.comments)
        self.doc_num = len(self.descriptions) + len(self.summaries) + len(self.attributes) + len(self.comments) + len(
            self.classes) + len(self.methods)
        # 计算tfidf
        self.build_tfidf()
        # 计算相似度 reportName{source code: sim}
        self.result = {}
        self.build_sim()
        # 实际code
        self.real_codes = (self.loadModule.read_fixedfiles())

    def cosine_sim(self, a, b, code_name):
        """
        计算余弦相似度
        :param a: vector a
        :param b: vector b
        :return: cosine_sim
        """
        a_array = cp.array(a)
        b_array = cp.array(b)
        return a_array.dot(b_array) / (cp.linalg.norm(a_array) * cp.linalg.norm(b_array))

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
                    idf = math.log(self.doc_num / docs_containing_key+1)
                    # idf = math.log((self.doc_num + 1) / (docs_containing_key + 0.5))
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
                    idf = math.log(self.doc_num/ docs_containing_key + 1)
                    # idf = math.log((self.doc_num + 1) / (docs_containing_key + 0.5))
                else:
                    idf = 0
                vec[self.corpus[key]] = tf * idf
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

    def build_source_codes_len_mean(self, codes):
        """
        计算source code内容的平均长度
        :return: source_codes_len_mean
        """
        lens = []
        for codeName in codes:
            lens.append(len(codes[codeName]))
        return np.mean(lens)

    def build_tfidf(self):
        self.methods_tfidf = self.build_codes_tfidf(self.methods, self.methods_len_mean)
        print('ok')
        self.classes_tfidf = self.build_codes_tfidf(self.classes, self.classes_len_mean)
        print('ok')
        self.comments_tfidf = self.build_codes_tfidf(self.comments, self.comments_len_mean)
        print('ok')
        self.attributes_tfidf = self.build_codes_tfidf(self.attributes, self.attributes_len_mean)
        print('ok')
        self.summaries_tfidf = self.build_report_tfidf(self.summaries)
        print('ok')
        self.descriptions_tfidf = self.build_report_tfidf(self.descriptions)
        print('ok')

    def build_sim(self):
        # one-hot，对于每一个source code都是0
        count = 0
        zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())
        for reportName in self.reports.keys():
            vec = copy.copy(zero_vector)
            # 每一个source code都算相似度 （8个）
            for codeName in self.codes.keys():
                sim = 0
                sim += self.cosine_sim(self.summaries_tfidf[reportName], self.methods_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.summaries_tfidf[reportName], self.classes_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.summaries_tfidf[reportName], self.attributes_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.summaries_tfidf[reportName], self.comments_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.descriptions_tfidf[reportName], self.methods_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.descriptions_tfidf[reportName], self.classes_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.descriptions_tfidf[reportName], self.attributes_tfidf[codeName], codeName)
                sim += self.cosine_sim(self.descriptions_tfidf[reportName], self.comments_tfidf[codeName],
                                       codeName)
                len_score = 1 / (1 + math.exp(
                    -1 * normalize(len(self.codes[codeName]), self.min_len_codes, self.max_len_codes)))
                if len_score < 0.5:
                    len_score = 0.5
                if len_score > 6:
                    len_score = 6
                rVSM_sim = len_score * float(sim)
                vec[codeName] = rVSM_sim
            vec = OrderedDict(sorted(vec.items(), reverse=True, key=lambda x: x[1]))
            self.result[reportName] = vec
            count += 1
            print(count)

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

    def build_min_len(self, reports):
        min_value = sys.maxsize
        for report in reports.keys():
            if min_value > len(reports[report]):
                min_value = len(reports[report])
        return min_value

    def build_max_len(self, reports):
        max_value = -sys.maxsize - 1
        for report in reports.keys():
            if max_value < len(reports[report]):
                max_value = len(reports[report])
        return max_value


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    with open('SC_version_3_swt.json', 'w') as file_obj:
        json.dump(handler.result, file_obj)
    print("Top1: " + str(handler.computeTopK(1)))
    print("Top5: " + str(handler.computeTopK(5)))
    print("Top10: " + str(handler.computeTopK(10)))
    print(datetime.datetime.now())
