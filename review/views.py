from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Lesson


@login_required(login_url="login")
def lesson_list(request):
    lessons = Lesson.objects.select_related("offering__course")

    # 관리자는 전체, 일반 회원은 현재 수강 중인 강좌만 조회합니다.
    if not request.user.is_staff:
        from academy.models import Enrollment

        offering_ids = Enrollment.objects.filter(
            user=request.user,
            status="enrolled",
        ).values("offering_id")

        lessons = lessons.filter(offering_id__in=offering_ids)

    return render(
        request,
        "review/lesson_list.html",
        {"lessons": lessons},
    )