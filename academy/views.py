from django.shortcuts import get_object_or_404, render

from .models import Course


def course_list(request):
    # 사용 중인 과정만 조회합니다.
    # 연결된 개설강좌도 함께 가져와 반복 조회를 줄입니다.
    courses = Course.objects.filter(
        is_active=True
    ).prefetch_related("offerings")

    return render(
        request,
        "academy/course_list.html",
        {"courses": courses},
    )


def course_detail(request, course_id):
    # 주소의 과정번호로 조회합니다.
    # 없는 번호이거나 비활성 과정이면 404 화면을 반환합니다.
    course = get_object_or_404(
        Course,
        course_id=course_id,
        is_active=True,
    )

    return render(
        request,
        "academy/course_detail.html",
        {
            "course": course,
            "offerings": course.offerings.all(),
        },
    )