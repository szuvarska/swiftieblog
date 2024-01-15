from allauth.account.views import LoginView, PasswordResetView, PasswordResetFromKeyView
from django.urls import path, include, re_path
from . import views
from .views import custom_logout, CustomSignupView

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('about', views.about, name='about'),
    path('articles/<int:article_id>', views.article, name='article'),
    path('user_account/', views.user_account, name='user_account'),
    path('accounts/signup/', CustomSignupView.as_view(template_name='account/signup.html'), name='account_signup'),
    path('accounts/login/', LoginView.as_view(template_name='account/login.html'), name='account_login'),
    path('accounts/password/reset/', PasswordResetView.as_view(template_name='account/password_reset.html'),
         name='account_reset'),
    re_path(
        r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        PasswordResetFromKeyView.as_view(template_name='account/password_change.html'),
        name="account_reset_password_from_key",
    ),
    path('accounts/logout/', custom_logout, name='account_logout'),
    path('accounts/confirmation_signup', views.confirmation_signup, name='account_confirmation_signup'),
    path('accounts/', include('allauth.urls')),
]
