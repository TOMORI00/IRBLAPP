import json
import os.path
import sys

from flask import Flask, request, jsonify

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import database
from webModule import processed
from webModule import CommitLogHandler
from webModule import ReporterHandler
from webModule import GA
from webModule import STC_version_3

app = Flask(__name__)


@app.route('/')
def index():
    return "hello word"


# 查询某一项目的某个reportID的TOP文件
@app.route('/queryfile')  # ?project=swt&reportID=12345
def getFileList():
    project = str(request.args['project'])
    print(project)
    print(getFinalScore(project))
    return getFinalScore(project)


@app.route('/getReport')  # ?project=SWT&reportID=12345
def getReport():
    project = str(request.args['project'])
    reportID = str(request.args['reportID'])
    with open("../JSON-" + project + "/JSON-New" + project + "BugRepository.json", 'r', encoding='utf8')as fp:
        report_dic = json.load(fp)
    ans_dic = {}
    if reportID in report_dic:
        ans_dic[reportID] = report_dic[reportID]
        return jsonify(ans_dic)
    else:
        return "No such report"


@app.route('/upload')  # ?project=SWT&path=C:\\repository\\JSON-Project
def upload():
    project = str(request.args['project'])
    # path = str(request.args['path'])
    rankdic = schedule(project)
    with open("D:\\hard\\report_FinalScore_swt.json", 'r', encoding='utf8')as fp:
        score_dic = json.load(fp)
    score_dic = transform(score_dic)
    ans = {}
    ans["score"] = score_dic
    ans["metric"] = rankdic
    return jsonify(ans)


def getFinalScore(projectName):
    # 这里要根据项目名找到分数（相似度）的json文件
    with open("./rankResult/" + projectName + "/report_FinalScore.json", 'r', encoding='utf8')as fp:
        score_dic = json.load(fp)
    for key in score_dic.keys():
        temList = score_dic[key]
        temList = sorted(temList, key=lambda x: x[1], reverse=True)[:10]
        score_dic[key] = temList
    return jsonify(score_dic)


def schedule(project, path='D://target', TestRatio=95):
    # path ..../JSON-SWT
    # path='/Users/xuyuxuan/Software_engineering/大三下/软工3/backend-irblapp/JSON-SWT'
    # project="SWT"
    # 该路径下包含所有文件 输出文件也都放在这一级目录
    # 预处理
    processorInstance = processed.processor(project, path)
    #     # 预处理结构化信息
    processorInstance.process_sc()
    # #     预处理report&summary和description信息
    processorInstance.process_report()
    # # 五个模块
    # SC
    schedule_SC(project, path)
    # STC
    schedule_STC(project, path)
    # SIM
    schedule_SIM(project, path)
    # RIC
    schedule_RIC(project, path)
    # VHC
    schedule_VHC(project, path)
    # GA
    rankdic = schedule_GA(project, path, TestRatio)
    print("++++")
    print(rankdic)
    return rankdic
    # rankdic = {"top1": "0.34408602150537637", "top5": "0.4731182795698925", "top10": "0.5053763440860215",
    #            "MRR": "0.4065217097984062", "MAP": "0.3184059121227315"}
    # 在这里修改目标数据库地址
    # db = database("172.31.42.10")
    # db.storeProjectRank(project, rankdic)


def schedule_VHC(project, path):
    with open(path + "/" + "JSON-DATE-" + project + "CommitRepository.json", 'r', encoding='utf8')as fp:
        commitdate_dic = json.load(fp)
    with open(path + "/" + "JSON-FIXEDFILES-" + project + "CommitRepository.json", 'r', encoding='gbk')as fp:
        fixfile_dic = json.load(fp)
    with open(path + "/" + "JSON-OPENDATE-New" + project + "BugRepository.json", 'r', encoding='utf8')as fp:
        opendate_dic = json.load(fp)
    with open(path + "/" + "packages.json", 'r', encoding='utf8')as fp:
        file_dic = json.load(fp)
    with open(path + "/" + "JSON-TITLE-" + project + "CommitRepository.json", 'r', encoding='utf8')as fp:
        title_dic = json.load(fp)
    k = 120
    handler = CommitLogHandler.commitLogHandler(opendate_dic, fixfile_dic, commitdate_dic, title_dic, file_dic, k)
    VHC = {}
    for key in opendate_dic:
        VHC[key] = handler.computeWeight(key)
    with open(path + "/" + "VHC_" + project + '.json', 'w') as file_obj:
        json.dump(VHC, file_obj)
    print("commitHandler done")


