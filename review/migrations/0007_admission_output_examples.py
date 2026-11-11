from django.db import migrations


def add_output_examples(apps, schema_editor):
    Exercise = apps.get_model("review", "Exercise")
    exercises = Exercise.objects.using(schema_editor.connection.alias).filter(
        lesson__topic__code="1.2.3",
        lesson__title="조건문으로 판단하기",
        title="어린이 입장료 정하기",
    )
    for exercise in exercises.iterator():
        exercise.guidance = {
            **exercise.guidance,
            "output_examples": [
                {"input": "age = 12", "output": "3000"},
                {"input": "age = 13", "output": "5000"},
            ],
        }
        exercise.save(update_fields=["guidance"], using=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [("review", "0006_add_conditional_lesson")]
    operations = [migrations.RunPython(add_output_examples, migrations.RunPython.noop)]
