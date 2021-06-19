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
from sklearn.model_selection import train_test_split


class Genetic_algorithm:
    def __init__(self, name):
        # 全局变量
        self.DNA_SIZE = 25  # DNA的长度
        self.POP_SIZE = 50  # 种群大小
        self.CROSSOVER_RATE = 0.9  # 交配率
        self.MUTATION_RATE = 0.1  # 突变率
        self.N_GENERATIONS = 200  # generation数
        self.W1_BOUND = [0, 1]  # 权值W1的上下界
        self.W2_BOUND = [0, 1]  # 权值W2的上下界
        self.W3_BOUND = [0, 1]  # 权值W3的上下界
        self.W4_BOUND = [0, 1]  # 权值W4的上下界
        self.W5_BOUND = [0, 1]  # 权值W5的上下界
        self.test = []  # 划分测试集的list
        self.train = []  # 划分训练集的list

        self.RIC = {}  # RIC的字典
        self.SC = {}  # SC的字典
        self.SIM = {}  # SIM的字典
        self.STC = {}  # STC的字典
        self.VHC = {}  # VHC的字典

        self.REAL_CODES = {}  # fixedfiles-bugRepository获取的字典，{id:list}

        self.RIC_test = {}  # RIC在测试集上的自典
        self.SC_test = {}  # SC在测试集上的自典
        self.SIM_test = {}  # SIM在测试集上的自典
        self.STC_test = {}  # STC在测试集上的自典
        self.VHC_test = {}  # VHC在测试集上的自典

        self.RIC_train = {}  # RIC在训练集上的自典
        self.SC_train = {}  # SC在训练集上的自典
        self.SIM_train = {}  # SIM在训练集上的自典
        self.STC_train = {}  # STC在训练集上的自典
        self.VHC_train = {}  # VHC在训练集上的自典

        self.name_of_project = name  # 训练项目的名字
        self.REAL_CODES_train = {}  # fixedfiles-bugRepository获取的字典，训练集上

    # 用于划分测试集和训练集，把字典放入对应的测试集字典和训练集字典上
    def split_train(self, percent):

        num = int(len(self.RIC.keys()) * percent / 100)  # 计算测试集数量

        ALL = self.RIC.copy()
        i = 0
        key_r = random.choice(list(ALL.keys()))  # random 选出测试集
        # print()
        # global test
        # global train
        # global REAL_CODES_train

        # random 选出测试集
        while i != num:
            if key_r not in self.test:
                i += 1
                self.test.append(key_r)
            key_r = random.choice(list(ALL.keys()))

        # 把划分出来的测试集对应的REAL_CODES放入READ_CODES的训练集字典上
        for key_ALL in ALL.keys():
            if key_ALL not in self.test:
                self.train.append(key_ALL)
                self.REAL_CODES_train[key_ALL] = self.REAL_CODES[key_ALL]

        for train_k in self.train:
            self.RIC_train[train_k] = self.RIC[train_k]
            self.SC_train[train_k] = self.SC[train_k]
            self.SIM_train[train_k] = self.SIM[train_k]
            self.STC_train[train_k] = self.STC[train_k]
            self.VHC_train[train_k] = self.VHC[train_k]

        for test_k in self.test:
            self.RIC_test[test_k] = self.RIC[test_k]
            self.SC_test[test_k] = self.SC[test_k]
            self.SIM_test[test_k] = self.SIM[test_k]
            self.STC_test[test_k] = self.STC[test_k]
            self.VHC_test[test_k] = self.VHC[test_k]

    # 输入测试集的比例

    # global RIC_train
    # global RIC_test
    # global SC_test
    # global SC_train
    # global SIM_test
    # global SIM_train
    # global STC_test
    # global STC_train
    # global VHC_test
    # global VHC_train

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

    def readModule(self, path):
        st = os.path.abspath(os.path.join(os.getcwd(), path))
        # print(st)
        # str_name = "resultFor" + self.name_of_project
        root = st  # os.path.join(st, str_name)  # 获取resultforXXX的json文件路径
        path_of_json = []
        for ro, dir, files in os.walk(root):
            for file in files:
                path_of_json.append(os.path.join(root, file))
                if (file[0:3] == "RIC"):
                    path_ = os.path.join(path, file)
                    with open(path_, 'r', encoding='UTF-8') as f:
                        d = json.load(f)
                        self.RIC = d
                elif (file[0:2] == "SC"):
                    path_ = os.path.join(path, file)
                    with open(path_, 'r', encoding='UTF-8') as f:
                        d = json.load(f)
                        self.SC = d
                elif (file[0:3] == "SIM"):
                    path_ = os.path.join(path, file)
                    with open(path_, 'r', encoding='UTF-8') as f:
                        d = json.load(f)
                        self.SIM = d
                elif (file[0:3] == "STC"):
                    path_ = os.path.join(path, file)
                    with open(path_, 'r', encoding='UTF-8') as f:
                        d = json.load(f)
                        self.STC = d
                elif (file[0:3] == "VHC"):
                    path_ = os.path.join(path, file)
                    with open(path_, 'r', encoding='UTF-8') as f:
                        d = json.load(f)
                        self.VHC = d
        # print(self.RIC)
        # with open("./../../JSON-SWT/JSON-FIXEDFILES-NewSWTBugRepository.json", 'r', encoding='UTF-8') as f:
        # 读取JSON-FIXEDFILES-NewXXXBugRepository的json {id：list[文件名]}

        str_of_path_of_rc = path + "/JSON-FIXEDFILES-New" + self.name_of_project + "BugRepository.json"
        # print(str_of_path_of_rc)
        with open(str_of_path_of_rc) as f:
            self.REAL_CODES = json.load(f)
        # 全类名 ----> 类名
        # print(self.REAL_CODES)
        for reportName in self.REAL_CODES.keys():
            code_list = self.REAL_CODES[reportName]
            new_code_list = []
            for codeName in code_list:
                new_code_list.append(codeName.split('.')[-2].split('/')[-1])  # 只需要文件名对应的.java前面的名字
            self.REAL_CODES[reportName] = new_code_list

    def funct(self, w1, w2, w3, w4, w5):
        leng = len(w1)
        OBJ = []
        sum_of_w = w1 + w2 + w3 + w4 + w5

        # 将权值的总和固定为1
        W1 = w1 / sum_of_w
        W2 = w2 / sum_of_w
        W3 = w3 / sum_of_w
        W4 = w4 / sum_of_w
        W5 = w5 / sum_of_w

        for i in range(leng):
            report_FinalScore = {}
            for dic1 in self.RIC_train.keys():
                d = {}
                # print(dic1)
                for dic2 in self.RIC_train[dic1].keys():
                    # 计算分数
                    d[dic2] = W1[i] * float(self.RIC[dic1][dic2]) + W2[i] * float(self.SC[dic1][dic2]) + W3[i] * float(
                        self.SIM[dic1][dic2]) + W4[i] * float(self.STC[dic1][dic2]) + W5[i] * float(
                        self.VHC[dic1][dic2])
                report_FinalScore[dic1] = d
            for key in report_FinalScore.keys():
                report_FinalScore[key] = sorted(report_FinalScore[key].items(), key=lambda x: x[1], reverse=True)
            # 计算指标
            MAP = self.computeMAP(report_FinalScore, self.REAL_CODES_train)
            MRR = self.computeMRR(report_FinalScore, self.REAL_CODES_train)
            # print(MAP,MRR)
            OBJt = math.exp(MAP + MRR)
            OBJ.append(OBJt)
        K = sorted(OBJ)

        return OBJ

    def translateDNA(self, pop):
        # pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目
        w1_pop = pop[:, 0::5]
        w2_pop = pop[:, 1::5]
        w3_pop = pop[:, 2::5]
        w4_pop = pop[:, 3::5]
        w5_pop = pop[:, 4::5]
        # 将权值的转化为50维的list 表示权值
        w1 = w1_pop.dot(2 ** np.arange(self.DNA_SIZE)[::-1]) / float(2 ** self.DNA_SIZE - 1) * (
                self.W1_BOUND[1] - self.W1_BOUND[0]) + \
             self.W1_BOUND[0]
        w2 = w2_pop.dot(2 ** np.arange(self.DNA_SIZE)[::-1]) / float(2 ** self.DNA_SIZE - 1) * (
                self.W2_BOUND[1] - self.W2_BOUND[0]) + \
             self.W2_BOUND[0]
        w3 = w3_pop.dot(2 ** np.arange(self.DNA_SIZE)[::-1]) / float(2 ** self.DNA_SIZE - 1) * (
                self.W3_BOUND[1] - self.W3_BOUND[0]) + \
             self.W3_BOUND[0]
        w4 = w4_pop.dot(2 ** np.arange(self.DNA_SIZE)[::-1]) / float(2 ** self.DNA_SIZE - 1) * (
                self.W4_BOUND[1] - self.W4_BOUND[0]) + \
             self.W4_BOUND[0]
        w5 = w5_pop.dot(2 ** np.arange(self.DNA_SIZE)[::-1]) / float(2 ** self.DNA_SIZE - 1) * (
                self.W5_BOUND[1] - self.W5_BOUND[0]) + \
             self.W5_BOUND[0]

        return w1, w2, w3, w4, w5

    def get_fitness(self, pop):
        w1, w2, w3, w4, w5 = self.translateDNA(pop)  # 获取权值

        pred = self.funct(w1, w2, w3, w4, w5)
        # 减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度
        return (pred - np.min(
            pred) + 1e-3)

        # 交叉和变异

    def crossover_and_mutation(self, pop, CROSSOVER_RATE):
        new_pop = []
        for father in pop:  # 遍历种群中的每一个个体，将该个体作为父亲
            child = father  # 孩子先得到父亲的全部基因（这里我把一串二进制串的那些0，1称为基因）
            if np.random.rand() < self.CROSSOVER_RATE:  # 产生子代时不是必然发生交叉，而是以一定的概率发生交叉
                mother = pop[np.random.randint(self.POP_SIZE)]  # 再种群中选择另一个个体，并将该个体作为母亲
                cross_points = np.random.randint(low=0, high=self.DNA_SIZE * 2)  # 随机产生交叉的点
                child[cross_points:] = mother[cross_points:]  # 孩子得到位于交叉点后的母亲的基因
            self.mutation(child, self.MUTATION_RATE)  # 每个后代有一定的机率发生变异
            new_pop.append(child)

        return new_pop

        # 突变

    def mutation(self, child, MUTATION_RATE):
        if np.random.rand() < self.MUTATION_RATE:  # 以MUTATION_RATE的概率进行变异
            mutate_point = np.random.randint(0, self.DNA_SIZE)  # 随机产生一个实数，代表要变异基因的位置
            child[mutate_point] = child[mutate_point] ^ 1  # 将变异点的二进制为反转

        # 根据适应度来随机选择种群

    def select(self, pop, fitness):
        # nature selection wrt pop's fitness
        idx = np.random.choice(np.arange(self.POP_SIZE), size=self.POP_SIZE, replace=True,
                               p=(fitness) / (fitness.sum()))
        return pop[idx]

    # pop:(POP_SIZE,DNA_SIZE)*(DNA_SIZE,1) --> (POP_SIZE,1)完成解码
    # x = x_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(X_BOUND[1]-X_BOUND[0])+X_BOUND[0]
    # y = y_pop.dot(2**np.arange(DNA_SIZE)[::-1])/float(2**DNA_SIZE-1)*(Y_BOUND[1]-Y_BOUND[0])+Y_BOUND[0]
    # return x,y

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

    def computeTopK(self, k, report_FinalScore, real_codes):
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

    def computeMRR(self, report_FinalScore, real_codes):
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

        # 计算MAP指标

    def computeMAP(self, report_FinalScore, real_codes):
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
                avgP_j += self.preK(K_j[i], computed_codes, real_code)
            if len(K_j) != 0:
                avgP_j /= len(K_j)
                result += avgP_j
        return result / len(report_FinalScore)

    # 注意：这里report_FinalScore是测试集，real_codes可以是全集，w参数的list，注意顺序是  RIC SC SIM STC VHC
    def printMetrics(self,path, test, real_codes, w):
        print("printMetrics(self,path, test, real_codes, w):")
        print(path)
        result = {}
        for reportName in test:
            FinalScore = {}
            for codeName in self.SC[reportName].keys():
                if self.SC[reportName][codeName] > 0 or self.SIM[reportName][codeName] > 0:
                    FinalScore[codeName] = w[0] * self.RIC[reportName][codeName] + w[1] * self.SC[reportName][
                        codeName] + w[2] * \
                                           self.SIM[reportName][codeName] + w[3] * self.STC[reportName][codeName] + w[
                                               4] * \
                                           self.VHC[reportName][codeName]
                else:
                    FinalScore[codeName] = 0
            result[reportName] = FinalScore
        # FinalScore排序
        for key in result.keys():
            result[key] = sorted(result[key].items(), key=lambda x: x[1], reverse=True)

        print("Top1: " + str(self.computeTopK(1, result, real_codes)))
        print("Top5: " + str(self.computeTopK(5, result, real_codes)))
        print("Top10: " + str(self.computeTopK(10, result, real_codes)))
        print("MRR: " + str(self.computeMRR(result, real_codes)))
        print("MAP: " + str(self.computeMAP(result, real_codes)))
        f = open("./result.txt", 'a+', encoding='UTF-8')
        f.write("\nProgram:" + str(self.name_of_project))
        f.write("\nTop1: " + str(self.computeTopK(1, result, real_codes)))
        f.write(" Top5:" + str(self.computeTopK(5, result, real_codes)))
        f.write(" Top10: " + str(self.computeTopK(10, result, real_codes)))
        f.write("\nMRR: " + str(self.computeMRR(result, real_codes)))
        f.write(" MAP: " + str(self.computeMAP(result, real_codes)))
        f.close()
        re = {}
        re["top1"] = str(self.computeTopK(1, result, real_codes))
        re["top5"] = str(self.computeTopK(5, result, real_codes))
        re["top10"] = str(self.computeTopK(10, result, real_codes))
        re["MRR"] = str(self.computeMRR(result, real_codes))
        re["MAP"] = str(self.computeMAP(result, real_codes))
        for report in result.keys():
            FinalScore = dict(result[report])
            result[report] = FinalScore
        with open(path+'/report_FinalScore_swt.json', 'w') as file_obj:
            json.dump(result, file_obj)
        return re

        # 改变染色体的 初始种群

    def change_IC(self, pop):
        li_of = []
        for i in range(7):
            li_of.append(0)
            li_of.append(1)
            li_of.append(1)
            li_of.append(1)
            li_of.append(1)
        for i in range(18):
            li_of.append(0)
            li_of.append(1)
            li_of.append(0)
            li_of.append(0)
            li_of.append(0)

        for i in range(0, 50):
            pop[i] = li_of

        return pop

        # 处理进度的进度bar

    def process_bar(self, percent, start_str='', end_str='', total_length=0):
        bar = ''
        bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent * 100) + end_str
        print(bar, end='', flush=True)


