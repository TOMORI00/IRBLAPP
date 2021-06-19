package team.cdwx.irblapp;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;


/**s
 * @author Daiqj
 */
@Component
public class initRunner implements ApplicationRunner {

    private static final Logger LOG = LoggerFactory.getLogger(IrblappApplication.class);

    @Override
    public void run(ApplicationArguments args) throws Exception {
        LOG.info("=*=*=*=*=*=*=*=*=*=*=*=*=*=  READY  =*=*=*=*=*=*=*=*=*=*=*=*=");
    }
}