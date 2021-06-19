//package team.cdwx.irblapp.DAO;
//
//import org.junit.Assert;
//import org.junit.Before;
//import org.junit.Test;
//import org.junit.runner.RunWith;
//import org.springframework.boot.test.context.SpringBootTest;
//import org.springframework.boot.test.mock.mockito.MockBean;
//import org.springframework.context.annotation.ComponentScan;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.context.annotation.FilterType;
//import org.springframework.test.annotation.Rollback;
//import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
//import team.cdwx.irblapp.Driver.MongoDBDriver;
///**
// * @author: WHC
// * @description:
// * @date: 2021/4/18 4:17
// * @param null
// * @return
// */
//
//
//@RunWith(SpringJUnit4ClassRunner.class)
//@SpringBootTest
//@Rollback
//public class AnsTest {
//
//    @Configuration
//    @ComponentScan(value = "team.cdwx.irblapp.DAO",
//            useDefaultFilters = false,
//            includeFilters = @ComponentScan.Filter(
//                    type = FilterType.REGEX,
//                    pattern = {"team.cdwx.irblapp.DAO"})
//    )
//    static class InnerConfig {
//    }
//
//    @MockBean
//    Ans ans;
//
//    private String ansId;
//    private String metric;
//    private String recommend;
//
//    @Before
//    public  void init(){
//        ansId=new String("1");
//        metric=new String("2");
//        recommend=new String("3");
//    }
//    @Test
//    public void setAnsId() {
//        ansId=new String("1");
//        ans.setAnsId(ansId);
//    }
//    @Test
//    public void getAnsId() {
//        Assert.assertNull(ans.getAnsId());
//    }
//
//    @Test
//    public void setMetric() {
//        metric=new String("2");
//        ans.setMetric(metric);
//    }
//
//    @Test
//    public void getMetric() {
//        Assert.assertNull(ans.getMetric());
//    }
//
//    @Test
//    public void setRecommend() {
//        recommend=new String("3");
//        ans.setRecommend(recommend);
//    }
//
//    @Test
//    public void getRecommend() {
//        Assert.assertNull(ans.getRecommend());
//    }
//
//
//
//
//    @Test
//    public void testToString() {
//    }
//}