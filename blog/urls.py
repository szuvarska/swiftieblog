from allauth.account.views import LoginView, SignupView, LogoutView
from django.urls import path, include
from . import views
from .views import custom_logout

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('articles', views.articles, name='articles'),
    path('articles/<int:article_id>', views.article, name='article'),
    path('user_account/', views.user_account, name='user_account'),
    path('accounts/signup/', SignupView.as_view(template_name='registration/signup.html'), name='account_signup'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='account_login'),
    path('accounts/logout/', custom_logout, name='account_logout'),
    path('forum/', views.forum, name='forum'),
    path('forum/category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('forum/subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('forum/post/<int:post_id>/', views.post_detail, name='post_detail'),
]
