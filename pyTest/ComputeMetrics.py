import json
import re

import numpy as np
import pymongo
from loadModule_swt import LoadModule


def normalization(data):
    _range = np.max(data) - np.min(data)
    if _range == 0:
        _range = 1
    return (data - np.min(data)) / _range


# 输入 RIC/SC/SIM/STC/VHC
def normalize_data(report_FinalScore):
    for key in report_FinalScore.keys():
        code_names = list(report_FinalScore[key].keys())
        scores = np.array(list(report_FinalScore[key].values()))
        scores = normalization(scores)
        new_FinalScore = {}
        for i in range(len(code_names)):
            new_FinalScore[code_names[i]] = scores[i]
        report_FinalScore[key] = new_FinalScore


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


def TopK(report_FinalScore, real_codes):
    # 命中次数
    shot = [0, 0, 0]
    # 判断reportSimilarity的前k个是不是至少含有一个realBugs里面的元素
    for report in report_FinalScore.keys():
        local_shot = [0, 0, 0]
        # 一个report对应的所有<codeName,相似度>，此处降序
        computed_codes = report_FinalScore[report]
        # 一个report实际对应的Codes文件名
        real_code = real_codes[report]
        for rank, item in enumerate(computed_codes):
            code_name = item[0]
            if code_name in real_code:
                if rank < 1:
                    local_shot[0] += 1
                if rank < 5:
                    local_shot[1] += 1
                if rank < 10:
                    local_shot[2] += 1
        if local_shot[0] > 0:
            shot[0] += 1
        if local_shot[1] > 0:
            shot[1] += 1
        if local_shot[2] > 0:
            shot[2] += 1
    for i in range(3):
        shot[i] /= len(report_FinalScore)
    return shot


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


def MAP(report_FinalScore, real_codes):
    map = 0.0
    for report in report_FinalScore.keys():
        # 一个report对应的所有<codeName,相似度>，此处降序
        computed_codes = report_FinalScore[report]
        # 一个report实际对应的Codes文件名
        real_code = real_codes[report]
        sum = 0.0
        retrieved_d = 0.0
        for rank, item in enumerate(computed_codes):
            code_name = item[0]
            if code_name in real_code:
                retrieved_d += 1
                precision_i = retrieved_d / (rank + 1)
                sum += precision_i
        # 加上ap
        map += (sum / len(real_code))
    return map / len(report_FinalScore)


def MRR(report_FinalScore, real_codes):
    mrr = 0
    for report in report_FinalScore.keys():
        # 一个report对应的所有<codeName,相似度>，此处降序
        computed_codes = report_FinalScore[report]
        # 一个report实际对应的Codes文件名
        real_code = real_codes[report]
        rr = 0
        for rank, item in enumerate(computed_codes):
            code_name = item[0]
            if code_name in real_code:
                rr = 1 / (rank + 1)
                break
        mrr += rr
    return mrr / len(report_FinalScore)


