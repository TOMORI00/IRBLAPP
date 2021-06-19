package team.cdwx.irblapp.Driver.rpcDriver;

import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.16.1)",
    comments = "Source: RPC.proto")
public final class ComputeGrpc {

  private ComputeGrpc() {}

  public static final String SERVICE_NAME = "Compute";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<RPC.ComputeRequest,
      RPC.ComputeReply> getComputeMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "compute",
      requestType = RPC.ComputeRequest.class,
      responseType = RPC.ComputeReply.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<RPC.ComputeRequest,
      RPC.ComputeReply> getComputeMethod() {
    io.grpc.MethodDescriptor<RPC.ComputeRequest, RPC.ComputeReply> getComputeMethod;
    if ((getComputeMethod = ComputeGrpc.getComputeMethod) == null) {
      synchronized (ComputeGrpc.class) {
        if ((getComputeMethod = ComputeGrpc.getComputeMethod) == null) {
          ComputeGrpc.getComputeMethod = getComputeMethod = 
              io.grpc.MethodDescriptor.<RPC.ComputeRequest, RPC.ComputeReply>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(
                  "Compute", "compute"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  RPC.ComputeRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  RPC.ComputeReply.getDefaultInstance()))
                  .setSchemaDescriptor(new ComputeMethodDescriptorSupplier("compute"))
                  .build();
          }
        }
     }
     return getComputeMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ComputeStub newStub(io.grpc.Channel channel) {
    return new ComputeStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ComputeBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new ComputeBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ComputeFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new ComputeFutureStub(channel);
  }

  /**
   */
  public static abstract class ComputeImplBase implements io.grpc.BindableService {

    /**
     */
    public void compute(RPC.ComputeRequest request,
        io.grpc.stub.StreamObserver<RPC.ComputeReply> responseObserver) {
      asyncUnimplementedUnaryCall(getComputeMethod(), responseObserver);
    }

    @Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getComputeMethod(),
            asyncUnaryCall(
              new MethodHandlers<
                RPC.ComputeRequest,
                RPC.ComputeReply>(
                  this, METHODID_COMPUTE)))
          .build();
    }
  }

  /**
   */
  public static final class ComputeStub extends io.grpc.stub.AbstractStub<ComputeStub> {
    private ComputeStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ComputeStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @Override
    protected ComputeStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ComputeStub(channel, callOptions);
    }

    /**
     */
    public void compute(RPC.ComputeRequest request,
        io.grpc.stub.StreamObserver<RPC.ComputeReply> responseObserver) {
      asyncUnaryCall(
          getChannel().newCall(getComputeMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class ComputeBlockingStub extends io.grpc.stub.AbstractStub<ComputeBlockingStub> {
    private ComputeBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ComputeBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @Override
    protected ComputeBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ComputeBlockingStub(channel, callOptions);
    }

    /**
     */
    public RPC.ComputeReply compute(RPC.ComputeRequest request) {
      return blockingUnaryCall(
          getChannel(), getComputeMethod(), getCallOptions(), request);
    }
  }

  /**
   */
  public static final class ComputeFutureStub extends io.grpc.stub.AbstractStub<ComputeFutureStub> {
    private ComputeFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ComputeFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @Override
    protected ComputeFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ComputeFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<RPC.ComputeReply> compute(
        RPC.ComputeRequest request) {
      return futureUnaryCall(
          getChannel().newCall(getComputeMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_COMPUTE = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final ComputeImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(ComputeImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @Override
    @SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_COMPUTE:
          serviceImpl.compute((RPC.ComputeRequest) request,
              (io.grpc.stub.StreamObserver<RPC.ComputeReply>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @Override
    @SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class ComputeBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ComputeBaseDescriptorSupplier() {}

    @Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return RPC.getDescriptor();
    }

    @Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Compute");
    }
  }

  private static final class ComputeFileDescriptorSupplier
      extends ComputeBaseDescriptorSupplier {
    ComputeFileDescriptorSupplier() {}
  }

  private static final class ComputeMethodDescriptorSupplier
      extends ComputeBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    ComputeMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (ComputeGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ComputeFileDescriptorSupplier())
              .addMethod(getComputeMethod())
              .build();
        }
      }
    }
    return result;
  }
}
