package team.cdwx.irblapp.DAO;

/**
 * @author Daiqj
 */
public class Metric {

    private String top1;
    private String top5;
    private String top10;
    private String MRR;
    private String MAP;

    public String getTop1() {
        return top1;
    }

    public void setTop1(String top1) {
        this.top1 = top1;
    }

    public String getTop5() {
        return top5;
    }

    public void setTop5(String top5) {
        this.top5 = top5;
    }

    public String getTop10() {
        return top10;
    }

    public void setTop10(String top10) {
        this.top10 = top10;
    }

    public String getMRR() {
        return MRR;
    }

    public void setMRR(String MRR) {
        this.MRR = MRR;
    }

    public String getMAP() {
        return MAP;
    }

    public void setMAP(String MAP) {
        this.MAP = MAP;
    }
}
