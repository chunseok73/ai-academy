from django.contrib import admin

from .models import Course, Offering, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # 목록에 표시할 항목과 검색·필터 기능입니다.
    list_display = ("code", "name", "category", "level", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active", "level")


@admin.register(Offering)
class OfferingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "course",
        "instructor_name",
        "start_date",
        "end_date",
        "capacity",
        "status",
    )
    search_fields = ("name", "course__name", "instructor_name")
    list_filter = ("status",)

    # 연결된 과정 정보를 함께 조회해 불필요한 DB 조회를 줄입니다.
    list_select_related = ("course",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "offering", "status", "enrolled_at")
    search_fields = ("user__username", "offering__name")
    list_filter = ("status",)
    list_select_related = ("user", "offering")
    readonly_fields = ("enrolled_at",)