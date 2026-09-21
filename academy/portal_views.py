"""학습 홈과 계정 화면. 기존 academy/views.py는 그대로 사용합니다."""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from academy.models import Enrollment
from board.models import Post

def home(request):
    # 인증되지 않은 방문자는 다른 회원의 수강 정보를 조회하지 않습니다.
    enrollments = Enrollment.objects.none()
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(
            user=request.user, status='enrolled'
        ).select_related('offering__course')
    # 첫 버전은 공통 공지·자료만 보여줍니다. 강좌별 글의 권한은 게시판 단계에서 처리합니다.
    posts = Post.objects.filter(
        category__in=['notice', 'material'], offering__isnull=True
    ).order_by('-created_at')[:3]
    return render(request, 'academy/home.html', {
        'enrollments': enrollments, 'posts': posts, 'nav': 'home',
    })

@login_required(login_url='login')
def mine(request):
    # 주소를 직접 입력하더라도 로그인한 본인의 수강만 조회합니다.
    enrollments = Enrollment.objects.filter(user=request.user).select_related('offering__course')
    return render(request, 'academy/mine.html', {'enrollments': enrollments, 'nav': 'mine'})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    # Django 기본 폼이 아이디 중복과 비밀번호 확인을 검사하고 해시로 저장합니다.
    form = UserCreationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'academy/signup.html', {'form': form})
