from django.db import migrations


def add_loop_exercises(apps, schema_editor):
    Lesson = apps.get_model("review", "Lesson")
    Exercise = apps.get_model("review", "Exercise")
    db = schema_editor.connection.alias
    lessons = Lesson.objects.using(db).filter(
        title="반복문으로 합계 구하기",
        topic__code="1.3.2",
        topic__section="Python",
        topic__unit="반복과 누적",
    )
    exercises = (
        {
            "title": "교통비만 골라 합계 내기",
            "description": (
                "[응용하기] 지출 목록을 for문으로 돌면서 분류가 '교통'인 금액만 더하세요. "
                "마지막에 합계 숫자만 출력하세요."
            ),
            "starter_code": (
                'expenses = [("교통", 1500), ("식비", 8000), ("교통", 2000),\n'
                '            ("간식", 3000), ("교통", 2000)]\n\n'
                '# 교통비만 더해보세요.\n'
            ),
            "expected_output": "5500",
            "order": 2,
        },
        {
            "title": "목표 걸음 수를 달성한 날 세기",
            "description": (
                "[스스로 풀기] 걸음 수 목록을 for문으로 돌면서 목표 이상인 날의 수를 세세요. "
                "목표와 같은 날도 포함하고, 마지막에 일수만 출력하세요."
            ),
            "starter_code": "steps = [3000, 4500, 5000, 3800, 5200, 2700, 3800]\ngoal = 4000\n",
            "expected_output": "3",
            "order": 3,
        },
    )
    for lesson_id in lessons.values_list("pk", flat=True).iterator():
        for exercise in exercises:
            if not Exercise.objects.using(db).filter(
                lesson_id=lesson_id, title=exercise["title"],
            ).exists():
                Exercise.objects.using(db).create(lesson_id=lesson_id, **exercise)


class Migration(migrations.Migration):
    dependencies = [("review", "0003_curriculum_material")]
    operations = [migrations.RunPython(add_loop_exercises, migrations.RunPython.noop)]
