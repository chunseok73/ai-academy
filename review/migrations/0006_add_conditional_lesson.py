from datetime import date

from django.db import migrations


SOURCE_DATE = date(2026, 7, 23)
EXERCISES = [
    {
        "title": "비가 오면 우산 챙기기",
        "description": "[따라 하기] raining이 True이면 '우산 챙기기'를 출력하세요. False이면 아무것도 출력하지 않아요.",
        "starter_code": "raining = True\n",
        "expected_output": "우산 챙기기",
        "guidance": {
            "prompt": "조건이 참일 때만 다음 줄을 실행하는 키워드를 넣으세요.",
            "before": "",
            "after": " raining:",
            "answer": "if",
            "steps": [
                ["if raining:", "raining이 True이면 아래 줄을 실행해요."],
                ['    print("우산 챙기기")', "공백 4칸을 넣어요. False로 바꿔 실행하면 이 줄을 건너뛰어요."],
            ],
        },
    },
    {
        "title": "어린이 입장료 정하기",
        "description": "[응용하기] 12세 이하는 3000원, 13세 이상은 5000원이에요. 금액 숫자만 출력하세요.",
        "starter_code": "age = 12\n",
        "expected_output": "3000",
        "guidance": {
            "prompt": "12세도 어린이 요금이에요. ‘작거나 같다’를 뜻하는 비교 연산자를 넣으세요.",
            "before": "if age ",
            "after": " 12:",
            "answer": "<=",
            "steps": [
                ["if age <= 12:", "age가 12이면 조건이 참이에요."],
                ["    fee = 3000", "조건이 참일 때 어린이 요금을 저장해요."],
                ["else:", "조건이 거짓일 때 실행할 부분이에요. if와 같은 위치에 써요."],
                ["    fee = 5000", "age를 13으로 바꾸면 이 줄이 실행돼요."],
                ["print(fee)", "조건문이 끝나면 정해진 금액을 한 번 출력해요."],
            ],
        },
    },
    {
        "title": "세 구간의 배송비 정하기",
        "description": "[스스로 풀기] 주문액이 50000원 이상이면 무료, 30000원 이상 50000원 미만이면 2000원, 그보다 적으면 3500원이에요. 배송비 숫자만 출력하세요.",
        "starter_code": "amount = 30000\n",
        "expected_output": "2000",
        "guidance": {
            "prompt": "첫 조건이 거짓일 때 다음 조건을 확인하는 키워드를 넣으세요.",
            "before": "",
            "after": " amount >= 30000:",
            "answer": "elif",
            "steps": [
                ["if amount >= 50000:", "50000원도 30000원 이상이므로 무료 조건부터 확인해요."],
                ["    fee = 0", "50000원 이상이면 배송비는 0원이에요."],
                ["elif amount >= 30000:", "첫 조건이 거짓이고 이 조건이 참이면 중간 구간이에요."],
                ["    fee = 2000", "시작 코드의 30000원은 여기에서 2000원으로 정해져요."],
                ["else:", "두 조건 모두 거짓이면 마지막 구간이에요."],
                ["    fee = 3500", "29999원으로 바꾸면 배송비는 3500원이에요."],
                ["print(fee)", "선택된 배송비를 한 번만 출력해요."],
            ],
        },
    },
]


def add_conditional_lesson(apps, schema_editor):
    db = schema_editor.connection.alias
    lessons = apps.get_model("review", "Lesson").objects.using(db)
    topics = apps.get_model("review", "CurriculumTopic").objects.using(db)
    materials = apps.get_model("review", "CurriculumMaterial").objects.using(db)
    exercises = apps.get_model("review", "Exercise").objects.using(db)

    offering_ids = lessons.filter(
        title="반복문으로 합계 구하기", topic__code="1.3.2",
        topic__section="Python", topic__unit="반복과 누적",
    ).order_by().values_list("offering_id", flat=True).distinct()
    Offering = apps.get_model("academy", "Offering")
    for offering in Offering.objects.using(db).filter(pk__in=offering_ids).iterator():
        topic, _ = topics.get_or_create(
            course_id=offering.course_id, code="1.2.3",
            defaults={"section": "Python", "unit": "문자열과 판단", "title": "연산자·if·elif·else", "order": 123},
        )
        materials.get_or_create(
            topic=topic, title="Python 기초 예제 (day02)",
            defaults={
                "source_date": SOURCE_DATE,
                "source_location": "SlackBackup/2026-07-23/2026-07-23_files/17-36-16_day02.zip",
                "preparation": "브라우저의 Python 실습창에서 시작하세요. 조건을 하나씩 바꿔 어떤 줄이 실행되는지 확인하세요.",
                "order": 1,
            },
        )
        lesson, _ = lessons.get_or_create(
            offering=offering, topic=topic, title="조건문으로 판단하기",
            defaults={
                "lesson_date": SOURCE_DATE,
                "description": "조건이 참일 때만 실행하기 → 두 갈래 중 하나 선택하기 → 여러 조건을 순서대로 확인하기",
            },
        )
        for order, exercise in enumerate(EXERCISES, start=1):
            exercises.get_or_create(
                lesson=lesson, title=exercise["title"],
                defaults={**exercise, "order": order},
            )


class Migration(migrations.Migration):
    dependencies = [("review", "0005_exercise_guidance")]
    operations = [migrations.RunPython(add_conditional_lesson, migrations.RunPython.noop)]