if __name__ == '__main__':
    loadModule = LoadModule()
    # 数据库连接
    client = pymongo.MongoClient(host='172.31.42.10', port=27017)
    db = client.irbl
    # fixedFiles
    real_codes = loadModule.read_fixedfiles()
    codes = loadModule.read_codes()
    # 所有的小写文件名
    LowerCodeNames = {}
    for codeName in codes.keys():
        LowerCodeNames[codeName.lower()] = codeName
    w = [0.035449796689733165, 0.47843872325326786, 0.03986231797828736, 0.30728952216869343, 0.13895963991001817]
    # w = [0.06777415812470297,0.2923153121897406,0.24622212465766916,0.18480242404731917,0.20888598098056824]
    # w = [0.045769328287679226, 0.22890065625590705, 0.23240117831649004, 0.2771943127570789, 0.21573452438284488]
    # w = [0.18043645197669378, 0.23964180145195324, 0.14758664389039305, 0.20190939823386939, 0.23042570444709054]
    # w = [0.06764894440323742, 0.3724494670123132, 0.04464678557901813, 0.3771996164874699, 0.13805518651796125]
    # w = [0.07619213541592451, 0.5791135878357074, 0.15568744014496702, 0.02959431486900088, 0.15941252173440015]
    # w = [0.04531420237641243, 0.36064123432073797, 0.4113214078559783, 0.10881980352663936, 0.07390335192023192]
    # w =[0.06572993662181899, 0.14155425862972143, 0.29426989968583656, 0.27891076832433265, 0.21953513673829045]
    # w = [0.06572993662181899, 0.14155425862972143, 0.29426989968583656, 0.27891076832433265, 0.21953513673829045]
    # w = [0.42570239782621067,0.04871382535560102,0.004851003886240336,0.47617798776136033,0.04455478517058766]
    RIC = {}
    SC = {}
    SIM = {}
    STC = {}
    VHC = {}
    report_FinalScore = {}
    # path_of_json = ['./resultForAspectJ/RIC_AspectJ.json', './resultForAspectJ/SC_AspectJ.json',
    #                 './resultForAspectJ/SIM_AspectJ.json', './resultForAspectJ/STC_AspectJ.json',
    #                 './resultForAspectJ/VHC_AspectJ.json']

    path_of_json = ['./resultForSWT/RIC_SWT.json', './resultForSWT/SC_SWT.json',
                    './resultForSWT/SIM_SWT.json', './resultForSWT/STC_SWT.json',
                    './resultForSWT/VHC_SWT.json']

    # path_of_json = ['./resultForEclipse/RIC_Eclipse.json', './resultForEclipse/SC_Eclipse.json',
    #                 './resultForEclipse/SIM_Eclipse.json', './resultForEclipse/STC_Eclipse.json',
    #                 './resultForEclipse/VHC_Eclipse.json']

    i = 0
    for path_json in path_of_json:
        with open(path_json, 'r', encoding='UTF-8') as f:
            d = json.load(f)
        if i == 0:
            RIC = d
        elif i == 1:
            SC = d
        elif i == 2:
            SIM = d
        elif i == 3:
            STC = d
        else:
            VHC = d
        i += 1
    # 所有数值归一化
    normalize_data(RIC)
    normalize_data(SC)
    normalize_data(SIM)
    normalize_data(STC)
    normalize_data(VHC)

    reports = loadModule.read_report()
    codes = loadModule.read_codes()
    for reportName in reports.keys():
        FinalScore = {}
        for codeName in codes.keys():
            # todo 修改公式 SC SIM
            if SC[reportName][codeName] > 0 or SIM[reportName][codeName] > 0:
                FinalScore[codeName] = w[0] * RIC[reportName][codeName] + w[1] * SC[reportName][codeName] + w[2] * \
                                       SIM[reportName][codeName] + w[3] * STC[reportName][codeName] + w[4] * \
                                       VHC[reportName][codeName]
            else:
                FinalScore[codeName] = 0
        report_FinalScore[reportName] = FinalScore
    # normalize_data(report_FinalScore)
    for key in report_FinalScore.keys():
        code_names = list(report_FinalScore[key].keys())
        scores = np.array(list(report_FinalScore[key].values()))
        scores = normalization(scores)
        new_FinalScore = {}
        for i in range(len(code_names)):
            new_FinalScore[code_names[i]] = scores[i]
        report_FinalScore[key] = new_FinalScore

    # print(report_FinalScore)
    # D&C算法，通过文件名添加权重
    loadModule = LoadModule()
    origin_reports = loadModule.read_origin_reports()
    codes = loadModule.read_codes()
    for reportName in origin_reports.keys():
        report_content = origin_reports[reportName].split(' ')
        for word in report_content:
            if word.lower() in LowerCodeNames.keys():
                report_FinalScore[reportName][LowerCodeNames[word.lower()]] += 0.05
            if re.match(r'.*\.java', word):
                if len(word.split('.')) > 1:
                    class_name = word.split('.')[-2]
                    if class_name in codes.keys():
                        report_FinalScore[reportName][class_name] += 2

    # FinalScore排序
    for key in report_FinalScore.keys():
        report_FinalScore[key] = sorted(report_FinalScore[key].items(), key=lambda x: x[1], reverse=True)

    for report in report_FinalScore.keys():
        FinalScore = dict(report_FinalScore[report])
        report_FinalScore[report] = FinalScore
    for report in report_FinalScore.keys():
        score_list = []
        FinalScore_dict = report_FinalScore[report]
        for key in FinalScore_dict:
            score_list.append({'score': FinalScore_dict[key], 'code_name': key})
        db['SWT_rank'].insert_one(
            {'report_id': report, 'score_list': score_list, "_class": 'team.cdwx.irblapp.DAO.Result'})

    # FinalScore排序
    for key in report_FinalScore.keys():
        report_FinalScore[key] = sorted(report_FinalScore[key].items(), key=lambda x: x[1], reverse=True)

    with open('report_FinalScore_SWT.json', 'w') as file_obj:
        json.dump(report_FinalScore, file_obj)

    print("Top1: " + str(computeTopK(1, report_FinalScore, real_codes)))
    print("Top5: " + str(computeTopK(5, report_FinalScore, real_codes)))
    print("Top10: " + str(computeTopK(10, report_FinalScore, real_codes)))
    print("TopK: " + str(TopK(report_FinalScore, real_codes)))
    print("computeMRR: " + str(computeMRR(report_FinalScore, real_codes)))
    print("MRR: " + str(MRR(report_FinalScore, real_codes)))
    print("computeMAP: " + str(computeMAP(report_FinalScore, real_codes)))
    print("MAP: " + str(MAP(report_FinalScore, real_codes)))

# 只考虑vhc
# k=15
# Top1: 0.16783216783216784
# Top5: 0.32517482517482516
# Top10: 0.4090909090909091
# MRR: 0.2594237284178967
# MAP: 0.1677041150221768
# - 添加一些正则匹配后
# Top1: 0.16083916083916083
# Top5: 0.32867132867132864
# Top10: 0.4160839160839161
# MRR: 0.25632693159076303
# MAP: 0.16363838615851403

# k=5
# Top1: 0.18181818181818182
# Top5: 0.34615384615384615
# Top10: 0.4370629370629371
# MRR: 0.27614082680567825
# MAP: 0.1806199620957223

# k=10
# Top1: 0.1853146853146853
# Top5: 0.3531468531468531
# Top10: 0.4160839160839161
# MRR: 0.27579361116332396
# MAP: 0.17557857764367504

# k=20
# Top1: 0.17832167832167833
# Top5: 0.32867132867132864
# Top10: 0.4125874125874126
# MRR: 0.2641254059895144
# MAP: 0.16199365735041696

# k=30
# Top1: 0.1888111888111888
# Top5: 0.33916083916083917
# Top10: 0.44405594405594406
# MRR: 0.27407812381055235
# MAP: 0.15933055071892763
