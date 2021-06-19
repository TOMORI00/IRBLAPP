package team.cdwx.irblapp.Driver.rpcDriver;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import org.springframework.stereotype.Component;
import team.cdwx.irblapp.Driver.RPCDriver;

import java.util.concurrent.TimeUnit;

/**
 * @author Daiqj
 */
@Component
public class RPCDriverImpl implements RPCDriver {

    private final ManagedChannel channel;
    private final GreeterGrpc.GreeterBlockingStub blockingStub;
    private final ComputeGrpc.ComputeBlockingStub computeBlockingStub;

    public RPCDriverImpl() {
//        channel = ManagedChannelBuilder.forAddress("42.192.54.221", 50051)
        channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()
                .build();
        blockingStub = GreeterGrpc.newBlockingStub(channel);
        computeBlockingStub = ComputeGrpc.newBlockingStub(channel);
    }

    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    /**
     * RPC连接测试
     */
    public void greet() {

        RPC.HelloRequest request = RPC.HelloRequest.newBuilder().setName("connection").build();
        RPC.HelloReply response;
        try {
            response = blockingStub.sayHello(request);
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: {0}" + e.getStatus());
            return;
        }
        System.out.println(("Greeting: " + response.getMessage()));
    }

    /**
     * 进行RPC调用
     * @param codes_s     code
     * @param reports_s   report
     * @param baselines_s fixed files
     * @return JSONObject 计算结果，包括度量值和列表
     */
    @Override
    public JSONObject compute(String codes_s, String reports_s, String baselines_s) {
        RPC.ComputeRequest request = RPC.ComputeRequest.newBuilder().setCodes(codes_s).setReports(reports_s).setFixedFiles(baselines_s).build();
        RPC.ComputeReply response;
        try {
            response = computeBlockingStub.compute(request);
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: {0}" + e.getStatus());
            return null;
        }
        System.out.println(("COMPUTE OK: " + response.getRecommendFiles()) + response.getMetric());
        JSONObject metric = (JSONObject) JSONObject.parse(response.getMetric());
        JSONObject recommend = (JSONObject) JSON.parse(response.getRecommendFiles());
        JSONObject out = new JSONObject();
        out.put("metric", metric);
        out.put("recommend", recommend);
        return out;
    }


    public static void main(String[] args) throws Exception {
        RPCDriverImpl client = new RPCDriverImpl();
        try {
            client.greet();
        } finally {
            client.shutdown();
        }
    }

}