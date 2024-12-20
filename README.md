# AIS24-DZ3

### ДЗ-3 полное. Микросервисы с использованием Docker и Nginx и gRPC

Этот проект демонстрирует архитектуру микросервисов, реализованную с использованием Python Flask, Docker,  Nginx и gRPC. Проект состоит из трёх сервисов:

Проект состоит из трёх HTTP-сервисов:

- **Score Service** — рассчитывает "хорошесть" пользователя.
- **Auth Service** — проверяет, может ли пользователь войти в систему.
- **Composition Service** — сначала обращается к Score Service, а затем к Auth Service для проверки входа на основании оценки пользователя.

- **Score Service (Сервис оценки)**:
  - Точка входа: `/score`
  - Генерирует случайный рейтинг (score) для указанного логина.

- **Auth Service (Сервис аутентификации)**:
  - Точка входа: `/auth`
  - Проверяет аутентификацию пользователя по логину и паролю.

- **Composition Service (Сервис композиции)**:
  - Точка входа: `/composition`
  - Объединяет функциональность сервисов Score Service и Auth Service, используя балансировку нагрузки через Nginx.

### Как сделано

- **Сервисы в Docker-контейнерах**:
  - Каждый сервис работает в своём отдельном контейнере.
  - Управление осуществляется с помощью `docker-compose`.
  
- **gRPC взаимодействие**:
  - composition_service обращается к scoring_service и auth_service через gRPC для проверки данных.

- **gБалансировщик нагрузки**:
  - Nginx используется в качестве L7-балансировщика нагрузки для нескольких экземпляров Composition Service.


### Структура проекта
```
my_microservices/
├── auth_service/
│   ├── auth_service.py
│   ├── auth_service.proto
│   ├── auth_service_pb2.py
│   ├── auth_service_pb2_grpc.py
│   ├── Dockerfile
│   └── requirements.txt
├── score_service/
│   ├── score_service.py
│   ├── scoring.proto
│   ├── scoring_pb2.py
│   ├── scoring_pb2_grpc.py
│   ├── Dockerfile
│   └── requirements.txt
├── composition_service/
│   ├── composition_service.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── nginx.conf

```

## Развёртывание и запуск

Должег быть устанлвен Docker и Docker Compose

Склонируйте репозиторий проекта:

	git clone https://github.com/FIIT24GP/AIS24-DZ3.git
	
	cd AIS24-DZ3

Соберите и запустите проект:
    sudo docker-compose up --build

Пример запроса

sudo curl -X POST -H "Content-Type: application/json" -d '{"login": "user1", "password": "password1"}' http://127.0.0.1:8080/composition




