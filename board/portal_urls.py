"""게시판 주소. 수정·삭제 권한은 각 뷰에서 별도로 확인합니다."""
from django.urls import path
from . import portal_views as views
app_name = 'board'
urlpatterns = [
    path('', views.listing, name='list'),
    path('new/', views.edit, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/answer/', views.answer, name='answer'),
    path('answers/<int:pk>/delete/', views.delete_answer, name='delete_answer'),
    path('attachments/<int:pk>/', views.download, name='download'),
    path('attachments/<int:pk>/delete/', views.delete_attachment, name='delete_attachment'),
]
