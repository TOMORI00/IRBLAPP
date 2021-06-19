import copy
import datetime
import json
import math
from collections import OrderedDict, Counter

import cupy as cp
from loadModule_swt import LoadModule


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
        self.fixdate = self.loadModule.read_fixdate()
        self.opendate = self.loadModule.read_opendate()
        self.doc_num = len(self.reports) + len(self.codes)
        # 构建
        self.build_corpus()
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
        # 所有词的list
        self.corpus_list = list(sorted(set(all_doc_tokens)))
        # 构建corpus，{word:在corpur_list中的下标}
        for i, word in enumerate(self.corpus_list):
            self.corpus[word] = i

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
            vec = [0] * len(self.corpus)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                for _docName in self.reports.keys():
                    if key in self.reports[_docName]:
                        docs_containing_key += 1
                for _docName in self.codes.keys():
                    if key in self.codes[_docName]:
                        docs_containing_key += 1
                # todo 修改 report tf公式
                tf = math.log(value / len(tokens)) + 1
                # todo 修改 report idf公式
                if docs_containing_key:
                    idf = math.log(self.doc_num / (docs_containing_key+1))
                else:
                    idf = 0
                vec[self.corpus[key]] = tf * idf
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
            vec = [0] * len(self.corpus)
            tokens = docs[docName].split(' ')
            token_counts = Counter(tokens)
            # 添加tfidf
            for key, value in token_counts.items():
                docs_containing_key = 0
                for _docName in self.reports.keys():
                    if key in self.reports[_docName]:
                        docs_containing_key += 1
                for _docName in self.codes.keys():
                    if key in self.codes[_docName]:
                        docs_containing_key += 1
                # todo 修改code tf公式
                tf = math.log(value / len(tokens)) + 1
                # todo 修改code idf公式
                if docs_containing_key:
                    idf = math.log(self.doc_num / (docs_containing_key+1))
                else:
                    idf = 0
                vec[self.corpus[key]] = tf * idf
            document_tfidf_vectors[docName] = vec
        return document_tfidf_vectors

    def build_tfidf(self):
        self.codes_tfidf = self.build_codes_tfidf(self.codes)
        print('ok')
        self.reports_tfidf = self.build_report_tfidf(self.reports)
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
                for old_report in self.reports.keys():
                    # 如果在这个report的fixedFiles里面,input的report的opendate要在old report的fixdate之后
                    if codeName in self.real_codes[old_report] and reportName is not old_report:
                        sim += (cosine_sim(self.reports_tfidf[reportName], self.reports_tfidf[old_report]) / len(
                            self.real_codes[old_report]))
                vec[codeName] = float(sim)
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


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    print("Top1: " + str(handler.computeTopK(1)))
    print("Top5: " + str(handler.computeTopK(5)))
    print("Top10: " + str(handler.computeTopK(10)))
    with open('./resultForSWT/SIM_SWT_new.json', 'w') as file_obj:
        json.dump(handler.result, file_obj)
    print(datetime.datetime.now())
