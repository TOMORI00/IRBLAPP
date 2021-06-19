package team.cdwx.irblapp.Driver;

import com.alibaba.fastjson.JSONObject;

/**
 * @author Daiqj
 */
public interface RPCDriver {

    /**
     * compute
     * @param codes_s code
     * @param reports_s report
     * @param baselines_s fixed files
     * @return JSONObject
     */
    JSONObject compute(String codes_s, String reports_s, String baselines_s);
}
