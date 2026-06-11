# Celery 설정 파일

# 브로커(redis) 주소: 작업을 전달받는 우체통
# /0 는 Redis의 0번 데이터베이스를 사용한다는 의미
broker_url = "redis://localhost:6379/0"

# 결과 백엔드(redis) 주소: 작업 결과를 저장하는 창고 주소
result_backend = "redis://localhost:6379/1"

# 작업 결과 저장 만료 시간
result_expires = 3600

# 직렬화 형식이다. 데이터를 어떤 형태로 주고받을지. json 이 가장 범용적이다.
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# 시간대 설정 (한국 시간 KST)
timezone = "Asia/Seoul"
enable_utc = True
