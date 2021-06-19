package team.cdwx.irblapp.Service;

import com.alibaba.fastjson.JSONObject;

/**
 * @author Daiqj
 */
public interface AuthenticationService {

    /**
     * 登录
     * @param username 用户名
     * @param password 密码
     * @return xxx
     */
    boolean signUp(String username, String password);

    /**
     * 注册
     * @param username 用户名
     * @param password 密码
     * @return xxx
     */
    boolean signIn(String username, String password);
}
