"""수강신청/취소: 로그인한 본인의 자료만 POST로 변경합니다."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Offering, Enrollment

@login_required(login_url='login')
@require_POST
def enroll(request, offering_id):
    # 첫 DB 작업을 쓰기로 시작해 SQLite에서도 정원 검사와 등록을 직렬화합니다.
    # 정원 값 자체는 바꾸지 않으며, 아래 작업은 한 트랜잭션으로 처리합니다.
    with transaction.atomic():
        Offering.objects.filter(pk=offering_id).update(capacity=F('capacity'))
        offering = get_object_or_404(Offering.objects.select_related('course'), pk=offering_id)
        existing = Enrollment.objects.filter(user=request.user, offering=offering).first()
        if existing and existing.status == 'enrolled':
            messages.info(request, '이미 신청한 강좌입니다.')
        elif offering.status != 'open' or not offering.course.is_active:
            messages.error(request, '현재 신청할 수 없는 강좌입니다.')
        elif Enrollment.objects.filter(offering=offering, status='enrolled').count() >= offering.capacity:
            messages.error(request, '정원이 마감되었습니다.')
        else:
            # 취소 이력이 있으면 기존 행을 재사용해 중복 기록을 방지합니다.
            Enrollment.objects.update_or_create(user=request.user, offering=offering, defaults={'status': 'enrolled'})
            messages.success(request, '수강신청이 완료되었습니다.')
    return redirect('mine')

@login_required(login_url='login')
@require_POST
def cancel(request, enrollment_id):
    # URL 번호를 바꾸더라도 다른 사람의 수강신청은 취소할 수 없습니다.
    with transaction.atomic():
        enrollment = get_object_or_404(Enrollment, pk=enrollment_id, user=request.user)
        Enrollment.objects.filter(pk=enrollment.pk, user=request.user).update(status='cancelled')
    messages.success(request, '수강신청을 취소했습니다.')
    return redirect('mine')
