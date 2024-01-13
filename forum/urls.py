from django.urls import path, include
from . import views

urlpatterns = [
    path('forum/', views.forum, name='forum'),
    path('forum/category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('forum/subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),
]
