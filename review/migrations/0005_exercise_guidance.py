from django.db import migrations, models


def add_guidance(apps, schema_editor):
    Exercise = apps.get_model("review", "Exercise")
    exercises = Exercise.objects.using(schema_editor.connection.alias).filter(
        lesson__title="반복문으로 합계 구하기",
        lesson__topic__code="1.3.2",
        lesson__topic__section="Python",
        lesson__topic__unit="반복과 누적",
    )
    exercises.filter(title="교통비만 골라 합계 내기").update(guidance={
        "prompt": "category는 지출 분류예요. ==는 두 값이 같은지 확인해요. 따옴표 안에 더할 분류를 써보세요.",
        "before": 'if category == "',
        "after": '":',
        "answer": "교통",
        "steps": [
            ["total = 0", "더하기 전이므로 합계는 0원이에요."],
            ["for category, amount in expenses:", '첫 기록 ("교통", 1500)에서 category는 "교통", amount는 1500이에요.'],
            ['    if category == "교통":', '첫 기록은 조건을 만족해요. 다음 기록인 "식비"는 건너뛰어요.'],
            ["        total = total + amount", "첫 기록을 더하면 합계가 0원에서 1500원으로 바뀌어요. 식비를 볼 때는 1500원 그대로예요."],
            ["print(total)", "맨 왼쪽에 써서 반복이 끝난 뒤 합계 5500을 한 번 출력해요."],
        ],
    })
    exercises.filter(title="목표 걸음 수를 달성한 날 세기").update(guidance={
        "prompt": "목표와 정확히 같은 날도 세어야 해요. ‘크거나 같다’를 뜻하는 비교 연산자를 넣어보세요.",
        "before": "if step ",
        "after": " goal:",
        "answer": ">=",
        "steps": [
            ["days = 0", "아직 확인한 날이 없으므로 0일에서 시작해요."],
            ["for step in steps:", "첫날은 step이 3000이고, 다음 날은 4500이에요."],
            ["    if step >= goal:", "목표가 4000보라면 3000은 건너뛰고 4500은 포함해요. 딱 4000보여도 포함해요."],
            ["        days = days + 1", "4500보를 확인했을 때 0일에서 1일로 바뀌어요. 그다음 5000보를 확인하면 2일이 돼요."],
            ["print(days)", "맨 왼쪽에 써서 모든 날을 확인한 뒤 달성 일수 3을 출력해요."],
        ],
    })


class Migration(migrations.Migration):
    dependencies = [("review", "0004_add_loop_exercises")]
    operations = [
        migrations.AddField(
            model_name="exercise",
            name="guidance",
            field=models.JSONField("단계별 도움", default=dict, blank=True),
        ),
        migrations.RunPython(add_guidance, migrations.RunPython.noop),
    ]