def schedule_RIC(project, path):
    with open(path + "/" + "JSON-REPORTER-New" + project + "BugRepository.json", 'r', encoding='utf8')as fp:
        reporter_dic = json.load(fp)
    with open(path + "/" + "packages.json", 'r', encoding='utf8')as fp:
        package_dic = json.load(fp)
    with open(path + "/" + "JSON-FIXEDFILES-New" + project + "BugRepository.json", 'r', encoding='utf8')as fp:
        fix_dic = json.load(fp)
    handler = ReporterHandler.reporterHandler(reporter_dic, package_dic, fix_dic)
    RIC = {}
    for key in reporter_dic:
        RIC[key] = handler.computeWeight(key)
    with open(path + "/" + "RIC_" + project + '.json', 'w') as file_obj:
        json.dump(RIC, file_obj)
    print("ReporterHandler done")


def schedule_SIM(project, path):
    Storepath = "D:\\hard\\SC_SWT.json"
    with open(Storepath, encoding='utf-8') as f:
        ans = json.load(f)
    with open(path + '/' + 'SIM_' + project + '.json', 'w') as file_obj:
        json.dump(ans, file_obj)
    print("SIMHandler ok")


def schedule_SC(project, path):
    Storepath = "D:\\hard\\SIM_SWT.json"
    with open(Storepath, encoding='utf-8') as f:
        ans = json.load(f)
    with open(path + '/' + 'SC_' + project + '.json', 'w') as file_obj:
        json.dump(ans, file_obj)


def schedule_STC(project, path):
    with open(path + '/JSON-SUMMARY&DESCRIPTION-New' + project + 'BugRepository.json', encoding='utf-8') as f:
        reports = json.load(f)
    with open(path + '/processedallWords.json', encoding='utf-8') as f:
        codes = json.load(f)
    STC_version_3.StackTraceHandler(project, path, reports, codes)
    print("STCHandler ok")


def schedule_GA(project, path, TestRatio):
    return GA.run(99, path, project)


def transform(dic):
    score_list = []
    for key in dic.keys():
        dic[key] = list((dic[key]).items())[0:10]
    for key in dic.keys():
        temdic = {}
        temdic["report_id"] = str(key)
        temdic["score_list"] = []
        for tp in dic[key]:
            temp = {}
            temp["code_name"] = tp[0]
            temp["score"] = tp[1]
            temdic["score_list"].append(temp)
        score_list.append(temdic)
    return score_list


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9999, threaded=True)
    # print(getFinalScore("SWT"))
    # 这个用于测试 把第二个参数换成自己本地的JSON-SWT路径：
    # schedule("SWT",'/Users/xuyuxuan/Software_engineering/大三下/软工3/backend-irblapp/JSON-SWT')
    # schedule_STC("SWT","/Users/xuyuxuan/Software_engineering/大三下/软工3/backend-irblapp/JSON-SWT")
    # schedule("SWT", path='/Users/xuyuxuan/Software_engineering/大三下/软工3/backend-irblapp/JSON-SWT', TestRatio=95)
    # with open(
    #         "/Users/xuyuxuan/Software_engineering/大三下/软工3/backend-irblapp/JSON-SWT" + '/' + "report_FinalScore_swt.json",
    #         'r', encoding='utf8')as fp:
    #     score_dic = json.load(fp)
    # score_dic = transform(score_dic)
    # print(score_dic)
