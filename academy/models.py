from django.conf import settings
from django.db import models


class Course(models.Model):
    """교육과정: 여러 개설강좌에서 공통으로 사용하는 교육 내용"""

    course_id = models.BigAutoField(primary_key=True)
    code = models.CharField("과정코드", max_length=20, unique=True)
    name = models.CharField("과정명", max_length=100)
    category = models.CharField("분류", max_length=50, blank=True)
    level = models.CharField("난이도", max_length=20, default="입문")
    description = models.TextField("과정 소개")
    curriculum = models.TextField("학습 내용", blank=True)
    is_active = models.BooleanField("사용 여부", default=True)

    class Meta:
        db_table = "academy_course"
        verbose_name = "교육과정"
        verbose_name_plural = "교육과정"
        ordering = ["name"]

    def __str__(self):
        # 관리자 화면에서 번호 대신 과정명을 표시합니다.
        return self.name


class Offering(models.Model):
    """개설강좌: 같은 교육과정도 기간과 반을 달리하여 개설할 수 있습니다."""

    class Status(models.TextChoices):
        OPEN = "open", "모집중"
        RUNNING = "running", "진행중"
        CLOSED = "closed", "종료"

    offering_id = models.BigAutoField(primary_key=True)

    # 교육과정 하나에 여러 강좌가 연결됩니다.
    # 연결된 강좌가 있으면 교육과정을 실수로 삭제하지 못하게 보호합니다.
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="offerings",
        verbose_name="교육과정",
    )

    name = models.CharField("개설강좌명", max_length=120)
    instructor_name = models.CharField("강사명", max_length=50)
    start_date = models.DateField("시작일")
    end_date = models.DateField("종료일")
    schedule = models.CharField(
        "수업 시간 안내",
        max_length=100,
        help_text="예: 평일 09:00~18:00",
    )
    capacity = models.PositiveIntegerField("정원", default=20)
    status = models.CharField(
        "개설 상태",
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )

    class Meta:
        db_table = "academy_offering"
        verbose_name = "개설강좌"
        verbose_name_plural = "개설강좌"
        ordering = ["-start_date", "-offering_id"]

    def __str__(self):
        return f"{self.course.name} / {self.name}"


class Enrollment(models.Model):
    """수강신청: 회원과 개설강좌 사이를 연결하는 모델"""

    class Status(models.TextChoices):
        ENROLLED = "enrolled", "수강등록"
        CANCELLED = "cancelled", "신청취소"

    enrollment_id = models.BigAutoField(primary_key=True)

    # 비밀번호를 별도 테이블에 저장하지 않고 Django 회원 모델을 참조합니다.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="회원",
    )
    offering = models.ForeignKey(
        Offering,
        on_delete=models.PROTECT,
        related_name="enrollments",
        verbose_name="개설강좌",
    )
    enrolled_at = models.DateTimeField("최초 신청일", auto_now_add=True)
    status = models.CharField(
        "신청 상태",
        max_length=10,
        choices=Status.choices,
        default=Status.ENROLLED,
    )

    class Meta:
        db_table = "academy_enrollment"
        verbose_name = "수강신청"
        verbose_name_plural = "수강신청"
        ordering = ["-enrolled_at"]

        # 동일 회원이 같은 강좌에 두 번 등록되는 것을 DB에서도 막습니다.
        # 취소 후 다시 신청할 때는 기존 행의 상태를 변경하는 방식으로 구현합니다.
        constraints = [
            models.UniqueConstraint(
                fields=["user", "offering"],
                name="unique_user_offering",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} / {self.offering.name}"