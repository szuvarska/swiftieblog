from allauth.account.views import LoginView
from django.urls import path, include
from . import views
from .views import custom_logout, CustomSignupView

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('articles', views.articles, name='articles'),
    path('articles/<int:article_id>', views.article, name='article'),
    path('user_account/', views.user_account, name='user_account'),
    path('accounts/signup/', CustomSignupView.as_view(template_name='account/signup.html'), name='account_signup'),
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('accounts/logout/', custom_logout, name='account_logout'),
    path('accounts/confirmation_signup', views.confirmation_signup, name='account_confirmation_signup'),
    path('accounts/', include('allauth.urls')),
]
