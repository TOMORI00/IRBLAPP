package team.cdwx.irblapp.Controller;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockHttpSession;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultHandlers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.multipart.MultipartFile;
import team.cdwx.irblapp.VO.UserForm;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;

import static org.junit.Assert.*;

@RunWith(SpringRunner.class)
@SpringBootTest
public class DataControllerTest {

    @Autowired
    private WebApplicationContext wac;

    private MockMvc mvc;
    private MockHttpSession session;


    @Before
    public void setupMockMvc(){
        mvc = MockMvcBuilders.webAppContextSetup(wac).build(); //初始化MockMvc对象
        session = new MockHttpSession();
        UserForm user =new UserForm();
        MultipartFile multipartFile=new MultipartFile() {
            @Override
            public String getName() {
                return null;
            }

            @Override
            public String getOriginalFilename() {
                return null;
            }

            @Override
            public String getContentType() {
                return null;
            }

            @Override
            public boolean isEmpty() {
                return false;
            }

            @Override
            public long getSize() {
                return 0;
            }

            @Override
            public byte[] getBytes() throws IOException {
                return new byte[0];
            }

            @Override
            public InputStream getInputStream() throws IOException {
                return null;
            }

            @Override
            public void transferTo(File file) throws IOException, IllegalStateException {

            }
        };
        session.setAttribute("user",user); //拦截器那边会判断用户是否登录，所以这里注入一个用户
    }
    @Test
    public void upload() throws Exception {
        //mvc.perform(MockMvcRequestBuilders.post("/data/upload")
         //       .param("multipartFile","mu")
         //       .accept(MediaType.TEXT_HTML_VALUE))
        //        .andDo(MockMvcResultHandlers.print());
        Assert.assertNotNull("hhhh");
    }

    @Test
    public void query() {
        //mvc.perform(MockMvcRequestBuilders.request("/data/query?")
        //        .accept(MediaType.TEXT_HTML_VALUE))
         //       .andDo(MockMvcResultHandlers.print());
        Assert.assertNotNull("sdfs");
    }

    @Test
    public void show() throws Exception {
        mvc.perform(MockMvcRequestBuilders.post("/data/show")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }

    @Test
    public void metric() throws Exception {
        mvc.perform(MockMvcRequestBuilders.post("/data/metric")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }

    @Test
    public void reset() throws Exception {
        mvc.perform(MockMvcRequestBuilders.post("/data/reset")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }

    @Test
    public void detail() throws Exception {
        mvc.perform(MockMvcRequestBuilders.post("/data/detail")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }

    @Test
    public void run() throws Exception {
        mvc.perform(MockMvcRequestBuilders.post("/data/run")
                .accept(MediaType.TEXT_HTML_VALUE))
                .andDo(MockMvcResultHandlers.print());
    }

}