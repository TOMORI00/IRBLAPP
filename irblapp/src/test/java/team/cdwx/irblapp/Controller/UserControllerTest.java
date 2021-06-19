package team.cdwx.irblapp.Controller;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;
import team.cdwx.irblapp.DAO.User;
import team.cdwx.irblapp.VO.UserForm;

import static org.junit.Assert.*;

@RunWith(SpringRunner.class)
@SpringBootTest
public class UserControllerTest {

    @Autowired
    private WebApplicationContext wac;

    private MockMvc mvc;
    private MockHttpSession session;


    @Before
    public void setupMockMvc(){
        mvc = MockMvcBuilders.webAppContextSetup(wac).build(); //初始化MockMvc对象
        session = new MockHttpSession();
        User user =new User();
        UserForm userForm=new UserForm();
        userForm.setPassword("");
        userForm.setUsername("");
        session.setAttribute("user",user); //拦截器那边会判断用户是否登录，所以这里注入一个用户
    }


    //@Test
    //public void login() {
     //   MvcResult mvcResult= mvc.perform(MockMvcRequestBuilders.get("/user/login")
    //            .param("name","lvgang")
    //            .accept(MediaType.TEXT_HTML_VALUE))
    //}

    @Test
    public void signIn() throws Exception {
        //MvcResult mvcResult= (MvcResult)
        mvc.perform(MockMvcRequestBuilders.post("/user/signIn")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }

    @Test
    public void signup() throws Exception {
        //MvcResult mvcResult= (MvcResult)
        mvc.perform(MockMvcRequestBuilders.post("/user/signUp")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }
}