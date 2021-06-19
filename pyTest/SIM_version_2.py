import json
import math
import sys

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from loadModule_swt import LoadModule


class CoreModule:
    # 一个report对应其file列表 例：'report75739.txt': ['Variant']
    real_codes = {}
    # 一个report对应其内容 例：'report75739.txt': ['Variant has no toString()', 'The Variant class has no toString() and one cannot call getString() in all cases since it throws an Exception if the']
    # 其中内容list中 list[0]是summary list[1]是description
    bug_contents = {}
    # 所有reports集合
    reports = {}
    # 所有codes集合
    codes = {}
    # 语料库
    corpus = []
    # report:该report与所有codes的相似度 <report:<code:similarity>>
    report_rVSM = {}
    # <report:<code:similarity>>
    report_SimiScore = {}
    # <report:<code:similarity>>
    report_FinalScore = {}
    # 记录report和code的所有tfidf
    report_tfidf = {}
    code_tfidf = {}
    # reports中每一个report所含词数的最大值
    terms_max = 0
    # reports中每一个report所含词数的最小值
    terms_min = 0
    # 所有的小写code name
    LowerCodeNames = []
    CodeNames = []

    def __init__(self, alpha):
        self.load()
        self.buildCorpus()
        self.compute_terms()
        self.buildReport_Cosine(alpha)

    # 加载所有的reports和codes
    def load(self):
        load_module = LoadModule()
        self.reports = load_module.read_report()
        self.codes = load_module.read_codes()
        self.real_codes = load_module.read_fixedfiles()

    # 构建语料库
    def buildCorpus(self):
        for key in self.reports.keys():
            self.corpus.append(self.reports[key])

        for key in self.codes.keys():
            self.corpus.append(self.codes[key])

    # 计算余弦相似度
    def compute_cos_sim(self, a, b):
        a_norm = np.linalg.norm(a)
        b_norm = np.linalg.norm(b)
        temp = np.dot(a, b)
        if temp == 0:
            return 0
        else:
            cos = np.dot(a, b) / (a_norm * b_norm)
            return cos

    # 对于每一个report,计算其和所有code的相似度g(#term)*cos
    def compute_rVSM_sim(self):
        for key in self.report_tfidf.keys():
            rVSM_sim = {}
            for code_key in self.code_tfidf.keys():
                a_norm = np.linalg.norm(self.report_tfidf[key])
                b_norm = np.linalg.norm(self.code_tfidf[code_key])
                cos = np.dot(self.report_tfidf[key], self.code_tfidf[code_key]) / (a_norm * b_norm)
                rVSM_sim[code_key] = 1 / (1 + math.exp(
                    -1 * self.normalize(len(self.reports[key]), self.terms_min, self.terms_max))) * cos
            self.report_rVSM[key] = rVSM_sim

    # 计算报告与code相似度
    def compute_SimiScore(self):
        # layer1
        for report_l1 in self.reports.keys():
            # 当前report对应的layer2和layer3
            layer2 = {}
            layer3 = {}
            # layer2
            for report_l2 in self.reports.keys():
                # similarity不为0的都可以算作本report的layer2
                if report_l1 != report_l2:
                    similarity = self.compute_cos_sim(self.report_tfidf[report_l1], self.report_tfidf[report_l2])
                    layer2[report_l2] = similarity
            # layer3
            # 所有layer2对应real_code加入layer3中
            for key_l2 in layer2.keys():
                # report相似度是0的不考虑
                if layer2[key_l2] == 0:
                    continue
                for real_code in self.real_codes[key_l2]:
                    if real_code not in layer3.keys():
                        layer3[real_code] = layer2[key_l2] / len(self.real_codes[key_l2])
                    else:
                        layer3[real_code] += layer2[key_l2] / len(self.real_codes[key_l2])
            self.report_SimiScore[report_l1] = layer3

    # 计算FinalScore
    def compute_FinalScore(self, alpha):
        # 标准化rVSM和SimiScore
        # 注意应该每个report对应所有的code都有一个FinalScore
        for key in self.report_SimiScore.keys():
            self.rVSM_min = sys.maxsize
            self.rVSM_max = -sys.maxsize - 1
            self.SimiScore_min = sys.maxsize
            self.SimiScore_max = -sys.maxsize - 1
            for code_key in self.report_SimiScore[key]:
                temp = self.report_SimiScore[key][code_key]
                temp1 = self.report_rVSM[key][code_key]
                # 找到最大最小
                if temp1 > self.rVSM_max:
                    self.rVSM_max = temp1
                if temp1 < self.rVSM_min:
                    self.rVSM_min = temp1
                if temp > self.SimiScore_max:
                    self.SimiScore_max = temp
                if temp < self.SimiScore_min:
                    self.SimiScore_min = temp
        for key in self.report_SimiScore.keys():
            for code_key in self.report_SimiScore[key]:
                self.report_rVSM[key][code_key] = self.normalize(self.report_rVSM[key][code_key], self.rVSM_min,
                                                                 self.rVSM_max)
                self.report_SimiScore[key][code_key] = self.normalize(self.report_SimiScore[key][code_key],
                                                                      self.SimiScore_min,
                                                                      self.SimiScore_max)
        # 计算FinalScore
        count = 0
        for key in self.report_SimiScore.keys():
            count += 1
            FinalScore = {}
            for code_key in self.report_SimiScore[key].keys():
                if self.report_SimiScore[key][code_key] < 0:
                    self.report_SimiScore[key][code_key] = 0
                FinalScore[code_key] = (1 - alpha) * self.report_rVSM[key][code_key] + alpha * \
                                       self.report_SimiScore[key][code_key]
            # FinalScore = sorted(FinalScore.items(), key=lambda x: x[1], reverse=True)
            self.report_FinalScore[key] = FinalScore
            print(count)
        for key in self.report_FinalScore.keys():
            self.report_FinalScore[key] = sorted(self.report_FinalScore[key].items(), key=lambda x: x[1], reverse=True)

    # 标准化
    def normalize(self, x, min, max):
        if max - min == 0:
            return 0
        return (x - min) / (max - min)

    def build_LowerCodeNames(self):
        for codeName in self.codes.keys():
            self.CodeNames.append(codeName)
            self.LowerCodeNames.append(codeName.lower())

    # 构建计算过的相似度，与report对应
    def buildReport_Cosine(self, alpha):
        # tfidf组件
        tfidf_vec = TfidfVectorizer(stop_words='english', sublinear_tf=True)
        tfidf_matrix = tfidf_vec.fit_transform(self.corpus)
        # 将计算出的tfidf拆分成report_tfidf和code_tfidf
        index = 0
        tfidf_array = tfidf_matrix.toarray()
        for key in self.reports.keys():
            self.report_tfidf[key] = tfidf_array[index]
            index += 1
        for key in self.codes.keys():
            self.code_tfidf[key] = tfidf_array[index]
            index += 1
        self.compute_rVSM_sim()
        self.compute_SimiScore()
        self.build_LowerCodeNames()
        self.compute_FinalScore(alpha)
        # 自己加的
        # for reportName in self.reports:
        #     report_list = self.reports[reportName].split(' ')
        #     for word in report_list:
        #         for i in range(len(self.LowerCodeNames)):
        #             if word.lower() == self.LowerCodeNames[i]:
        #                 FinalScore_dict = dict(self.report_FinalScore[reportName])
        #                 if self.CodeNames[i] not in dict(FinalScore_dict):
        #                     FinalScore_dict[self.CodeNames[i]] = 0.5
        #                 else:
        #                     FinalScore_dict[self.CodeNames[i]] += 0.1

    # 计算所有reports所含词个数的最大值与最小值
    def compute_terms(self):
        min_value = sys.maxsize
        max_value = -sys.maxsize - 1
        for report in self.reports.keys():
            size = len(self.reports[report])
            if size < min_value:
                min_value = size
            if size > max_value:
                max_value = size
        self.terms_min = min_value
        self.terms_max = max_value

    def preK(self, k, computed_codes, real_code):
        count = 0
        qualifiedNum = 0
        for codeTuple in computed_codes:
            if codeTuple[0] in real_code:
                qualifiedNum += 1
            count += 1
            if count == k:
                break
        return qualifiedNum / k

    # 计算topK指标
    def computeTopK(self, k):
        # 命中次数
        shot = 0
        report_father = []
        report_son = []
        # 判断reportSimilarity的前k个是不是至少含有一个realBugs里面的元素
        for reportName in self.report_FinalScore.keys():
            # 取computedCodes前K个,即相似度最高的K个,这里不一定能取到k个，注意判断
            topK = self.report_FinalScore.get(reportName)[0:k]
            real_bug = self.real_codes.get(reportName)
            for i in range(len(topK)):
                if real_bug.count(topK[i][0]) != 0:
                    shot += 1
                    report_father.append(reportName)
                    break
        for key in self.reports.keys():
            if key not in report_father:
                report_son.append(key)
        return shot / len(self.reports)

    # 计算MRR指标
    def computeMRR(self):
        result = 0
        # 排序后的report_cos列表中第一个是真实的的排名
        for report in self.reports.keys():
            # 一个report对应的所有<codeName,相似度>，此处降序
            computed_codes = self.report_FinalScore[report]
            # 一个report实际对应的Codes文件名
            real_code = self.real_codes[report]
            count = 1
            for codeTuple in computed_codes:
                if codeTuple[0] in real_code:
                    result += 1 / count
                    break
                count += 1
        return result / len(self.reports)

    def computeMAP(self):
        result = 0
        for report in self.reports.keys():
            # 一个report对应的所有<codeName,相似度>，此处降序
            computed_codes = self.report_FinalScore[report]
            # 一个report实际对应的Codes文件名
            real_code = self.real_codes[report]
            # 建立K_j,从1开始
            K_j = []
            count = 1
            # 如果有当前code在真实code的里面，添加到K_j
            for codeTuple in computed_codes:
                if codeTuple[0] in real_code:
                    K_j.append(count)
                count += 1

            # 计算avgP_j
            avgP_j = 0
            for i in range(len(K_j)):
                avgP_j += self.preK(K_j[i], computed_codes, real_code)
            if len(K_j) != 0:
                avgP_j /= len(K_j)
                result += avgP_j
        return result / len(self.reports)


