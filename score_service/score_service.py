import grpc
from concurrent import futures
import random
import scoring_pb2
import scoring_pb2_grpc


# Реализация ScoringService
class ScoringService(scoring_pb2_grpc.ScoringServiceServicer):
    def GetScore(self, request, context):
        # Генерируем случайный балл (от 0 до 1)
        score_value = random.uniform(0, 1)
        return scoring_pb2.ScoreResponse(score=score_value)


def serve():
    # Создаём gRPC сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scoring_pb2_grpc.add_ScoringServiceServicer_to_server(ScoringService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Scoring service is running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

