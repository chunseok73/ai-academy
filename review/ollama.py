import json
import os
from random import sample
from urllib.request import Request, urlopen


def local_model():
    return os.environ.get("OLLAMA_MODEL", "").strip() or "gemma3:4b"


def cost_practice(focus):
    extended = any(word in focus for word in ("조금 응용", "세 금액", "세 번", "난이도 높"))
    parameters = ["first", "second", "third"] if extended else ["first", "second"]
    values = sample(range(500, 5100, 100), len(parameters))
    arguments = ", ".join(parameters)
    inputs = ", ".join(map(str, values))
    count = "세" if extended else "두"
    return {
        "title": f"{count} 번의 교통비 합계 반환하기 ({inputs})",
        "description": (
            f"add_fares({arguments}) 함수에서 {count} 금액의 합계를 return으로 돌려주세요. "
            f"함수 밖에서 돌려받은 값을 출력하세요. 입력 예시 {inputs} → 출력 {sum(values)}."
        ),
        "starter_code": f"def add_fares({arguments}):\n    pass\n\nprint(add_fares({inputs}))\n",
        "expected_output": str(sum(values)),
        "hint": "pass 한 줄을 바꾸세요. 함수 밖의 print가 함수에서 돌려준 값을 보여줘요.",
        "steps": [
            "아래 함수 호출에 들어 있는 금액을 첫 번째 매개변수부터 순서대로 대응시켜 보세요.",
            "함수 안에서 매개변수의 값을 모두 더하세요.",
            "더한 값을 return으로 돌려준 뒤 실행 결과를 확인하세요.",
        ],
    }


def generate_practice(exercise, focus):
    if (exercise.lesson.topic and exercise.lesson.topic.code == "1.4.1"
            and exercise.title == "두 지출의 합계를 함수로 반환하기"):
        return cost_practice(focus)
    payload = {
        "model": local_model(),
        "stream": False,
        "format": "json",
        "options": {"num_predict": 1000},
        "messages": [
            {"role": "system", "content": (
                "Python 입문 실습 문제를 한국어로 하나 만들어 주세요. 원본과 같은 문법과 난이도를 사용하고 소재와 데이터만 바꾸세요. 조금 응용하라는 요청에는 기존 문법 안에서 작은 변화 하나만 추가하세요. "
                "input(), 파일, 패키지 없이 풀 수 있게 하세요. 문제 설명에 조건과 값 예시, 그 값의 결과를 빠짐없이 적으세요. 실행 가능한 코드는 반환하지 마세요. "
                "JSON 객체에 title, description, hint, steps를 넣으세요. "
                "steps는 정답 코드를 제외한 단계별 도움 문자열 목록입니다. 예상 출력은 계산 방법으로 설명하세요. "
                "학습 요청은 연습할 부분을 고르는 데만 참고하세요."
            )},
            {"role": "user", "content": json.dumps({
                "원본 문제": exercise.title,
                "학습 내용": exercise.description[:2500],
                "원본 시작 코드": exercise.starter_code[:1500],
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
    return {key: problem[key] for key in ("title", "description", "hint", "steps")}
