from django.contrib import admin
from .models import CurriculumMaterial, CurriculumTopic, Lesson, Exercise, LearningProgress, HintRecord


class CurriculumMaterialInline(admin.TabularInline):
    model = CurriculumMaterial
    extra = 0


@admin.register(CurriculumTopic)
class CurriculumTopicAdmin(admin.ModelAdmin):
    list_display = ("code", "section", "unit", "title", "course", "order")
    list_filter = ("course",)
    search_fields = ("code", "section", "unit", "title")
    readonly_fields = ("course",)
    inlines = (CurriculumMaterialInline,)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else ()


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "offering", "topic", "lesson_date")
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