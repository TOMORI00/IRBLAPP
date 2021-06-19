//package team.cdwx.irblapp.Driver;
//
//import org.junit.Assert;
//import org.junit.Test;
//import org.junit.runner.RunWith;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.boot.test.context.SpringBootTest;
//import org.springframework.boot.test.mock.mockito.MockBean;
//import org.springframework.context.annotation.ComponentScan;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.context.annotation.FilterType;
//import org.springframework.data.mongodb.core.MongoTemplate;
//import org.springframework.test.annotation.Rollback;
//import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
//import team.cdwx.irblapp.DAO.Ans;
//import team.cdwx.irblapp.DAO.Code;
//import team.cdwx.irblapp.DAO.Report;
//
//import java.util.HashMap;
//import java.util.LinkedList;
//import java.util.List;
//
//import static org.junit.jupiter.api.Assertions.*;
//
///**
// * @author: WHC
// * @description:
// * @date: 2021/4/18 4:17
// * @return null
// */
//
//
//@RunWith(SpringJUnit4ClassRunner.class)
//@SpringBootTest
//public class MongoDBDriverTest {
//
//    @Configuration
//    @ComponentScan(value = "team.cdwx.irblapp.Driver.rpcDriver",
//            useDefaultFilters = false,
//            includeFilters = @ComponentScan.Filter(
//                    type = FilterType.REGEX,
//                    pattern = {"team.cdwx.irblapp.Driver.rpcDriver"})
//    )
//    static class InnerConfig {
//    }
//
//    @MockBean
//    MongoDBDriver mongoDBDriver;
//
//
//
//
//    @Test
//    @Rollback
//    public void setMongoTemplate() {
//
//    }
//
//    @Test
//    public void findAllCodes() {
//        Assert.assertNotNull(
//                mongoDBDriver.findAllCodes()
//        );
//    }
//
//    @Test
//    public void findAllReports() {
//        Assert.assertNotNull(
//                mongoDBDriver.findAllReports()
//        );
//    }
//
//    @Test
//    public void saveCode() {
//        Code code=new Code();
//        mongoDBDriver.saveCode(code);
//        Assert.assertNotNull("1");
//    }
//
//    @Test
//    @Rollback
//    public void saveReport() {
//        Report report=new Report();
//        mongoDBDriver.saveReport(report);
//        Assert.assertNotNull("1");
//    }
//
//    @Test
//    @Rollback
//    public void saveSimilarityByName() {
//        mongoDBDriver.saveSimilarityByName("1",new HashMap<>());
//        Assert.assertNotNull("1");
//    }
//
//    @Test
//    @Rollback
//    public void saveAllCodes() {
//        List<Code> code=new LinkedList<>();
//        mongoDBDriver.saveAllCodes(code);
//        Assert.assertNotNull("1");
//    }
//
//    @Test
//    @Rollback
//    public void saveAllReports() {
//        List<Report>reports=new LinkedList<>();
//        mongoDBDriver.saveAllReports(reports);
//        Assert.assertNotNull("!");
//    }
//
//    @Test
//    @Rollback
//    public void findSimilarityByReportName() {
//        mongoDBDriver.findSimilarityByReportName("1111");
//        Assert.assertNotNull("45");
//    }
//
//    @Test
//    @Rollback
//    public void resetBase() {
//        mongoDBDriver.resetBase();
//        Assert.assertNotNull("5");
//    }
//
//    @Test
//    @Rollback
//    public void saveAns() {
//        Ans ans=new Ans();
//        mongoDBDriver.saveAns(ans);
//    }
//
//    @Test
//    public void findAns() {
//        Assert.assertNotNull(
//                mongoDBDriver.findAns()
//        );
//    }
//}