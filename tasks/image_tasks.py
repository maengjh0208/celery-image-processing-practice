from pathlib import Path

from PIL import Image

from celery_app.worker import celery_app


# ─────────────────────────────────────────────
# @app.task 데코레이터 -> 이 함수를 Celery 태스크로 등록
# bind=True -> 첫번째 인자로 self(태스크 자신)을 받음. 그리고 나중에 재시도(retry)등 태스크 제어할때 사용
# name -> Celery 내부에서 이 태스크르 부르는 고유 이름
# ─────────────────────────────────────────────
@celery_app.task(bind=True, name="tasks.resize_image")
def resize_image(self, input_path: str, width: int, height: int) -> dict:
    """
    이미지를 지정한 크기로 리사이징

    Args:
        input_path: 원본 이미지 파일 경로 (예: "images/input/photo.jpg")
        width: 리사이징할 너비 (픽셀)
        height: 리사이징할 높이 (픽셀)

    Returns:
        dict: 결과 정보 (출력 경로, 원본/결과 크기 등)
    """

    # 원본 파일 확인
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"입력 파일이 존재하지 않음: {input_path}")

    # 출력 경로 생성
    output_dir = Path("images/output")
    # 폴더가 이미 있으면 넘어가고, 없으면 자동 생성
    output_dir.mkdir(parents=True, exist_ok=True)
    # stem = 확장자 제외한 파일명 / suffix = 확장자 (예: .jpg)
    output_filename = f"{input_file.stem}_{width}x{height}{input_file.suffix}"
    # Path 객체로 경로 결합
    output_path = output_dir / output_filename

    # 이미지 열고
    print("=================================================")
    print(f"[resize_image] 처리 시작: {input_path}")

    with Image.open(input_path) as img:
        original_size = img.size

        # 리사이징
        resized_img = img.resize((width, height), Image.LANCZOS)

        # 파일 저장
        if output_path.suffix.lower() in [".jpg", ".jpeg"]:
            resized_img.save(str(output_path), quality=85)
        else:
            resized_img.save(str(output_path))

    print("=================================================")
    print(f"[resized_image] 처리 완료: {output_path}")

    return {
        "input_path": str(input_path),
        "output_path": str(output_path),
        "original_size": {
            "width": original_size[0],
            "height": original_size[1],
        },
        "resized_size": {
            "width": width,
            "height": height,
        },
        "file_size_kb": round(output_path.stat().st_size / 1024, 2),
    }
