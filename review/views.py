from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from academy.models import Enrollment
from .models import Lesson, Exercise, LearningProgress


def accessible_lessons(user):
    lessons = Lesson.objects.select_related("offering__course")

    if not user.is_staff:
        offering_ids = Enrollment.objects.filter(
            user=user,
            status="enrolled",
        ).values("offering_id")

        lessons = lessons.filter(offering_id__in=offering_ids)

    return lessons


@login_required(login_url="login")
def lesson_list(request):
    return render(
        request,
        "review/lesson_list.html",
        {"lessons": accessible_lessons(request.user)},
    )


@login_required(login_url="login")
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(
        accessible_lessons(request.user),
        pk=lesson_id,
    )
    exercises = list(Exercise.objects.filter(lesson=lesson))

    saved_codes = dict(
        LearningProgress.objects.filter(
            user=request.user,
            exercise__lesson=lesson,
        ).values_list("exercise_id", "code")
    )

    for exercise in exercises:
        exercise.saved_code = saved_codes.get(
            exercise.pk,
            exercise.starter_code,
        )

    return render(
        request,
        "review/lesson_detail.html",
        {"lesson": lesson, "exercises": exercises},
    )


@login_required(login_url="login")
@require_POST
def save_code(request, exercise_id):
    exercise = get_object_or_404(
        Exercise.objects.filter(
            lesson__in=accessible_lessons(request.user)
        ),
        pk=exercise_id,
    )

    LearningProgress.objects.update_or_create(
        user=request.user,
        exercise=exercise,
        defaults={"code": request.POST.get("code", "")},
    )

    return redirect(
        "review:lesson_detail",
        lesson_id=exercise.lesson_id,
    )