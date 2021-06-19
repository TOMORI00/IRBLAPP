package team.cdwx.irblapp.Service;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.httpclient.*;
import org.apache.commons.httpclient.methods.GetMethod;
import org.apache.commons.httpclient.params.HttpMethodParams;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import team.cdwx.irblapp.DAO.Metric;
import team.cdwx.irblapp.DAO.Result;
import team.cdwx.irblapp.Driver.MongoDriver;
import team.cdwx.irblapp.Handler.ASTHandler;
import team.cdwx.irblapp.Handler.CommitXMLHandler;
import team.cdwx.irblapp.Handler.ReportXMLHandler;
import team.cdwx.irblapp.Handler.ZIPHandler;

import java.io.File;
import java.io.IOException;
import java.util.List;

/**
 * @author Daiqj
 */
@Service
public class DataServiceImpl implements DataService {

    @Value("${uploadProject.path}")
    private String projectPath;

    @Value("${uploadReport.path}")
    private String reportPath;

    @Value("${targetPath.path}")
    private String targetPath;

    @Value("${tempPath.path}")
    private String tempPath;

    private MongoDriver mongoDriver;

    public static boolean deleteFile(File file) {
        if (file == null || !file.exists()) {
            System.out.println("文件删除失败,请检查文件路径是否正确");
            return false;
        }
        File[] files = file.listFiles();
        for (File f : files) {
            String name = file.getName();
//            System.out.println(name);
            if (f.isDirectory()) {
                deleteFile(f);
            } else {
                f.delete();
            }
        }
        file.delete();
        return true;
    }

    public static String doGet(String url, String charset) {
        HttpClient httpClient = new HttpClient();
        httpClient.getHttpConnectionManager().getParams().setConnectionTimeout(50000);
        GetMethod getMethod = new GetMethod(url);
        getMethod.getParams().setParameter(HttpMethodParams.SO_TIMEOUT, 50000);
        getMethod.getParams().setParameter(HttpMethodParams.RETRY_HANDLER, new DefaultHttpMethodRetryHandler());
        String response = "";
        try {
            int statusCode = httpClient.executeMethod(getMethod);
            if (statusCode != HttpStatus.SC_OK) {
                System.err.println("请求出错：" + getMethod.getStatusLine());
            }
            Header[] headers = getMethod.getResponseHeaders();
            for (Header h : headers) {
                System.out.println(h.getName() + "---------------" + h.getValue());
            }
            byte[] responseBody = getMethod.getResponseBody();
            response = new String(responseBody, charset);
            System.out.println("response:" + response);
        } catch (HttpException e) {
            System.out.println("请检查输入的URL!");
            e.printStackTrace();
        } catch (IOException e) {
            System.out.println("发生网络异常!");
        } finally {
            getMethod.releaseConnection();
        }
        return response;
    }

    @Autowired
    public void setMongoDriver(MongoDriver mongoDriver) {
        this.mongoDriver = mongoDriver;
    }

    @Override
    public boolean upload(MultipartFile multipartFile) {

        if (multipartFile.isEmpty()) {
            return false;
        }
        String fileName = multipartFile.getOriginalFilename();
        File dest = new File(new File(projectPath).getAbsolutePath() + "/" + fileName);
        if (!dest.getParentFile().exists()) {
            dest.getParentFile().mkdirs();
        }
        try {
            multipartFile.transferTo(dest);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean query(MultipartFile multipartFile) {
        if (multipartFile.isEmpty()) {
            return false;
        }
        String fileName = multipartFile.getOriginalFilename();
        File dest = new File(new File(reportPath).getAbsolutePath() + "/" + fileName);
        if (!dest.getParentFile().exists()) {
            dest.getParentFile().mkdirs();
        }
        try {
            multipartFile.transferTo(dest);
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public List<Metric> metric(String projectName) {
        return mongoDriver.searchMertic(projectName + "_metric");
    }

    @Override
    public List<Result> show(String projectName) {
        return mongoDriver.searchResult(projectName);
    }

    @Override
    public boolean reset() {
        deleteFile(new File(projectPath));
        deleteFile(new File(reportPath));
        deleteFile(new File(targetPath));
        deleteFile(new File(tempPath));
        return true;
    }

    @Override
    public String getReport(String projectName, String reportID) {
        return doGet("http://127.0.0.1:9999/getReport?project=" + projectName + "&reportID=" + reportID, "UTF-8");
    }

    @Override
    public String run(String projectName) {
        File target = new File(targetPath);
        target.mkdir();
        ReportXMLHandler reportXmlHandler = new ReportXMLHandler();
        reportXmlHandler.parseXML(reportPath + "\\" + "New" + projectName + "BugRepository.xml", projectName);
        CommitXMLHandler commitXMLHandler = new CommitXMLHandler();
        commitXMLHandler.parseXML(reportPath + "\\" + projectName+"CommitRepository.xml", projectName);
        try {
            ZIPHandler.zipUncompress(projectPath + "\\swt-3.1.zip", tempPath);
            ASTHandler.run(tempPath + "\\swt-3.1", targetPath);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return doGet("http://127.0.0.1:9999/upload?project=" + projectName, "UTF-8");
    }
}
