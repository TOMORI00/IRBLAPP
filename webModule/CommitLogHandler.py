# TODO
# 1.判断title是否满足.*fix.*|.*bug.*的函数
# =>筛选出可以使用的commitLog
# 对于每一个bugReport
# 2.选出opendate前K天的commitLog（可能不存在）
# =>需要能判断时间的函数
# 3.同时要求选出来的commitLog的fixfiles包括该report中的file
import math
from datetime import datetime, date
import json
import re
class commitLogHandler:
    def __init__(self,opendate_dic,fixfile_dic,commitdate_dic,title_dic,file_dic,k):
        self.opendate_dic=opendate_dic
        self.fixfile_dic=fixfile_dic
        self.commitdate_dic=commitdate_dic
        self.title_dic=title_dic
        self.file_dic=file_dic
        self.k=k
    def getElapsedDays(self,time_1,time_2):
        # return Tc
        #time2>time1
        # time1 "%Y-%m-%d"
        # time2 "%Y-%m-%d %H:%M:%S"
        # time_1 = '2004-10-07 01:02:22'
        # time_2 = '2004-10-12'
        time_1_struct = datetime.strptime(time_1, "%Y-%m-%d")
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        day = total_seconds/60/60/24
        return day
    def computeWeight(self,bugID):
        # 过滤得到符合条件的commit
        bugID=str(bugID)
        bugOpenDate=self.opendate_dic[bugID] #"%Y-%m-%d %H:%M:%S"
        # relevantCommit key:commitID value:Tc（这条commit和这条report之间的日子差）
        relevantCommit=self.getRelevantCommit(bugOpenDate)
        # 下面要计算所有出现在commit的fixlist中且出现在file集合中的文件的score了
        # 首先建立所有file名为key的字典
        # 这里利用file_dic TODO 后期改进
        ans={}
        for key in self.file_dic:
            ans[key]=0
        # 下面解析revelentCommit修复的java file
        for commitID in relevantCommit:
            fixlist=self.fixfile_dic[commitID]# ['../../a.java','../../s.cpp']
            for fixfile in fixlist:
                fileName=self.getFileName(fixfile)#['a','no such file']
                if fileName in ans.keys():
                    # compute file
                    ans[fileName]+=self.getScore(relevantCommit[commitID])
                    # print(bugID+":"+str(ans[fileName]))
        return ans
    def getRelevantCommit(self,bugOpenDate):
        # ans key：commitID value：Tc
        ans={}
        # TODO 查找相关commit算法可以优化
        # 现在是遍历查找
        for key in self.commitdate_dic:
            # bugOpendate>commitdate
            day=self.getElapsedDays(self.commitdate_dic[key],bugOpenDate)
            # 相关的两个条件
            # 1.时间上小于k天
            if 0<day<self.k:
                # 2.内容上与fix和bug相关
                # 则加入字典
                if self.isBugFix(self.title_dic[key]):
                    ans[key]=day
        return ans
    def isBugFix(self,expression):
        if re.match(".*bug.*|.*fix.*|.*issue.*|.*fail.*|.*error.*",expression.lower())!=None:
            return True
        return False
    def getFileName(self,longName):
        # 首先要判断是不是.java结尾
        if not longName.endswith(".java"):
            return "no such file"
        longName=longName[:-5]
        index=longName.rindex('/')+1 # swt eclipse
        # index=longName.rindex('.')+1
        fileName=longName[index:]
        return fileName
    def getScore(self,tc):
        return 1.0/(1+(math.exp(12*(1-((self.k-tc)/self.k)))))

if __name__ == '__main__':
    with open("./../JSON-SWT/JSON-DATE-SWTCommitRepository.json",'r',encoding='utf8')as fp:
        commitdate_dic = json.load(fp)
    with open("./../JSON-SWT/JSON-FIXEDFILES-SWTCommitRepository.json",'r',encoding='utf8')as fp:
        fixfile_dic = json.load(fp)
    with open("./../JSON-SWT/JSON-OPENDATE-NewSWTBugRepository.json",'r',encoding='utf8')as fp:
        opendate_dic= json.load(fp)
    with open("./../JSON-SWT/packages.json",'r',encoding='utf8')as fp:
        file_dic = json.load(fp)
    with open("./../JSON-SWT/JSON-TITLE-SWTCommitRepository.json",'r',encoding='utf8')as fp:
        title_dic = json.load(fp)
    k=120
    handler=commitLogHandler(opendate_dic,fixfile_dic,commitdate_dic,title_dic,file_dic,k)
    VHC_SWT={}
    for key in opendate_dic:
        VHC_SWT[key]=handler.computeWeight(key)
    with open('./resultForSWT/VHC_SWT.json', 'w') as file_obj:
        json.dump(VHC_SWT, file_obj)
    print("done")

    # with open("./../JSON-AspectJ/JSON-DATE-AspectJCommitRepository.json",'r',encoding='utf8')as fp:
    #     commitdate_dic = json.load(fp)
    # with open("./../JSON-AspectJ/JSON-FIXEDFILES-AspectJCommitRepository.json",'r',encoding='utf8')as fp:
    #     fixfile_dic = json.load(fp)
    # with open("./../JSON-AspectJ/JSON-OPENDATE-NewAspectJBugRepository.json",'r',encoding='utf8')as fp:
    #     opendate_dic= json.load(fp)
    # with open("./../JSON-AspectJ/packages.json",'r',encoding='utf8')as fp:
    #     file_dic = json.load(fp)
    # with open("./../JSON-AspectJ/JSON-TITLE-AspectJCommitRepository.json",'r',encoding='utf8')as fp:
    #     title_dic = json.load(fp)
    # k=15
    # handler=commitLogHandler(opendate_dic,fixfile_dic,commitdate_dic,title_dic,file_dic,k)
    # VHC_SWT={}
    # for key in opendate_dic:
    #     VHC_SWT[key]=handler.computeWeight(key)
    # with open('./resultForAspectJ/VHC_AspectJ.json', 'w') as file_obj:
    #     json.dump(VHC_SWT, file_obj)
    # print("done")

    # with open("./../JSON-Eclipse/JSON-DATE-EclipseCommitRepository.json",'r',encoding='utf8')as fp:
    #     commitdate_dic = json.load(fp)
    # with open("./../JSON-Eclipse/JSON-FIXEDFILES-EclipseCommitRepository.json",'r',encoding='utf8')as fp:
    #     fixfile_dic = json.load(fp)
    # with open("./../JSON-Eclipse/JSON-OPENDATE-NewEclipseBugRepository.json",'r',encoding='utf8')as fp:
    #     opendate_dic= json.load(fp)
    # with open("./../JSON-Eclipse/packages.json",'r',encoding='utf8')as fp:
    #     file_dic = json.load(fp)
    # with open("./../JSON-Eclipse/JSON-TITLE-EclipseCommitRepository.json",'r',encoding='utf8')as fp:
    #     title_dic = json.load(fp)
    # k=15
    # handler=commitLogHandler(opendate_dic,fixfile_dic,commitdate_dic,title_dic,file_dic,k)
    # # print(handler.computeWeight(80522))
    # VHC_Eclipse={}
    # for key in opendate_dic:
    #     VHC_Eclipse[key]=handler.computeWeight(key)
    # output = open("resultForEclipse/VHC_Eclipse.json", 'w', encoding='utf-8')
    # json.dump(VHC_Eclipse, output, ensure_ascii=False)
    # print("done")