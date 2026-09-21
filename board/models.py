from django.conf import settings
from django.db import models


class Post(models.Model):
    """공지·자료·질문을 하나의 테이블에서 구분하여 관리합니다."""

    class Category(models.TextChoices):
        NOTICE = "notice", "공지"
        MATERIAL = "material", "자료"
        QUESTION = "question", "질문"

    post_id = models.BigAutoField(primary_key=True)

    # 작성자는 Django 기본 회원 테이블과 연결합니다.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="작성자",
    )

    # 강좌를 지정하지 않으면 전체 공지나 공통 질문으로 사용합니다.
    # PPT의 게시글-개설강좌 관계를 유지하되 연결은 선택 사항입니다.
    offering = models.ForeignKey(
        "academy.Offering",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="관련 강좌",
        null=True,
        blank=True,
    )

    category = models.CharField(
        "분류",
        max_length=10,
        choices=Category.choices,
        default=Category.QUESTION,
    )
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        db_table = "board_post"
        verbose_name = "게시글"
        verbose_name_plural = "게시글"
        ordering = ["-created_at", "-post_id"]

    def __str__(self):
        return self.title


class Answer(models.Model):
    """게시글에 작성하는 답변입니다. 한 게시글에 여러 답변이 가능합니다."""

    # PPT의 물리 모델에 맞춰 DB에서는 comment_id를 사용합니다.
    comment_id = models.BigAutoField(primary_key=True)

    # 게시글을 삭제하면 해당 글의 답변도 함께 삭제합니다.
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="게시글",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="answers",
        verbose_name="답변 작성자",
    )
    content = models.TextField("답변 내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        db_table = "board_comment"
        verbose_name = "답변"
        verbose_name_plural = "답변"
        ordering = ["created_at", "comment_id"]

    def __str__(self):
        return f"{self.post.title}의 답변"


class Attachment(models.Model):
    """실제 파일은 폴더에, 파일 경로와 정보는 DB에 저장합니다."""

    attachment_id = models.BigAutoField(primary_key=True)

    # 한 게시글에 여러 첨부파일을 연결할 수 있습니다.
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name="게시글",
    )

    # MEDIA_ROOT 아래에 연/월 단위 폴더로 저장합니다.
    file = models.FileField(
        "첨부파일",
        upload_to="attachments/%Y/%m/",
        max_length=255,
    )
    original_name = models.CharField("원본 파일명", max_length=255)
    size = models.PositiveBigIntegerField("파일 크기(byte)")
    uploaded_at = models.DateTimeField("업로드일", auto_now_add=True)

    class Meta:
        db_table = "board_attachment"
        verbose_name = "첨부파일"
        verbose_name_plural = "첨부파일"
        ordering = ["uploaded_at", "attachment_id"]

    def __str__(self):
        return self.original_name