# n测试集比例 【0-100】
# path resultForXXX的路径
# name_of_project 文件名 SWT/Eclipse/AspectJ
def run(n, path, name_of_project):
    handler = Genetic_algorithm(name_of_project)
    print(time.asctime(time.localtime(time.time())))
    f = open("./result.txt", 'a+', encoding='UTF-8')
    f.write(name_of_project)
    f.close()
    handler.readModule(path)
    handler.split_train(n)  # 输入测试集比例 【0-100】
    pop = np.random.randint(2, size=(handler.POP_SIZE, handler.DNA_SIZE * 5))  # matrix (POP_SIZE, DNA_SIZE*2)
    # 初始化种群 干涉初值
    pop = handler.change_IC(pop)

    # 训练N_Generation
    for i in range(handler.N_GENERATIONS):
        w1, w2, w3, w4, w5 = handler.translateDNA(pop)
        end_str = '100%'
        handler.process_bar(i / 200, start_str='', end_str=end_str, total_length=15)
        # 交叉和变异
        pop = np.array(handler.crossover_and_mutation(pop, handler.CROSSOVER_RATE))
        # 获取适应度
        fitness = handler.get_fitness(pop)
        # 自然选择
        pop = handler.select(pop, fitness)
    fitness = handler.get_fitness(pop)
    max_fitness_index = np.argmax(fitness)
    print("max_fitness:", fitness[max_fitness_index])
    w1, w2, w3, w4, w5 = handler.translateDNA(pop)
    print("最优的基因型：", pop[max_fitness_index])

    sum_of_w = w1[max_fitness_index] + w2[max_fitness_index] + w3[max_fitness_index] + w4[max_fitness_index] + \
               w5[
                   max_fitness_index]
    W1, W2, W3, W4, W5 = w1[max_fitness_index] / sum_of_w, w2[max_fitness_index] / sum_of_w, w3[
        max_fitness_index] / sum_of_w, w4[max_fitness_index] / sum_of_w, w5[max_fitness_index] / sum_of_w,

    print("(w1, w2, w3, w4, w5):", (W1, W2, W3, W4, W5))

    # 结果记录到result.txt里
    f = open("./result.txt", 'a+', encoding='UTF-8')
    f.write("\n\ntime: " + str(time.time()))
    f.write("\nsplit:" + str(n))
    # f.write(str(max_fitness_index))
    # f.write("\nw1=" + str(w1) + "\nw2=" + str(w2) + "\nw3=" + str(w3) + "\nw4=" + str(w4) + "\nw5=" + str(w5))
    f.write("\npop[max_fitness_index]:" + str(pop[max_fitness_index]))
    f.write("\n(w1, w2, w3, w4, w5):" + str((W1, W2, W3, W4, W5)))
    f.close()
    # for r in train:
    #     test.append(r)

    # 代表测试集上的real_codes,通过全局REAL_CODES分割而来
    real_codes = {}
    for key in handler.REAL_CODES.keys():
        if key in handler.test:
            real_codes[key] = handler.REAL_CODES[key]
    return_val = handler.printMetrics(path,handler.test, real_codes, [W1, W2, W3, W4, W5])
    f.close()
    print(time.asctime(time.localtime(time.time())))
    return return_val


