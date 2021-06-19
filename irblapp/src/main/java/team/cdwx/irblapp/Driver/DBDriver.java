//package team.cdwx.irblapp.Driver;
//
//import team.cdwx.irblapp.DAO.Ans;
//import team.cdwx.irblapp.DAO.Report;
//import team.cdwx.irblapp.DAO.Code;
//import java.util.List;
//import java.util.Map;
//
///**
// * @author Daiqj
// */
//public interface DBDriver {
//
//    /**
//     * 返回所有Code检索单元
//     * @return Code列表
//     * @see team.cdwx.irblapp.DAO.Code
//     */
//    List<Code> findAllCodes();
//
//    /**
//     * 返回所有Report检索单元
//     * @return Report列表
//     * @see team.cdwx.irblapp.DAO.Report
//     */
//    List<Report> findAllReports();
//
//    /**
//     * 保存一个Code检索单元
//     * @param code 传入一个Code类对象
//     * @see team.cdwx.irblapp.DAO.Code
//     */
//    void saveCode(Code code);
//
//    /**
//     * 保存一个Report检索单元
//      * @param report 传入一个Report对象
//     *  @see team.cdwx.irblapp.DAO.Report
//     */
//    void saveReport(Report report);
//
//    /**
//     * 保存一个Code检索单元列表
//     * @param code 传入一个Code列表
//     */
//    void saveAllCodes(List<Code> code);
//
//    /**
//     * 保存一个Report检索单元列表
//     * @param report 传入一个Report列表
//     */
//    void saveAllReports(List<Report> report);
//
//    /**
//     * 为Report检索单元更新相似文件字段
//     * @param reportName Report的名字
//     * @param similarity 相似文件键值对组
//     */
//    void saveSimilarityByName(String reportName, Map<String,Double> similarity);
//
//    /**
//     * 返回某Report检索单元的相似文件字段
//     * @param reportName Report的名字
//     */
//    void findSimilarityByReportName(String reportName);
//
//    /**
//     * 重置数据库
//     */
//    void resetBase();
//
//    /**
//     * saveAns
//     * @param ans
//     */
//    void saveAns(Ans ans);
//
//    /**
//     * findans
//     * @return ans
//     */
//    List<Ans> findAns();
//}
