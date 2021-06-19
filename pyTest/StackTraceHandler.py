import copy
import re
from collections import OrderedDict
import datetime
import numpy as np

# todo 改进:只要出现文件名就计算得分
# todo 判断：rank是stack trace从上到下还是从下到上
# todo 改进：org/a/b/c 加上判断
from loadModule_aspectj import LoadModule
import json


class StackTraceHandler:
    def __init__(self):
        # reportName:{code:score}
        self.stack_scores = {}
        # 加载reports和codes
        self.loadModule = LoadModule()
        self.reports = self.loadModule.read_origin_reports()
        self.codes = self.loadModule.read_codes()
        self.zero_vector = OrderedDict((token, 0) for token in self.codes.keys())

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
                    stack_score[file_list[j]] = 1 / (j + 1)
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
        return stack_score


if __name__ == '__main__':
    print(datetime.datetime.now())
    sth = StackTraceHandler()
    stack_scores = sth.get_stack_scores()
    # with open('./resultForEclipse/STC_Eclipse.json', 'w') as file_obj:
    with open('./resultForAspectJ/STC_AspectJ.json', 'w') as file_obj:
        json.dump(stack_scores, file_obj)
    print(datetime.datetime.now())
