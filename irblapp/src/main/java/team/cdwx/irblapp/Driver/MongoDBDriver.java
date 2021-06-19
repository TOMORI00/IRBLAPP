//package team.cdwx.irblapp.Driver;
//
//import org.springframework.data.mongodb.core.MongoTemplate;
//import org.springframework.data.mongodb.core.query.Criteria;
//import org.springframework.data.mongodb.core.query.Query;
//import org.springframework.data.mongodb.core.query.Update;
//import team.cdwx.irblapp.DAO.Ans;
//import team.cdwx.irblapp.DAO.Code;
//import team.cdwx.irblapp.DAO.Report;
//
//import java.util.List;
//import java.util.Map;
//
///**
// * @author Daiqj
// */
//public class MongoDBDriver implements DBDriver {
//
//    private MongoTemplate mongoTemplate;
//
//    public void setMongoTemplate(MongoTemplate mongoTemplate) {
//        this.mongoTemplate = mongoTemplate;
//    }
//
//    /**
//     * 获取所有Code
//     *
//     * @return Code列表
//     */
//    @Override
//    public List<Code> findAllCodes() {
//        return mongoTemplate.findAll(Code.class);
//    }
//
//    /**
//     * 获取所有Report
//     *
//     * @return Report集合
//     */
//    @Override
//    public List<Report> findAllReports() {
//        return mongoTemplate.findAll(Report.class);
//    }
//
//    /**
//     * 存储code
//     *
//     * @param code CodeDAO
//     */
//    @Override
//    public void saveCode(Code code) {
//        mongoTemplate.insert(code);
//    }
//
//    /**
//     * 存储Report
//     *
//     * @param report ReportDAO
//     */
//    @Override
//    public void saveReport(Report report) {
//        mongoTemplate.insert(report);
//    }
//
//    /**
//     * 根据Report名称，存储Similarity
//     *
//     * @param reportName ReportDAO name
//     * @param similarity Map<String,Double>
//     */
//    @Override
//    public void saveSimilarityByName(String reportName, Map<String, Double> similarity) {
//        Query query = new Query();
//        query.addCriteria(Criteria.where("name").is(reportName));
//        Update update = new Update();
//        update.set("similarity", similarity);
//        mongoTemplate.updateMulti(query, update, Report.class);
//    }
//
//    @Override
//    public void saveAllCodes(List<Code> code) {
//        mongoTemplate.insertAll(code);
//    }
//
//    @Override
//    public void saveAllReports(List<Report> report) {
//        mongoTemplate.insertAll(report);
//    }
//
//    @Override
//    public void findSimilarityByReportName(String reportName) {
//        Query query = new Query();
//        query.addCriteria(Criteria.where("name").is(reportName));
//        Report report = mongoTemplate.findOne(query, Report.class, "report");
//        int u = 0;
//    }
//
//    @Override
//    public void resetBase() {
//        if (mongoTemplate.collectionExists(Report.class)) {
//            mongoTemplate.dropCollection(Report.class);
//        }
//        if (mongoTemplate.collectionExists(Code.class)) {
//            mongoTemplate.dropCollection(Code.class);
//        }
//        if (mongoTemplate.collectionExists(Ans.class)) {
//            mongoTemplate.dropCollection(Ans.class);
//        }
//    }
//
//    @Override
//    public void saveAns(Ans ans) {
//        mongoTemplate.insert(ans);
//    }
//
//    @Override
//    public List<Ans> findAns() {
//        return mongoTemplate.findAll(Ans.class);
//    }
//}
