import pymongo


class database:
    def __init__(self, url):
        self.client = pymongo.MongoClient("mongodb://" + url + ":27017/")
    def storeProjectRank(self, projectName, Rank_dic):
        mydb = self.client["irbl"]
        mycol = mydb[projectName + "_metric"]
        myquery = {"_id": "1"}
        if (mycol.find(myquery)):
            mycol.delete_one(myquery)
        Rank_dic["_id"] = "1"
        Rank_dic["_class"] = "team.cdwx.irblapp.DAO.Metric"
        mycol.insert_one(Rank_dic)
        return "ok"


if __name__ == "__main__":
    # myclient = pymongo.MongoClie】
    # 、nt("mongodb://localhost:27017/")
    # myclient = pymongo.MongoClient("mongodb://172.31.42.10:27017/")
    # db=database("localhost")
    db = database("172.31.42.10")
    rankdic = {"top1": "0.34408602150537637", "top5": "0.4731182795698925", "top10": "0.5053763440860215",
               "MRR": "0.4065217097984062", "MAP": "0.3184059121227315"}
    db.storeProjectRank("SWT", rankdic)
    rankdic = {"top1": "0.3440860237637", "top5": "0.4731182795698925", "top10": "0.5053763440860215",
               "MRR": "0.406", "MAP": "0.39827315"}
    db.storeProjectRank("AspectJ", rankdic)
    rankdic = {"top1": "0.3447", "top5": "0.4731182795698925", "top10": "0.5053763440860215",
               "MRR": "0.4084062", "MAP": "0.3184059121227315"}
    db.storeProjectRank("Eclipse", rankdic)
