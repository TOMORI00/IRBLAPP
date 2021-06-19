package team.cdwx.irblapp.Driver;

import org.springframework.beans.Mergeable;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;
import team.cdwx.irblapp.DAO.Metric;
import team.cdwx.irblapp.DAO.Result;
import team.cdwx.irblapp.DAO.User;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * @author Daiqj
 */
@Repository
public class MongoDriver {

    private MongoTemplate mongoTemplate;

    @Autowired
    public void setMongoTemplate(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    /**
     * 增加新用户
     *
     * @param username 用户名
     * @param password 密码
     */
    public boolean addUser(String username, String password) {
        boolean out = false;
        User temp = searchUser(username);
        if (temp == null) {
            User user = new User();
            user.setUsername(username);
            user.setPassword(password);
            mongoTemplate.insert(user);
            out = true;
        }
        return out;
    }

    /**
     * 查找用户
     *
     * @param username 用户名
     */
    public User searchUser(String username) {
        Query query = new Query();
        query.addCriteria(Criteria.where("username").is(username));
        return mongoTemplate.findOne(query, User.class, "user");
    }


    public List<Result> searchResult(String projectName) {
//        Result result = new Result();
//        result.setReport_id("1237");
//        ArrayList<HashMap<String, String>> arrayList = new ArrayList<>();
//
//        HashMap<String, String> hashMap = new HashMap<>();
//        hashMap.put("code_name", "hha37haha");
//        hashMap.put("score", "0.172544");
//        arrayList.add(hashMap);
//        HashMap<String, String> hashMap1 = new HashMap<>();
//        hashMap1.put("code_name", "hh3a2haha");
//        hashMap1.put("score", "0.124342");
//        arrayList.add(hashMap1);
//        result.setScore_list(arrayList);
//        mongoTemplate.insert(result, projectName);
        return mongoTemplate.findAll(Result.class, projectName);
    }

    public List<Metric> searchMertic(String projectName) {
        return mongoTemplate.findAll(Metric.class, projectName);
    }
}

