package team.cdwx.irblapp.Controller;

import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import team.cdwx.irblapp.DAO.Metric;
import team.cdwx.irblapp.DAO.Result;
import team.cdwx.irblapp.Service.DataService;
import team.cdwx.irblapp.VO.Response;

import java.util.List;

/**
 * 数据控制器
 * 负责上传功能、查询功能、展示功能
 *
 * @author Daiqj
 */
@CrossOrigin
@RestController
@RequestMapping("/data")
public class DataController {

    private DataService dataService;

    @Autowired
    public void setDataService(DataService dataService) {
        this.dataService = dataService;
    }

    /**
     * 上传项目
     *
     * @param multipartFile 上传的文件
     * @return Response
     */
    @PostMapping(value = "/upload")
    public Response upload(@RequestParam("files") MultipartFile multipartFile) {
        boolean response = dataService.upload(multipartFile);
        if (!response) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess("success");
    }

    /**
     * 上传ReportXML进行查询
     *
     * @param multipartFile 上传的文件
     * @return Response
     */
    @RequestMapping(value = "/query")
    public Response query(@RequestParam("report") MultipartFile multipartFile) {
        boolean response = dataService.query(multipartFile);
        if (!response) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess("success");
    }

    /**
     * 查询结果
     *
     * @return Response
     */
    @PostMapping(value = "/show")
    public Response show(@RequestBody String projectName) {
        List<Result> list = dataService.show(projectName.substring(0, projectName.length() - 1));
        if (list == null) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess(list);
    }

    /**
     * @param projectName
     * @return
     */
    @PostMapping(value = "/metric")
    public Response metric(@RequestBody String projectName) {
        List<Metric> metric = dataService.metric(projectName.substring(0, projectName.length() - 1));
        if (metric == null) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess(metric);
    }

    /**
     * @return
     */
    @RequestMapping(value = "/reset")
    public Response reset() {
        boolean response = dataService.reset();
        if (!response) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess("success");
    }

    @PostMapping(value = "/detail")
    public Response detail(@RequestBody JSONObject params) {
        String response = dataService.getReport(params.getString("projectName"), params.getString("report_id"));
        if ("No such report".equals(response)) {
            return Response.buildFailure(response);
        } else {
            JSONObject jsonObject = JSONObject.parseObject(response);
            return Response.buildSuccess(jsonObject);
        }
    }

    @PostMapping(value = "/run")
    public Response run(@RequestBody String projectName) {
        String response = dataService.run(projectName.substring(0, projectName.length() - 1));
        if (response.equals("")) {
            return Response.buildSuccess("fail");
        } else {
            JSONObject jsonObject = JSONObject.parseObject(response);
            return Response.buildSuccess(jsonObject);
        }
    }

}
