import math
import random
import time
from datetime import date
from itertools import count

import numpy as np
import json
import os

# author:whc
# date:2021/6/3
from sko.GA import GA
from sko.demo_func import schaffer

from sko.operators import ranking, selection, crossover, mutation

DNA_SIZE = 25
POP_SIZE = 50
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.1
N_GENERATIONS = 200
W1_BOUND = [0, 1]
W2_BOUND = [0, 1]
W3_BOUND = [0, 1]
W4_BOUND = [0, 1]
W5_BOUND = [0, 1]
test = []
train = []

RIC = {}
SC = {}
SIM = {}
STC = {}
VHC = {}
REPORTS = {}
REAL_CODES = {}

RIC_test = {}
SC_test = {}
SIM_test = {}
STC_test = {}
VHC_test = {}

RIC_train = {}
SC_train = {}
SIM_train = {}
STC_train = {}
VHC_train = {}
name_of_project = ""
REAL_CODES_train = {}


def split_train(percent):
    # 输入测试集的比例

    global RIC_train
    global RIC_test
    global SC_test
    global SC_train
    global SIM_test
    global SIM_train
    global STC_test
    global STC_train
    global VHC_test
    global VHC_train
    num = int(len(RIC.keys()) * percent / 100)  # 测试集数量
    ALL = RIC.copy()
    i = 0
    key_r = random.choice(list(ALL.keys()))
    # print()
    global test
    global train
    global REAL_CODES_train
    while i != num:
        if key_r not in test:
            i += 1
            test.append(key_r)
        key_r = random.choice(list(ALL.keys()))
    # t_size=float(percent/100)
    # train, test = train_test_split(ALL, test_size=t_size)
    for key_ALL in ALL.keys():
        if key_ALL not in test:
            train.append(key_ALL)
            REAL_CODES_train[key_ALL] = REAL_CODES[key_ALL]
    # print(train)
    # print(test)
    # print(RIC.keys())

    for train_k in train:
        RIC_train[train_k] = RIC[train_k]
        SC_train[train_k] = SC[train_k]
        SIM_train[train_k] = SIM[train_k]
        STC_train[train_k] = STC[train_k]
        VHC_train[train_k] = VHC[train_k]

    for test_k in test:
        RIC_test[test_k] = RIC[test_k]
        SC_test[test_k] = SC[test_k]
        SIM_test[test_k] = SIM[test_k]
        STC_test[test_k] = STC[test_k]
        VHC_test[test_k] = VHC[test_k]


# print(RIC_train.keys())
# print(RIC_test.keys())
# print(RIC.keys())

# def normalization(data):
#     _range = np.max(data) - np.min(data)
#     if _range == 0:
#         _range = 1
#     return (data - np.min(data)) / _range
#
# # 输入 RIC/SC/SIM/STC/VHC
# def normalize_data(report_FinalScore):
#     for key in report_FinalScore.keys():
#         code_names = list(report_FinalScore[key].keys())
#         scores = np.array(list(report_FinalScore[key].values()))
#         scores = normalization(scores)
#         new_FinalScore = {}
#         for i in range(len(code_names)):
#             new_FinalScore[code_names[i]] = scores[i]
#         report_FinalScore[key] = new_FinalScore


