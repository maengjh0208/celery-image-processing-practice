# 태스크 실행 & 결과 확인

import time

from tasks.image_tasks import resize_image


def run_resize_task():
    """
    이미지 리사이징 태스크 실행하고 결과 출력
    """

    input_image = "images/input/example.jpg"
    width = 800
    height = 600

    print("=================================================")
    print("태스크 전송 중 ...")
    print(f"* 입력 파일: {input_image}")
    print(f"* 목표 크기: {width}x{height}")

    # .delay() 로 태스크 비동기 전송함
    result = resize_image.delay(input_image, width, height)

    print("=================================================")
    print("태스크 전송 완료")
    print(f"* Task Id: {result.task_id}")

    print("=================================================")
    print(f"결과 대기중 ...")
    # 상태 pulling -> 0.5초 간격으로 최대 10회 시도
    for i in range(10):
        # 태스크 상태
        # PENDING : 대기중 (아직 Worker가 못 받았거나 처리 전)
        # STARTED : Worker가 처리 시작
        # SUCCESS : 성공적으로 완료
        # FAILURE : 에러로 실패
        # RETRY : 재시도 중
        status = result.status
        print(f"[{i + 1}/10] 상태: {status}")

        if status == "SUCCESS":
            task_result = result.result
            print("=================================================")
            print("!!! 처리 완료 !!!")
            print(f"* 원본 파일: {task_result['input_path']}")
            print(f"* 출력 파일: {task_result['output_path']}")
            print(f"* 원본 크기: {task_result['original_size']}")
            print(f"* 변환 크기: {task_result['resized_size']}")
            print(f"* resized 파일 크기(KB): {task_result['file_size_kb']}")
            return
        elif status == "FAILURE":
            print("=================================================")
            print("XXX 태스크 실패 XXX")
            # 실패하면 .result 가 예외 객체를 담고 있음
            print(f"* 에러: {result.result}")
            return
        else:
            # 0.5초 후 재확인
            time.sleep(0.5)

    print("=================================================")
    print("타임 아웃 - 아직 결과 받지 못함")


if __name__ == "__main__":
    run_resize_task()