if __name__ == '__main__':
    coreModule = CoreModule(1)
    print("Top1: " + str(coreModule.computeTopK(1)))
    print("Top5: " + str(coreModule.computeTopK(5)))
    print("Top10: " + str(coreModule.computeTopK(10)))
    print("MRR: " + str(coreModule.computeMRR()))
    print("MAP: " + str(coreModule.computeMAP()))
    result = {}
    for report in coreModule.report_FinalScore.keys():
        FinalScore = {}
        for code in coreModule.codes:
            report_FinalScore_dict = dict(coreModule.report_FinalScore[report])
            if code not in report_FinalScore_dict.keys():
                FinalScore[code] = 0
            else:
                FinalScore[code] = report_FinalScore_dict[code]
        result[report] = FinalScore
    with open('SIM_version_2_AJ.json', 'w') as file_obj:
        json.dump(result, file_obj)

    # i = 1
    # Top5 = 0
    # Top10 = 0
    # MRR = 0
    # MAP = 0
    # Top1_max = 0
    # Top5_max = 0
    # Top10_max = 0
    # MRR_max = 0
    # MAP_max = 0
    # Top1_alpha = 0.2
    # Top5_alpha = 0.2
    # Top10_alpha = 0.2
    # MRR_alpha = 0.2
    # MAP_alpha = 0.2
    # for i in np.arange(0.2,0.3,0.001):
    #     coreModule = CoreModule(i)
    #     Top1 = coreModule.computeTopK(1)
    #     Top5 = coreModule.computeTopK(5)
    #     Top10 = coreModule.computeTopK(10)
    #     MRR = coreModule.computeMRR()
    #     MAP = coreModule.computeMAP()
    #     if Top1_max < Top1:
    #         Top1_max = Top1
    #         Top1_alpha = i
    #     if Top5_max < Top5:
    #         Top5_max = Top5
    #         Top5_alpha = i
    #     if Top10_max < Top10:
    #         Top10_max = Top10
    #         Top10_alpha = i
    #     if MRR_max < MRR:
    #         MRR_max = MRR
    #         MRR_alpha = i
    #     if MAP_max < MAP:
    #         MAP_max = MAP
    #         MAP_alpha = i
    # print("Top1: " + str(Top1_alpha))
    # print("Top5: " + str(Top5_alpha))
    # print("Top10: " + str(Top10_alpha))
    # print("MRR: " + str(MRR_alpha))
    # print("MAP: " + str(MAP_alpha))
    # print("=================")
    # print("Top1: " + str(Top1_max))
    # print("Top5: " + str(Top5_max))
    # print("Top10: " + str(Top10_max))
    # print("MRR: " + str(MRR_max))
    # print("MAP: " + str(MAP_max))

# Top1: 0.24600000000000005
# Top5: 0.21300000000000002
# Top10: 0.2
# MRR: 0.24700000000000005
# MAP: 0.2970000000000001

# 最高
# Top1: 0.35714285714285715
# Top5: 0.6428571428571429
# Top10: 0.7551020408163265
# MRR: 0.4876624782594291