def readModule():
    st = os.path.abspath(os.path.join(os.getcwd(), ".."))
    str_name = "resultFor" + name_of_project
    root = os.path.join(st, str_name)  # 获取路径
    path_of_json = []
    for ro, dir, files in os.walk(root):
        for file in files:
            path_of_json.append(os.path.join(root, file))
    i = 0
    for path_json in path_of_json:
        with open(path_json, 'r', encoding='UTF-8') as f:
            d = json.load(f)
            # (path_json)
        if (i == 0):
            global RIC
            RIC = d
            # print(RIC)
        elif (i == 1):
            global SC
            SC = d
        elif (i == 2):
            global SIM
            SIM = d
        elif (i == 3):
            global STC
            STC = d
        else:
            global VHC
            VHC = d
        i += 1
    # with open("./../../JSON-SWT/JSON-FIXEDFILES-NewSWTBugRepository.json", 'r', encoding='UTF-8') as f:
    global REAL_CODES
    str_of_path_of_rc = "./../../JSON-" + name_of_project + "/JSON-FIXEDFILES-New" + name_of_project + "BugRepository.json"
    with open(str_of_path_of_rc) as f:
        REAL_CODES = json.load(f)
    # 全类名 ----> 类名
    for reportName in REAL_CODES.keys():
        code_list = REAL_CODES[reportName]
        new_code_list = []
        for codeName in code_list:
            new_code_list.append(codeName.split('.')[-2].split('/')[-1])
        REAL_CODES[reportName] = new_code_list


def schaffer(p):
    '''
    二维函数，具有无数个极小值点、强烈的震荡形态。很难找到全局最优值
    在(0,0)处取的最值0
    -10<=x1,x2<=10
    '''
    W1, W2, W3, W4, W5 = p
    for i in range(1):
        report_FinalScore = {}
        for dic1 in RIC_train.keys():
            d = {}
            # print(dic1)
            for dic2 in RIC_train[dic1].keys():
                d[dic2] = W1 * float(RIC[dic1][dic2]) + W2 * float(SC[dic1][dic2]) + W3 * float(
                    SIM[dic1][dic2]) + W4 * float(STC[dic1][dic2]) + W5 * float(VHC[dic1][dic2])

            report_FinalScore[dic1] = d
        for key in report_FinalScore.keys():
            report_FinalScore[key] = sorted(report_FinalScore[key].items(), key=lambda x: x[1], reverse=True)
        MAP = computeMAP(report_FinalScore, REAL_CODES_train)
        MRR = computeMRR(report_FinalScore, REAL_CODES_train)
        TOP = computeTopK(10, report_FinalScore, REAL_CODES_train)
        # print([MAP, MRR])
        # print(math.exp(MAP+MRR))
        # print('========')
        return (-1 * math.exp(MAP+MRR))


def preK(k, computed_codes, real_code):
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
def computeTopK(k, report_FinalScore, real_codes):
    # 命中次数
    shot = 0
    # 判断reportSimilarity的前k个是不是至少含有一个realBugs里面的元素
    for reportName in report_FinalScore.keys():
        # 取computedCodes前K个,即相似度最高的K个,这里不一定能取到k个，注意判断
        topK = report_FinalScore.get(reportName)[0:k]
        real_bug = real_codes.get(reportName)
        for i in range(len(topK)):
            if real_bug.count(topK[i][0]) != 0:
                shot += 1
                break
    return shot / len(report_FinalScore)


# 计算MRR指标
def computeMRR(report_FinalScore, real_codes):
    result = 0
    # 排序后的report_cos列表中第一个是真实的的排名
    for report in report_FinalScore.keys():
        # 一个report对应的所有<codeName,相似度>，此处降序
        computed_codes = report_FinalScore[report]
        # 一个report实际对应的Codes文件名
        real_code = real_codes[report]
        count = 1
        for codeTuple in computed_codes:
            if codeTuple[0] in real_code:
                result += 1 / count
                break
            count += 1
    return result / len(report_FinalScore)


def computeMAP(report_FinalScore, real_codes):
    result = 0
    for report in report_FinalScore.keys():
        # 一个report对应的所有<codeName,相似度>，此处降序
        computed_codes = report_FinalScore[report]
        # 一个report实际对应的Codes文件名
        real_code = real_codes[report]
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
            avgP_j += preK(K_j[i], computed_codes, real_code)
        if len(K_j) != 0:
            avgP_j /= len(K_j)
            result += avgP_j
    return result / len(report_FinalScore)


