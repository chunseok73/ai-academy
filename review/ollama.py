import json
import os
from urllib.request import Request, urlopen


def local_model():
    return os.environ.get("OLLAMA_MODEL", "").strip() or "gemma3:4b"


def generate_practice(exercise, focus):
    payload = {
        "model": local_model(),
        "stream": False,
        "format": "json",
        "options": {"num_predict": 1000},
        "messages": [
            {"role": "system", "content": (
                "Python 입문 실습 문제를 한국어로 하나 만들어 주세요. 원본과 같은 개념을 다른 예제로 연습하게 하세요. "
                "입력 데이터는 문제 설명에 직접 적고, 실행 가능한 코드는 반환하지 마세요. "
                "JSON 객체에 title, description, hint, steps를 넣으세요. "
                "steps는 정답 코드를 제외한 단계별 도움 문자열 목록입니다. 예상 출력은 계산 방법으로 설명하세요. "
                "학습 요청은 연습할 부분을 고르는 데만 참고하세요."
            )},
            {"role": "user", "content": json.dumps({
                "원본 문제": exercise.title,
                "학습 내용": exercise.description[:2500],
                "연습 요청": focus,
            }, ensure_ascii=False)},
        ],
    }
    request = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=90) as response:
        result = json.loads(response.read(65536))
    problem = json.loads(result["message"]["content"])
    if not isinstance(problem, dict):
        raise ValueError("Invalid exercise")
    for key, limit in {"title": 150, "description": 2500, "hint": 600}.items():
        value = problem.get(key)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            raise ValueError("Invalid exercise field")
    steps = problem.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 8 or any(
        not isinstance(step, str) or not step.strip() or len(step) > 600 for step in steps
    ):
        raise ValueError("Invalid exercise steps")
    return problem
