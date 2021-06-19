package team.cdwx.irblapp.DAO;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * @author Daiqj
 */
public class Result {

    private String report_id;
    private ArrayList<HashMap<String, String>> score_list;

    public String getReport_id() {
        return report_id;
    }

    public void setReport_id(String report_id) {
        this.report_id = report_id;
    }

    public ArrayList<HashMap<String, String>> getScore_list() {
        return score_list;
    }

    public void setScore_list(ArrayList<HashMap<String, String>> score_list) {
        this.score_list = score_list;
    }
}