# 注意：这里report_FinalScore是测试集，real_codes可以是全集，w参数的list，注意顺序是  RIC SC SIM STC VHC
def printMetrics(test, real_codes, w):
    result = {}
    for reportName in test:
        FinalScore = {}
        for codeName in SC[reportName].keys():
            if SC[reportName][codeName] > 0 or SIM[reportName][codeName] > 0:
                FinalScore[codeName] = w[0] * RIC[reportName][codeName] + w[1] * SC[reportName][codeName] + w[2] * \
                                       SIM[reportName][codeName] + w[3] * STC[reportName][codeName] + w[4] * \
                                       VHC[reportName][codeName]
            else:
                FinalScore[codeName] = 0
        result[reportName] = FinalScore
    # FinalScore排序
    for key in result.keys():
        result[key] = sorted(result[key].items(), key=lambda x: x[1], reverse=True)
    with open('./report_FinalScore_aspectj.json', 'w') as file_obj:
        json.dump(result, file_obj)

    print("Top1: " + str(computeTopK(1, result, real_codes)))
    print("Top5: " + str(computeTopK(5, result, real_codes)))
    print("Top10: " + str(computeTopK(10, result, real_codes)))
    print("MRR: " + str(computeMRR(result, real_codes)))
    print("MAP: " + str(computeMAP(result, real_codes)))
    f = open("./result.txt", 'a+', encoding='UTF-8')
    f.write("\nProgram:" + str(name_of_project))
    f.write("\nTop1: " + str(computeTopK(1, result, real_codes)))
    f.write(" Top5:" + str(computeTopK(5, result, real_codes)))
    f.write(" Top10: " + str(computeTopK(10, result, real_codes)))
    f.write("\nMRR: " + str(computeMRR(result, real_codes)))
    f.write(" MAP: " + str(computeMAP(result, real_codes)))
    f.close()
    '''
def change_IC(pop):
    li_of=[]
    for i in range(125):
        li_of.append(1)
    for i in range(1,POP_SIZE):
        for j in range(1,50,5):
            pop[i]=li_of
    return pop
'''


def process_bar(percent, start_str='', end_str='', total_length=0):
    bar = ''
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
    print(bar, end='', flush=True)


if __name__ == "__main__":
    print(time.asctime(time.localtime(time.time())))

    print(
        "please enter a positive integer within 100 to split cases, the number you enter indicates the test set's percentage")
    # n=int(input())
    n = 90
    print(
        "please enter the project number within 3  to indicate program, 0 for SWT , 1 for AspectJ, 2 for eclipse")
    # num_of_project = int(input())
    num_of_project = 0
    if (num_of_project == 0):
        name_of_project = "SWT"
    elif num_of_project == 1:
        name_of_project = "AspectJ"

    elif num_of_project == 2:
        name_of_project = "Eclipse"
    else:
        exit(1)

    readModule()
    split_train(n)  # 输入测试集比例 【0-100】

    # pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 5))  # matrix (POP_SIZE, DNA_SIZE*2)
    # pop=change_IC(pop)
    # print(pop)
    ga = GA(func=schaffer, n_dim=5, size_pop=POP_SIZE, max_iter=200, lb=[0, 0, 0, 0, 0], ub=[1, 1, 1, 1, 1],
            precision=1e-7, prob_mut=0.1)

    ga.register(operator_name='crossover', operator=crossover.crossover_2point). \
        register(operator_name='mutation', operator=mutation.mutation)
    li, k = ga.run()

    # for r in train:
    #     test.append(r)
    # 代表测试集上的real_codes,通过全局REAL_CODES分割而来
    real_codes = {}
    for key in REAL_CODES.keys():
        if key in test:
            real_codes[key] = REAL_CODES[key]
    printMetrics(test, real_codes, list(li))
    for r in train:
        test.append(r)
    printMetrics(test, REAL_CODES, list(li))

    print(time.asctime(time.localtime(time.time())))
