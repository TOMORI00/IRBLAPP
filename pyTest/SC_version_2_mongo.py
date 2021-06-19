import copy
import datetime
from collections import OrderedDict

import numpy as np
import pymongo

from loadModule_eclipse import LoadModule


# todo one-hot向量去除key

def cosine_sim(a, b):
    """
    计算余弦相似度
    :param a: vector a
    :param b: vector b
    :return: cosine_sim
    """
    a_array = np.array(a)
    b_array = np.array(b)
    return a_array.dot(b_array) / (np.linalg.norm(a_array) * np.linalg.norm(b_array))


class StructureHandler:
    def __init__(self):
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_report()
        self.codes = self.loadModule.read_codes()
        # 加载语料库
        self.corpus = self.loadModule.read_corpus()
        # 数据库连接
        # todo 更换成公共的
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

    def build_sim(self):
        # one-hot，对于每一个source code都是0
        count = 0
        zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())
        report_list = list(self.reports.keys())[# 这里填入分片]
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
                sim += cosine_sim(self.summaries_tfidf[reportName], self.comments_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.methods_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.classes_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.attributes_tfidf[codeName])
                sim += cosine_sim(self.descriptions_tfidf[reportName], self.comments_tfidf[codeName])
                # vec[codeName] = float(sim)
                score_list.append({'code_name': codeName, 'score': float(sim)})
            # vec = OrderedDict(sorted(vec.items(), reverse=True, key=lambda x: x[1]))
            # 存入mongodb
            self.result[reportName] = vec
            # 存入mongodb
            if self.db['SC_Eclipse'].find_one({'report_id': reportName}) is None:
                self.db['SC_Eclipse'].insert_one({'report_id': reportName, 'score_list': score_list})
                count += 1
                print(count)
                print(reportName)
                print('========')



if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    print(datetime.datetime.now())
