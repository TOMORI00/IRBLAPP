import copy
import datetime
from collections import OrderedDict

import cupy as cp
import pymongo

from loadModule import LoadModule


# todo 修改数据库report_id


def cosine_sim(a, b):
    """
    计算余弦相似度
    :param a: vector a
    :param b: vector b
    :return: cosine_sim
    """
    a_array = cp.array(list(a.values()))
    b_array = cp.array(list(b.values()))
    return a_array.dot(b_array) / (cp.linalg.norm(a_array) * cp.linalg.norm(b_array))


class StructureHandler:
    def __init__(self):
        # 数据库连接
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.irbl
        # 计算相似度 reportName{source code: sim}
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_report()
        self.codes = self.loadModule.read_codes()
        self.build_sim()

    def build_sim(self):
        # one-hot，对于每一个source code都是0
        zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())
        count = 0
        for reportName in self.reports.keys():
            if self.db['SC_AspectJ'].find_one({'report_id': reportName}) is not None:
                continue
            # vec = copy.copy(zero_vector)
            count += 1
            # 每一个source code都算相似度 （8个）
            score_list = []
            for codeName in self.codes.keys():
                sim = 0
                # descriptions_tfidf = {}
                # summaries_tfidf = {}
                # classes_tfidf = {}
                # comments_tfidf = {}
                # attributes_tfidf = {}
                # methods_tfidf = {}
                # for item in self.db.descriptions_tfidf.find():
                #     descriptions_tfidf.update({item['report_id']: item['tf_idf']})
                # for item in self.db.summaries_tfidf.find():
                #     summaries_tfidf.update({item['report_id']: item['tf_idf']})
                # for item in self.db.comments_tfidf.find():
                #     comments_tfidf.update({item['report_id']: item['tf_idf']})
                # for item in self.db.attributes_tfidf.find():
                #     attributes_tfidf.update({item['report_id']: item['tf_idf']})
                # for item in self.db.classes_tfidf.find():
                #     classes_tfidf.update({item['report_id']: item['tf_idf']})
                # for item in self.db.methods_tfidf.find():
                #     methods_tfidf.update({item['report_id']: item['tf_idf']})
                #
                # sim += cosine_sim(summaries_tfidf[reportName], methods_tfidf[codeName])
                # sim += cosine_sim(summaries_tfidf[reportName], classes_tfidf[codeName])
                # sim += cosine_sim(summaries_tfidf[reportName], attributes_tfidf[codeName])
                # sim += cosine_sim(summaries_tfidf[reportName], comments_tfidf[codeName])
                # sim += cosine_sim(descriptions_tfidf[reportName], methods_tfidf[codeName])
                # sim += cosine_sim(descriptions_tfidf[reportName], classes_tfidf[codeName])
                # sim += cosine_sim(descriptions_tfidf[reportName], attributes_tfidf[codeName])
                # sim += cosine_sim(descriptions_tfidf[reportName], comments_tfidf[codeName])

                description = self.db.descriptions_tfidf.find_one({'report_id': reportName})['tf_idf']
                summary = self.db.summaries_tfidf.find_one({'report_id': reportName})['tf_idf']
                clazz = self.db.classes_tfidf.find_one({'report_id': codeName})['tf_idf']
                comment = self.db.comments_tfidf.find_one({'report_id': codeName})['tf_idf']
                method = self.db.methods_tfidf.find_one({'report_id': codeName})['tf_idf']
                attribute = self.db.attributes_tfidf.find_one({'report_id': codeName})['tf_idf']
                sim += cosine_sim(description, clazz)
                sim += cosine_sim(description, comment)
                sim += cosine_sim(description, method)
                sim += cosine_sim(description, attribute)
                sim += cosine_sim(summary, clazz)
                sim += cosine_sim(summary, comment)
                sim += cosine_sim(summary, method)
                sim += cosine_sim(summary, attribute)
                # todo key 不能用codeName
                score_list.append({'code_name': codeName, 'score': float(sim)})
            # vec = OrderedDict(sorted(vec.items(), reverse=True, key=lambda x: x[1]))
            # 存入mongodb
            if self.db['SC_AspectJ'].find_one({'report_id':reportName}) is None:
                self.db['SC_AspectJ'].insert_one({'report_id': reportName, 'score_list': score_list})
            print(str(count))


if __name__ == '__main__':
    print(datetime.datetime.now())
    handler = StructureHandler()
    print(datetime.datetime.now())
