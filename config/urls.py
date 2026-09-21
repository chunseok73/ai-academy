"""프로젝트 전체 주소. 로그인 성공 및 로그아웃 후 학습 홈으로 이동합니다."""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from academy import portal_views, enrollment_views

class PortalLoginView(LoginView):
    template_name = 'academy/login.html'
    next_page = 'home'
    redirect_authenticated_user = True

urlpatterns = [
    path('board/', include('board.portal_urls')),
    path('enroll/<int:offering_id>/', enrollment_views.enroll, name='enroll'),
    path('enrollments/<int:enrollment_id>/cancel/', enrollment_views.cancel, name='cancel_enrollment'),
    path('admin/', admin.site.urls),
    path('', portal_views.home, name='home'),
    path('courses/', include('academy.urls')),
    path('my-courses/', portal_views.mine, name='mine'),
    path('accounts/login/', PortalLoginView.as_view(), name='login'),
    # 로그아웃은 CSRF 토큰을 포함한 POST 폼으로만 요청합니다.
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/signup/', portal_views.signup, name='signup'),
]
