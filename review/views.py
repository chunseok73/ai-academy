from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from academy.models import Enrollment
from .models import Lesson, Exercise


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
    exercises = Exercise.objects.filter(lesson=lesson)

    return render(
        request,
        "review/lesson_detail.html",
        {"lesson": lesson, "exercises": exercises},
    )