from django.contrib import admin

from .models import Post, Answer


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "user", "offering", "created_at")
    search_fields = ("title", "content", "user__username")
    list_filter = ("category",)
    list_select_related = ("user", "offering")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    search_fields = ("content", "post__title")
    list_select_related = ("post", "user")
    readonly_fields = ("created_at", "updated_at")


# 첨부파일은 크기·확장자 검사와 파일명 자동 기록을 연결한 뒤
# 업로드 화면에서 관리하도록 다음 단계에 구현합니다.