if __name__ == "__main__":
    print(run(95, "C:/Users/11159/Desktop/SE3/backend-irblapp/JSON-SWT", "SWT"))
    # print(run(95, "..", "Eclipse"))
    # print(run(95, "..", "AspectJ"))
    '''
    print(time.asctime( time.localtime(time.time()) ))


    #print("please enter a positive integer within 100 to split cases, the number you enter indicates the test set's percentage")
    #n=int(input())
    n=90  #输入测试集的比例
    #print(
    #    "please enter the project number within 3  to indicate program, 0 for SWT , 1 for AspectJ, 2 for eclipse")
    #num_of_project = int(input())

    #指代project
    num_of_project=0
    if(num_of_project==0):
        name_of_project="SWT"
    elif num_of_project==1:
        name_of_project="AspectJ"

    elif num_of_project==2:
        name_of_project="Eclipse"
    else:
        exit(1)

    #记录文件名
    f = open("./result.txt", 'a+', encoding='UTF-8')
    f.write(name_of_project)
    f.close()
    readModule()
    split_train(n)#输入测试集比例 【0-100】

    '''

    '''
    real_codes = {}
    for key in REAL_CODES.keys():

        real_codes[key] = REAL_CODES[key]
    test.extend(train)
    printMetrics(test, real_codes, [6.786071150934917E-4, 2.5717160226394697E-5, 0.9981898769028404, 6.435016414460524E-5, 0.0010414486576951472])
'''
    '''
    #随机生成种群pop
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 5))  # matrix (POP_SIZE, DNA_SIZE*2)
    #初始化种群 干涉初值
    pop=change_IC(pop)

    #训练N_Generation
    for i in range(N_GENERATIONS):
        w1, w2, w3, w4, w5 = translateDNA(pop)
        end_str = '100%'
        process_bar(i / 200, start_str='', end_str=end_str, total_length=15)
        #交叉和变异
        pop = np.array(crossover_and_mutation(pop, CROSSOVER_RATE))
        #获取适应度
        fitness = get_fitness(pop)
        #自然选择
        pop = select(pop, fitness)
    fitness = get_fitness(pop)
    max_fitness_index = np.argmax(fitness)
    print("max_fitness:", fitness[max_fitness_index])
    w1, w2, w3, w4, w5 = translateDNA(pop)
    print("最优的基因型：", pop[max_fitness_index])


    sum_of_w = w1[max_fitness_index] + w2[max_fitness_index] + w3[max_fitness_index] + w4[max_fitness_index] + w5[
        max_fitness_index]
    W1, W2, W3, W4, W5 = w1[max_fitness_index] / sum_of_w, w2[max_fitness_index] / sum_of_w, w3[
        max_fitness_index] / sum_of_w, w4[max_fitness_index] / sum_of_w, w5[max_fitness_index] / sum_of_w,

    print("(w1, w2, w3, w4, w5):", (W1, W2, W3, W4, W5))

    #结果记录到result.txt里
    f = open("./result.txt", 'a+', encoding='UTF-8')
    f.write("\n\ntime: "+str(time.time()))
    f.write("\nsplit:" +str(n))
    #f.write(str(max_fitness_index))
    #f.write("\nw1=" + str(w1) + "\nw2=" + str(w2) + "\nw3=" + str(w3) + "\nw4=" + str(w4) + "\nw5=" + str(w5))
    f.write("\npop[max_fitness_index]:" + str(pop[max_fitness_index]))
    f.write("\n(w1, w2, w3, w4, w5):" + str((W1, W2, W3, W4, W5)))
    f.close()
    # for r in train:
    #     test.append(r)



    # 代表测试集上的real_codes,通过全局REAL_CODES分割而来
    real_codes = {}
    for key in REAL_CODES.keys():
        if key in test:
            real_codes[key] = REAL_CODES[key]
    printMetrics(test, real_codes, [W1, W2, W3, W4, W5])
    f.close()
    print(time.asctime( time.localtime(time.time()) ))

'''