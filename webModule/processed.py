from . import filter

import json
class processor:
    def __init__(self,project,path):
        self.path=path+'/'
        self.project=project
    def process_sc(self):
        dataName = ["allWords.json", "attributes.json", "classes.json", "comments.json", "methods.json"]
        for data in dataName:
            with open(self.path + data, 'r', encoding='utf8')as fp:
                java_dic = json.load(fp)
            for key in java_dic:
                tem = []
                tem.append(java_dic[key])
                java_dic[key] = tem
            java_dic = filter.Filter().splitWords(java_dic)
            output = open(self.path + "/processed" + data, 'w', encoding='utf-8')
            json.dump(java_dic, output, ensure_ascii=False)
            output.close()
            print(self.path + data + "  ok")
    def process_report(self):
        dataName=["JSON-SUMMARY-New"+self.project+"BugRepository.json","JSON-DESCRIPTION-New"+self.project+"BugRepository.json","JSON-SUMMARY&DESCRIPTION-New"+self.project+"BugRepository.json"]
        for data in dataName:
            with open(self.path+data,'r',encoding='utf8')as fp:
                java_dic = json.load(fp)
            for key in java_dic:
                tem = []
                tem.append(java_dic[key])
                java_dic[key] = tem
            java_dic = filter.Filter().splitWords(java_dic)
            if data=="JSON-SUMMARY-New"+self.project+"BugRepository.json":
                output = open(self.path+self.project+"_Summary.json", 'w', encoding='utf-8')
            elif data=="JSON-DESCRIPTION-New"+self.project+"BugRepository.json":
                output = open(self.path+self.project+"_Description.json", 'w', encoding='utf-8')
            else:
                output = open(self.path+self.project+"_SummaryAndDescription.json", 'w', encoding='utf-8')
            json.dump(java_dic, output, ensure_ascii=False)
            output.close()
            print(self.path+ data + "  ok")

if __name__ == '__main__':
    dataName=["allWords.json","attributes.json","classes.json","comments.json","methods.json"]
    pathName=["./resultsOfAST/swt-3.1/","./resultsOfAST/aspectj-RB_V152/","./resultsOfAST/eclipse-3.1/"]
    for path in pathName:
        for data in dataName:
            with open(path+data,'r',encoding='utf8')as fp:
                java_dic = json.load(fp)
            for key in java_dic:
                tem = []
                tem.append(java_dic[key])
                java_dic[key] = tem
            java_dic = filter.Filter().splitWords(java_dic)
            output = open(path+"processed"+data, 'w', encoding='utf-8')
            json.dump(java_dic, output, ensure_ascii=False)
            output.close()
            print(path+data+"  ok")

        # with open("/Users/xuyuxuan/Software_engineering/大三下/软工3/backend-irblapp/JSON-Eclipse/JSON-SUMMARY&DESCRIPTION-NewEclipseBugRepository.json",'r',encoding='utf8')as fp:
        #     java_dic = json.load(fp)
        # for key in java_dic:
        #     tem = []
        #     tem.append(java_dic[key])
        #     java_dic[key] = tem
        # java_dic = Filter().splitWords(java_dic)
        # output = open("Eclipse_SummaryAndDescription.json", 'w', encoding='utf-8')
        # # output = open("Eclipse_Description.json", 'w', encoding='utf-8')
        # # output = open("Eclipse_Summary.json", 'w', encoding='utf-8')
        # json.dump(java_dic, output, ensure_ascii=False)
        # output.close()
        # print("ok")
