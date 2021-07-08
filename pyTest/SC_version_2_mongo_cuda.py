import copy
import datetime
import math
import sys
from collections import OrderedDict

import cupy as cp
import numpy as np
import pymongo

from loadModule_eclipse import LoadModule


# todo one-hot向量去除key

def normalize(x, min, max):
    if min == max:
        return 0
    else:
        return 6 * (x - min) / (max - min)


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
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_report()
        self.codes = self.loadModule.read_codes()
        self.max_len_codes = self.build_max_len(self.codes)
        self.min_len_codes = self.build_min_len(self.codes)
        # 加载语料库
        self.corpus = self.loadModule.read_corpus()
        # 数据库连接
        self.client = pymongo.MongoClient(host='172.31.42.10', port=27017)
        self.db = self.client.irbl
        # 加载source code 4 个属性
        self.methods_tfidf = self.loadModule.read_methods_tfidf()
        self.classes_tfidf = self.loadModule.read_classes_tfidf()
        self.comments_tfidf = self.loadModule.read_comments_tfidf()
        self.attributes_tfidf = self.loadModule.read_attributes_tfidf()
        # 加载report两个属性
        self.summaries_tfidf = self.loadModule.read_summaries_tfidf()
        self.descriptions_tfidf = self.loadModule.read_descriptions_tfidf()
        # 计算所有文档数量
        self.doc_num = 20526
        # 计算相似度 reportName{source code: sim}
        self.result = {}
        self.build_sim()
        # 实际code
        self.real_codes = self.loadModule.read_fixedfiles()

    def build_source_codes_len_mean(self, codes):
        """
        计算source code内容的平均长度
        :return: source_codes_len_mean
        """
        lens = []
        for codeName in codes:
            lens.append(len(codes[codeName]))
        return np.mean(lens)

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

    def build_sim(self):
        # one-hot，对于每一个source code都是0
        count = 0
        zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())
        report_list = list(self.reports.keys())[950:1000]
        for reportName in report_list:
            if self.db['SC_Eclipse'].find_one({'report_id': reportName}) is not None:
                continue
            vec = copy.copy(zero_vector)
            # 每一个source code都算相似度 （8个）
            score_list = []
            for codeName in self.codes.keys():
                sim = 0
                sim += cosine_sim(self.summaries_tfidf[reportName], self.methods_tfidf[codeName])
                sim += cosine_sim(self.summaries_tfidf[reportName], self.classes_tfidf[codeName])
                sim += cosine_sim(self.summaries_tfidf[reportName], self.attributes_tfidf[codeName])
                sim += cosine_sim(self.summaries_tfidf[reportName], self.comments_tfidf[codeName]) * 0.5
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.methods_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.classes_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.attributes_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.comments_tfidf[codeName]) * 0.5
                # vec[codeName] = float(sim)
                len_score = 1 / (1 + math.exp(
                    -1 * normalize(len(self.codes[codeName]), self.min_len_codes, self.max_len_codes)))
                if len_score < 0.5:
                    len_score = 0.5
                if len_score > 6:
                    len_score = 6
                rVSM_sim = len_score * float(sim)
                score_list.append({'code_name': codeName, 'score': float(rVSM_sim)})
            # vec = OrderedDict(sorted(vec.items(), reverse=True, key=lambda x: x[1]))
            # 存入mongodb
            self.result[reportName] = vec
            # 存入mongodb
            if self.db['SC_Eclipse'].find_one({'report_id': reportName}) is None:
                self.db['SC_Eclipse'].insert_one({'report_id': reportName, 'score_list': score_list})
                count += 1
                print(count)
                print(reportName)
                print('=========')


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    print(datetime.datetime.now())
