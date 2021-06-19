import grpc
import RPC_pb2
import RPC_pb2_grpc

IP = 'localhost:50051'


def run():
    channel = grpc.insecure_channel(IP)
    stub = RPC_pb2_grpc.ComputeStub(channel=channel)
    response = stub.compute(RPC_pb2.ComputeRequest(Reports='{"app":["app is bad","client not good","width is over"]}', Codes='{"app":["app is bad","client not good","width is over"]}', FixedFiles='{"app":"widget"}'))
    print("received: " + response.RecommendFiles + " " + response.Metric)


if __name__ == '__main__':
    run()
