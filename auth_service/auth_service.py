from concurrent import futures
import grpc
import auth_service_pb2
import auth_service_pb2_grpc


class AuthService(auth_service_pb2_grpc.AuthServiceServicer):
    def Authenticate(self, request, context):
        # Проверка логина и пароля
        if request.login == "user1" and request.password == "password1":
            return auth_service_pb2.AuthResponse(auth=True)
        return auth_service_pb2.AuthResponse(auth=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_service_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

