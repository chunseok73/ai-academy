from django.conf import settings
from django.db import models


class Lesson(models.Model):
    offering = models.ForeignKey(
        "academy.Offering",
        on_delete=models.PROTECT,
        related_name="lessons",
        verbose_name="개설강좌",
    )
    title = models.CharField("수업 제목", max_length=200)
    lesson_date = models.DateField("수업 날짜")
    description = models.TextField("수업 설명", blank=True)

    class Meta:
        ordering = ["lesson_date", "id"]
        verbose_name = "복습 수업"
        verbose_name_plural = "복습 수업"

    def __str__(self):
        return self.title


class Exercise(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="수업",
    )
    title = models.CharField("문제 제목", max_length=200)
    description = models.TextField("문제 설명")
    starter_code = models.TextField("시작 코드", blank=True)
    expected_output = models.TextField("예상 출력", blank=True)
    order = models.PositiveIntegerField("표시 순서", default=1)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "실습 문제"
        verbose_name_plural = "실습 문제"

    def __str__(self):
        return self.title


class LearningProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="learning_progress",
        verbose_name="학습자",
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="progress_records",
        verbose_name="문제",
    )
    code = models.TextField("작성 코드", blank=True)
    is_completed = models.BooleanField("학습 완료", default=False)
    updated_at = models.DateTimeField("마지막 저장 시각", auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "exercise"],
                name="unique_review_user_exercise",
            )
        ]
        verbose_name = "학습 기록"
        verbose_name_plural = "학습 기록"

    def __str__(self):
        return f"{self.user} / {self.exercise}"


class HintRecord(models.Model):
    progress = models.ForeignKey(
        LearningProgress,
        on_delete=models.CASCADE,
        related_name="hints",
        verbose_name="학습 기록",
    )
    stage = models.PositiveSmallIntegerField(
        "힌트 단계",
        choices=[
            (1, "개념"),
            (2, "접근 방법"),
            (3, "코드 점검"),
        ],
    )
    response = models.TextField("AI 힌트")
    created_at = models.DateTimeField("요청 시각", auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = "힌트 기록"
        verbose_name_plural = "힌트 기록"

    def __str__(self):
        return f"{self.progress} / 힌트 {self.stage}"