import copy
import re
from collections import OrderedDict
import datetime

# todo 改进:只要出现文件名就计算得分
# todo 判断：rank是stack trace从上到下还是从下到上
# todo 改进：org/a/b/c 加上判断
import numpy as np
from loadModule_swt import LoadModule
import json

def normalization(data):
    _range = np.max(data) - np.min(data)
    if _range == 0:
        _range = 1
    return (data - np.min(data)) / _range


# 输入 RIC/SC/SIM/STC/VHC
def normalize_data(report_FinalScore):
    scores = np.array(list(report_FinalScore.values()))
    scores = normalization(scores)
    for i,key in enumerate(report_FinalScore.keys()):
        report_FinalScore[key] = scores[i]

# 用于存储图
class Graph():
    def __init__(self):
        self.linked_node_map = {}  # 邻接表，
        self.PR_map = {}  # 存储每个节点的入度

    # 添加节点
    def add_node(self, node_id):
        if node_id not in self.linked_node_map:
            self.linked_node_map[node_id] = set({})
            self.PR_map[node_id] = 0
        else:
            print("这个节点已经存在")

    # 增加一个从Node1指向node2的边。允许添加新节点
    def add_link(self, node1, node2):
        if node1 not in self.linked_node_map:
            self.add_node(node1)
        if node2 not in self.linked_node_map:
            self.add_node(node2)
        self.linked_node_map[node1].add(node2)  # 为node1添加一个邻接节点，表示ndoe2引用了node1

    # 计算pr
    def get_PR(self, epoch_num=10, d=0.5):  # 配置迭代轮数，以及阻尼系数
        for i in range(epoch_num):
            for node in self.PR_map:  # 遍历每一个节点
                self.PR_map[node] = (1 - d) + d * sum(
                    [self.PR_map[temp_node] for temp_node in self.linked_node_map[node]])  # 原始版公式
            print(self.PR_map)
            return self.PR_map


class StackTraceHandler:
    def __init__(self):
        # reportName:{code:score}
        self.stack_scores = {}
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_origin_reports()
        self.codes = self.loadModule.read_codes()
        self.imports = self.loadModule.read_imports()
        self.packages = self.loadModule.read_packages()
        self.call_graph = self.loadModule.read_call_graph()
        self.zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())

    def get_stack_scores(self):
        """
        计算所有stack_score
        :return: None
        """
        # 对每一个文件获取所有stack信息，并计算score_list
        for reportName in self.reports.keys():
            # 存放结果的one-hot向量，和每一个source code分数初始化为0
            stack_score = copy.copy(self.zero_vector)
            stacks = re.findall(r'at [^()]+\([^()]+.java:[0-9]*[)]', self.reports[reportName])
            # 计算每一个report的description中出现在的stack trace中的java文件的score
            # {code:score}
            file_list = []
            for j in range(len(stacks)):
                # 获取文件名,添加到file_list中
                # 原本是 at xxx.xxx.xxx.a.b(a.java:123) ,要的是a
                fileName = stacks[j].split('(')[1].split(':')[0].split('.')[0]
                if fileName not in file_list:
                    file_list.append(fileName)
            # 计算score a b c
            for j in range(len(file_list)):
                if file_list[j] in self.codes.keys():
                    if j <= 10:
                        stack_score[file_list[j]] += 1.0 / (j + 1)
                    else:
                        stack_score[file_list[j]] += 0.1
            # stacktrace中类调用的的类pagerank
            graph = Graph()
            edges = []
            node_index = {}
            node_index_inverse = {}
            count = 1
            # 构建node索引
            for node in set(self.call_graph.keys()):
                if node not in node_index.keys():
                    node_index[node] = count
                    count += 1
            for node in set(self.call_graph.values()):
                if node not in node_index.keys():
                    node_index[node] = count
                    count += 1
            for key in self.call_graph.keys():
                edge = [node_index[key],node_index[self.call_graph[key]]]
                edges.append(edge)

            for edge in edges:
                graph.add_link(edge[0], edge[1])
            pagerank_score = graph.get_PR()
            normalize_data(pagerank_score)

            # todo 考虑标签传播
            # 第一层找到的文件再根据引用关系去分配权重，传播权重
            for file in self.call_graph.keys():
                call_classes = self.call_graph[file].split(' ')
                for call_class in call_classes:
                    if call_class in self.codes.keys() and call_class in node_index.keys():
                        stack_score[call_class] += pagerank_score[node_index[call_class]]
            self.stack_scores[reportName] = stack_score
        return self.stack_scores



    def get_new_stack_score(self, new_report):
        """
        为新来的bug report计算stack_score
        :param new_report: 新的bug report {reportName:content}
        :return: None
        """
        # 获取内容
        reportName = ''
        content = ''
        for key in new_report.keys():
            reportName += key
            content += new_report[key]
        # 找所有stack trace
        stacks = re.findall(r'at [^()]+\([^()]+.java:[0-9]*[)]', content)
        # 计算每一个report的description中出现在的stack trace中的java文件的score
        # {code:score}
        stack_score = {}
        file_list = []
        for j in range(len(stacks)):
            # 获取文件名,添加到file_list中
            # 原本是 at xxx.xxx.xxx.a.b(a.java:123) ,要的是xxx.xxx.xxx.a.java
            fileName = stacks[j].split('(')[1].split(':')[0].split('.')[0]
            if fileName not in file_list:
                file_list.append(fileName)
        # 计算score
        for j in range(len(file_list)):
            if file_list[j] in self.codes.keys():
                stack_score[file_list[j]] = 1 / (j + 1)
        self.stack_scores[reportName] = stack_score

        # import 信息
        import_files = []
        for file in file_list:
            import_files = self.imports[file].split(' ')
        for i in range(len(import_files)):
            import_files[i] = import_files[i].split('.')[-2]
        for import_file in import_files:
            if import_file in self.codes.keys():
                stack_score[import_file] = 0.1
        self.stack_scores[reportName] = stack_score
        return stack_score



if __name__ == '__main__':
    print(datetime.datetime.now())
    sth = StackTraceHandler()
    stack_scores = sth.get_stack_scores()

    with open('STC_version_3.json', 'w') as file_obj:
        json.dump(stack_scores, file_obj)
    print(datetime.datetime.now())
