"""게시판: 목록부터 다운로드까지 같은 열람 권한을 적용합니다."""
from pathlib import Path
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from academy.models import Enrollment, Offering
from .models import Post, Answer, Attachment
from .portal_forms import PostForm, AnswerForm

def visible_posts(user):
    # 공통 글은 공개, 강좌 글은 현재 수강생과 관리자에게만 공개합니다.
    posts = Post.objects.select_related('user', 'offering')
    if user.is_authenticated and user.is_staff:
        return posts
    rule = Q(offering__isnull=True)
    if user.is_authenticated:
        ids = Enrollment.objects.filter(user=user, status='enrolled').values('offering_id')
        rule |= Q(offering_id__in=ids)
    return posts.filter(rule)

def can_edit(user, post):
    return user.is_authenticated and (user.is_staff or (post.user_id == user.pk and post.category == 'question'))

def selected_offering(request):
    """주소로 전달된 강좌를 확인하고, 현재 사용자의 접근 권한을 검사합니다."""
    value = request.GET.get('offering', '').strip()

    if not value:
        return None

    # 잘못된 강좌 번호도 서버 오류 대신 404로 처리합니다.
    try:
        offering_id = int(value)
    except (TypeError, ValueError):
        raise Http404("강좌를 찾을 수 없습니다.")

    if offering_id <= 0 or offering_id > 9223372036854775807:
        raise Http404("강좌를 찾을 수 없습니다.")

    offerings = Offering.objects.select_related('course')

    if not request.user.is_authenticated:
        raise Http404("강좌를 찾을 수 없습니다.")

    if not request.user.is_staff:
        # 주소의 강좌 번호를 바꿔도 미수강 강좌에는 접근할 수 없습니다.
        enrolled_ids = Enrollment.objects.filter(
            user=request.user,
            status='enrolled'
        ).values('offering_id')
        offerings = offerings.filter(pk__in=enrolled_ids)

    return get_object_or_404(offerings, pk=offering_id)

def listing(request):
    offering = selected_offering(request)

    # 기존 게시글 열람 권한을 유지한 상태에서 강좌 필터를 적용합니다.
    posts = visible_posts(request.user).prefetch_related('answers')
    if offering:
        posts = posts.filter(offering=offering)

    category = request.GET.get('category', '')
    query = request.GET.get('q', '').strip()

    if category in {'notice', 'material', 'question'}:
        posts = posts.filter(category=category)

    if query:
        posts = posts.filter(title__icontains=query)

    page = Paginator(posts, 10).get_page(request.GET.get('page'))

    return render(request, 'board/list.html', {
        'page': page,
        'q': query,
        'category': category,
        'offering': offering,
        'nav': 'board',
    })

def detail(request, pk):
    post = get_object_or_404(visible_posts(request.user), pk=pk)
    return render(request, 'board/detail.html', {'post':post, 'editable':can_edit(request.user,post), 'answer_form':AnswerForm(), 'nav':'board'})

@login_required(login_url='login')
def edit(request, pk=None):
    post = get_object_or_404(visible_posts(request.user), pk=pk) if pk else None
    if post and not can_edit(request.user, post):
        raise PermissionDenied
    # 새 글 작성 시에만 주소에서 전달된 강좌를 기본값으로 선택합니다.
    offering = selected_offering(request) if post is None else None
    initial = {'offering': offering.pk} if offering else {}

    form = PostForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=post,
        user=request.user,
        initial=initial,
    )
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        if not post.pk:
            post.user = request.user  # 작성자는 입력값이 아니라 로그인 세션에서 결정합니다.
        post.save()
        file = form.cleaned_data.get('attachment')
        if file:
            original = Path(file.name).name
            attachment = Attachment(post=post, original_name=original, size=file.size)
            # 저장명은 무작위로 생성하고, 원본 이름은 다운로드 때 사용합니다.
            attachment.file.save(uuid4().hex + Path(original).suffix.lower(), file, save=True)
        messages.success(request, '게시글을 저장했습니다.')
        return redirect('board:detail', pk=post.pk)
    return render(request, 'board/form.html', {'form':form, 'post':post, 'nav':'board'})

@login_required(login_url='login')
@require_POST
def delete(request, pk):
    post = get_object_or_404(visible_posts(request.user), pk=pk)
    if not can_edit(request.user, post):
        raise PermissionDenied
    files = [(a.file.storage, a.file.name) for a in post.attachments.all()]
    post.delete()  # 답변과 첨부 메타데이터는 CASCADE로 함께 삭제됩니다.
    for storage, name in files:
        storage.delete(name)
    messages.success(request, '게시글을 삭제했습니다.')
    return redirect('board:list')

@login_required(login_url='login')
@require_POST
def answer(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    post = get_object_or_404(visible_posts(request.user), pk=pk)
    form = AnswerForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.post, reply.user = post, request.user
        reply.save()
        messages.success(request, '답변을 등록했습니다.')
        return redirect('board:detail', pk=pk)
    return render(request, 'board/detail.html', {'post':post,'editable':True,'answer_form':form,'nav':'board'}, status=400)

@login_required(login_url='login')
@require_POST
def delete_answer(request, pk):
    if not request.user.is_staff:
        raise PermissionDenied
    reply = get_object_or_404(Answer, pk=pk)
    post_id = reply.post_id
    reply.delete()
    return redirect('board:detail', pk=post_id)

def download(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk, post__in=visible_posts(request.user))
    try:
        response = FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.original_name, content_type='application/octet-stream')
    except FileNotFoundError:
        raise Http404('첨부파일을 찾을 수 없습니다.')
    response['X-Content-Type-Options'] = 'nosniff'
    return response

@login_required(login_url='login')
@require_POST
def delete_attachment(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk, post__in=visible_posts(request.user))
    if not can_edit(request.user, attachment.post):
        raise PermissionDenied
    post_id = attachment.post_id
    attachment.file.delete(save=False)
    attachment.delete()
    return redirect('board:detail', pk=post_id)
