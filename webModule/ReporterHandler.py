import json
# reporterHandler接受一个bug report信息，返回一个source code list
# 1. Find past bug reports that are submitted by r.
#
# 2. Extract the names of the buggy ﬁles that are modiﬁed to ﬁx the past bugs.
#
# 3. Extract the names of packages (denoted as r. P) that contain the buggy ﬁles.
#
# 4. Calculate the suspiciousness score of a ﬁle f following Equation (6).
class reporterHandler:
    # result={}
    def __init__(self,reporter_dic,package_dic,fix_dic):
        self.reporter_dic=reporter_dic
        self.package_dic=package_dic
        self.fix_dic=fix_dic
    def computeWeight(self,bugID):
        bugID=str(bugID)
        result={}
        for key in self.package_dic:
            result[key]=0
        # 默认所有的输入bug report信息都是已经有的
        reporterName=self.reporter_dic[bugID]
        # print(reporterName)
        # 获得该reporter所提交的所有bug reportID
        # 不包括该report的信息
        bugList=[]
        for key in self.reporter_dic:
            if self.reporter_dic[key]==reporterName and key!=bugID:
                bugList.append(key)
        # print(bugList)
        # 将涉及到的fixed file的包记录下来
        packageSet=set()
        for bugID in bugList:
            #求并集
            packageSet=packageSet | self.getPackage(bugID)
        # print(packageSet)
        # 所有文件，只要是所属package在packageset就为1
        for key in result:
            # 这里也要处理一下package_dic[key]可能出现的拼接情况
            temarr=str(self.package_dic[key]).split(" ")
            temarr=set(temarr)
            for pkg in temarr:
                if pkg in packageSet:
                    result[key]=1
                    # print(bugID+":"+key)
        return result

    def getPackage(self,bugID):
        # 输入bugID
        # 返回fixedList对应的package
        # 获取修复文件列表
        bugID=str(bugID)
        fixedFilesList=self.fix_dic[bugID]
        # 根据文件名返回包名,首先将全类型名转换为文件名
        fixedFilesList=[self.getFileName(i) for i in fixedFilesList]
        packages=set()
        for file in fixedFilesList:
            # 判断当前file是否在sourcefile中
            if file in self.package_dic.keys():
                # 判断package_dic[file]的package格式是否是"package1 package2"格式
                temarr=str(self.package_dic[file]).split(" ")
                temarr=set(temarr)
                for pkg in temarr:
                    packages.add(pkg)
        return packages

    def getFileName(self,longName):
        # print(longName)
        longName=longName[:-5]
        if(longName.find('.')==-1): #swt
        # if(longName.find('/')==-1): #aj
            # print(longName)
            return longName
        # index=longName.rindex('/')+1
        index=longName.rindex('.')+1
        fileName=longName[index:]
        return fileName


if __name__ == '__main__':
    # with open("./data/JSON-REPORTER-NewSWTBugRepository.json",'r',encoding='utf8')as fp:
    # with open("./../JSON-SWT/JSON-REPORTER-NewSWTBugRepository.json",'r',encoding='utf8')as fp:
    #     reporter_dic = json.load(fp)
    # with open("./../JSON-SWT/packages.json",'r',encoding='utf8')as fp:
    #     package_dic = json.load(fp)
    # with open("./../JSON-SWT/JSON-FIXEDFILES-NewSWTBugRepository.json",'r',encoding='utf8')as fp:
    #     fix_dic = json.load(fp)
    # handler = reporterHandler(reporter_dic,package_dic,fix_dic)
    # RIC_SWT={}
    # for key in reporter_dic:
    #     RIC_SWT[key]=handler.computeWeight(key)
    # output = open("./resultForSWT/RIC_SWT.json", 'w', encoding='utf-8')
    # json.dump(RIC_SWT, output, ensure_ascii=False)
    # print("done")

    with open("./../JSON-AspectJ/JSON-REPORTER-NewAspectJBugRepository.json",'r',encoding='utf8')as fp:
        reporter_dic = json.load(fp)
    with open("./../JSON-AspectJ/packages.json",'r',encoding='utf8')as fp:
        package_dic = json.load(fp)
    with open("./../JSON-AspectJ/JSON-FIXEDFILES-NewAspectJBugRepository.json",'r',encoding='utf8')as fp:
        fix_dic = json.load(fp)
    handler = reporterHandler(reporter_dic,package_dic,fix_dic)
    RIC={}
    for key in reporter_dic:
        RIC[key]=handler.computeWeight(key)
    with open('./resultForAspectJ/RIC_AspectJ.json', 'w') as file_obj:
        json.dump(RIC, file_obj)
    print("done")

    # with open("./../JSON-Eclipse/JSON-REPORTER-NewEclipseBugRepository.json",'r',encoding='utf8')as fp:
    #     reporter_dic = json.load(fp)
    # with open("./../JSON-Eclipse/packages.json",'r',encoding='utf8')as fp:
    #     package_dic = json.load(fp)
    # with open("./../JSON-Eclipse/JSON-FIXEDFILES-NewEclipseBugRepository.json",'r',encoding='utf8')as fp:
    #     fix_dic = json.load(fp)
    # handler = reporterHandler(reporter_dic,package_dic,fix_dic)
    # # handler.computeWeight(94907)
    # RIC_SWT={}
    # for key in reporter_dic:
    #     RIC_SWT[key]=handler.computeWeight(key)
    # output = open("./resultForEclipse/RIC_Eclipse.json", 'w', encoding='utf-8')
    # json.dump(RIC_SWT, output, ensure_ascii=False)
    # print("done")




