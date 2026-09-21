from django.urls import path

from . import views

# 다른 앱의 주소 이름과 충돌하지 않도록 구분합니다.
app_name = "academy"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path(
        "<int:course_id>/",
        views.course_detail,
        name="course_detail",
    ),
]