import time
import os
import sys
from concurrent import futures
import grpc
import RPC_pb2
import RPC_pb2_grpc
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, ".."))
from FilterService.filter import Filter
from ComputeService.computer import Computer

_ONE_DAY_IN_SERVICE = 60 * 60 * 24
IP = "[::]:50051"


class ComputeServiceClass(RPC_pb2_grpc.ComputeServicer):

    def compute(self, request, context):
        Reports = request.Reports
        Codes = request.Codes
        FixedFiles = request.FixedFiles
        bug_dic = eval(Reports)
        java_dic = eval(Codes)
        for key in java_dic:
            tem = []
            tem.append(java_dic[key])
            java_dic[key] = tem
        for key in bug_dic:
            tem = []
            tem.append(bug_dic[key])
            bug_dic[key] = tem
        fixed_dic = eval(FixedFiles)
        java_dic = Filter().splitWords(java_dic)
        bug_dic = Filter().splitWords(bug_dic)
        # 三个dict
        computer = Computer(0.2, reports=bug_dic, codes=java_dic, fixedFiles=fixed_dic)
        # 类型是str
        Metric_json = computer.getMetric()
        RecommendFiles_json = computer.getRecommendFiles()
        txt = 'OK'
        return RPC_pb2.ComputeReply(RecommendFiles=RecommendFiles_json, Metric=Metric_json)


class HelloServiceClass(RPC_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        txt = request.name
        return RPC_pb2.HelloReply(message='Hello ' + txt)


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    RPC_pb2_grpc.add_ComputeServicer_to_server(ComputeServiceClass(), grpcServer)
    RPC_pb2_grpc.add_GreeterServicer_to_server(HelloServiceClass(), grpcServer)
    grpcServer.add_insecure_port(IP)
    grpcServer.start()

    print("PY-SERVER start success")

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SERVICE)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    serve()
