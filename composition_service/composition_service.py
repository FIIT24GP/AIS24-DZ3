import sys
sys.path.append('/app/score_service')  # Путь для gRPC файлов scoring
sys.path.append('/app/auth_service')  # Путь для gRPC файлов auth


from flask import Flask, request, jsonify
import grpc
import scoring_pb2
import scoring_pb2_grpc
import auth_service_pb2
import auth_service_pb2_grpc

app = Flask(__name__)

@app.route('/composition', methods=['POST'])
def composition():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    # Проверка входных данных
    if not login or not password:
        return jsonify({"error": "Login and password required"}), 400

    # gRPC вызов в scoring
    try:
        with grpc.insecure_channel('scoring:50051') as scoring_channel:
            scoring_stub = scoring_pb2_grpc.ScoringServiceStub(scoring_channel)
            scoring_response = scoring_stub.GetScore(scoring_pb2.ScoreRequest(login=login))
            score_value = scoring_response.score
    except Exception as e:
        return jsonify({"error": f"Failed to connect to scoring service: {str(e)}"}), 500

    # Проверка порога
    if score_value < 0.5:
        return jsonify({"auth": False, "reason": "Low score"}), 403

    # gRPC вызов в auth_service
    try:
        with grpc.insecure_channel('auth_service:50052') as auth_channel:
            auth_stub = auth_service_pb2_grpc.AuthServiceStub(auth_channel)
            auth_response = auth_stub.Authenticate(auth_service_pb2.AuthRequest(login=login, password=password))
            is_authenticated = auth_response.auth
    except Exception as e:
        return jsonify({"error": f"Failed to connect to auth service: {str(e)}"}), 500

    # Если оба условия выполнены, возвращаем успешный ответ
    if is_authenticated:
        return jsonify({"auth": True, "score": score_value})
    else:
        return jsonify({"auth": False, "reason": "Invalid credentials"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

