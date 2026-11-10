from django.contrib import admin
from .models import Lesson, Exercise, LearningProgress, HintRecord


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "offering", "lesson_date")
    list_filter = ("lesson_date",)
    search_fields = ("title",)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "order")
    list_filter = ("lesson",)
    search_fields = ("title",)


@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "exercise", "is_completed", "updated_at")
    list_filter = ("is_completed",)
    readonly_fields = ("updated_at",)


@admin.register(HintRecord)
class HintRecordAdmin(admin.ModelAdmin):
    list_display = ("progress", "stage", "created_at")
    readonly_fields = ("created_at",)