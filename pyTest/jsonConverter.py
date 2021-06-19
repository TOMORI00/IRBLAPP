import json
from collections import OrderedDict

import pymongo
from loadModule_aspectj import LoadModule


def TopK(report_FinalScore, real_codes):
    # 命中次数
    shot = [0,0,0]
    # 判断reportSimilarity的前k个是不是至少含有一个realBugs里面的元素
    for report in report_FinalScore.keys():
        local_shot = [0, 0, 0]
        # 一个report对应的所有<codeName,相似度>，此处降序
        computed_codes = report_FinalScore[report]
        # 一个report实际对应的Codes文件名
        real_code = real_codes[report]
        for rank,item in enumerate(computed_codes):
            code_name = item
            if code_name in real_code:
                if rank<1:
                    local_shot[0] += 1
                if rank<5:
                    local_shot[1] += 1
                if rank<10:
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

if __name__ == '__main__':
    # 数据库连接
    client = pymongo.MongoClient(host='172.31.42.10', port=27017)
    db = client.irbl
    loadModule = LoadModule()
    reports = loadModule.read_report()
    real_codes = loadModule.read_fixedfiles()
    result = {}
    for report in reports.keys():
        res = db.SC_AspectJ.find_one({'report_id': report})
        dic = {}
        for item in res['score_list']:
            code_name = item['code_name']
            score = item['score']
            dic[code_name] = score
        dic = OrderedDict(sorted(dic.items(), reverse=True, key=lambda x: x[1]))
        result[report] = dic
    with open('SC_AspectJ.json', 'w') as file_obj:
        json.dump(result, file_obj)
    print("TopK: " + str(TopK(result,real_codes)))



