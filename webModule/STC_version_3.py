import copy
import re
from collections import OrderedDict
import datetime

# todo 改进:只要出现文件名就计算得分
# todo 判断：rank是stack trace从上到下还是从下到上
# todo 改进：org/a/b/c 加上判断
import json


class StackTraceHandler:
    def __init__(self,project,path,reports,codes):
        # reportName:{code:score}
        self.codes=codes
        self.reports=reports
        self.project = project
        self.path = path
        self.stack_scores = {}
        self.zero_vector = OrderedDict((token, 0.0) for token in self.codes.keys())
        # 加载reports和codes
        result = self.get_stack_scores()
        with open(self.path+'/'+'STC_'+project+'.json', 'w') as file_obj:
            json.dump(result, file_obj)


    def get_stack_scores(self):
        """
        计算所有stack_score
        :return: None
        """
        # 对每一个文件获取所有stack信息，并计算score_list
        for reportName in self.reports.keys():
            # 存放结果的one-hot向量，和每一个source code分数初始化为0
            stack_score = copy.copy(self.zero_vector)
            stacks = re.findall(r'at[\n]* [^()]+\([^()]+.java:[0-9]*[)]', self.reports[reportName])
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
            # stacktrace中类调用的的类
            # todo 考虑标签传播
            # 第一层找到的文件再根据引用关系去分配权重，传播权重
            # layer1 = []
            # for file in file_list:
            #     if file in self.call_graph.keys():
            #         call_classes = self.call_graph[file].split(' ')
            #         for call_class in call_classes:
            #             if call_class in self.codes.keys():
            #                 stack_score[call_class] += 0.1
                            # layer1.append(call_class)
            # for file in layer1:
            #     if file in self.call_graph.keys():
            #         call_classes = self.call_graph[file].split(' ')
            #         for call_class in call_classes:
            #             if call_class in self.codes.keys():
            #                 stack_score[call_class] += 0.1

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



# if __name__ == '__main__':
    # print(datetime.datetime.now())
    # sth = StackTraceHandler(project,path)
    # stack_scores = sth.get_stack_scores()
    # with open('+STC_AspectJ.json', 'w') as file_obj:
    #     json.dump(stack_scores, file_obj)
    # print(datetime.datetime.now())
