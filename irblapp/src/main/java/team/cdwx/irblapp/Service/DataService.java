package team.cdwx.irblapp.Service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.web.multipart.MultipartFile;
import team.cdwx.irblapp.DAO.Metric;
import team.cdwx.irblapp.DAO.Result;

import java.util.List;

/**
 * @author Daiqj
 */
public interface DataService {

    /**
     * @param multipartFile 上传的文件
     * @return 操作成功与否
     */
    boolean upload(MultipartFile multipartFile);

    /**
     * xxx
     *
     * @return xxx
     */
    boolean query(MultipartFile multipartFile);

    /**
     * xxx
     *
     * @return xxx
     */
    List<Result> show(String projectName);

    /**
     * @param projectName
     * @return
     */
    List<Metric> metric(String projectName);

    /**
     * @return
     */
    boolean reset();

    /**
     *
     * @param projectName
     * @param reportID
     */
    String getReport(String projectName,String reportID);

    /**
     *
     * @return
     */
    String run(String projectName);
}
