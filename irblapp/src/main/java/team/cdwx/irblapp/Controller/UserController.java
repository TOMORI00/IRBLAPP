package team.cdwx.irblapp.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import team.cdwx.irblapp.Service.AuthenticationService;
import team.cdwx.irblapp.VO.Response;
import team.cdwx.irblapp.VO.UserForm;

/**
 * 认证控制器
 * 负责登录功能、注册功能
 *
 * @author Daiqj
 */
@CrossOrigin
@RestController
@RequestMapping("/user")
public class UserController {

    private AuthenticationService authenticationService;

    @Autowired
    public void setAuthenticationService(AuthenticationService authenticationService) {
        this.authenticationService = authenticationService;
    }

    /**
     * 登录
     *
     * @return Response
     */
    @PostMapping(value = "/signUp")
    public Response signUp(@RequestBody UserForm userForm) {
        boolean response = authenticationService.signUp(userForm.getUsername(), userForm.getPassword());
        if (!response) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess("success");
    }

    /**
     * 注册
     *
     * @return Response
     */
    @PostMapping(value = "/signIn")
    public Response signIn(@RequestBody UserForm userForm) {
        boolean response = authenticationService.signIn(userForm.getUsername(), userForm.getPassword());
        if (!response) {
            return Response.buildSuccess("fail");
        }
        return Response.buildSuccess("success");
    }
}