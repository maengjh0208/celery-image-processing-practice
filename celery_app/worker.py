# Celery 앱 인스턴스 생성 (시작점)


from celery import Celery


# Celery 앱을 생성하고 반환하는 함수
def create_celery_app() -> Celery:
    # Celery 인스턴스 생성
    # 첫번째 인자 = 앱 이름
    app = Celery("celery_app")

    # celery_app/config.py 설정
    app.config_from_object("celery_app.config")

    # Worker가 어떤 태스크 파일을 불러올지 등록
    app.conf.include = [
        "tasks.image_tasks",  # tasks/image_tasks.py
    ]

    return app


celery_app = create_celery_app()
