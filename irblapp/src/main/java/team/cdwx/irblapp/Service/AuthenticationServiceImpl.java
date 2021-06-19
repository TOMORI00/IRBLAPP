package team.cdwx.irblapp.Service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import team.cdwx.irblapp.DAO.User;
import team.cdwx.irblapp.Driver.MongoDriver;

/**
 * @author Daiqj
 */
@Service
public class AuthenticationServiceImpl implements AuthenticationService {

    private MongoDriver mongoDriver;

    @Autowired
    public void setMongoDriver(MongoDriver mongoDriver) {
        this.mongoDriver = mongoDriver;
    }

    @Override
    public boolean signUp(String username, String password) {
        User user = mongoDriver.searchUser(username);
        return user.getPassword().equals(password);
    }

    @Override
    public boolean signIn(String username, String password) {
        return mongoDriver.addUser(username, password);
    }
}
