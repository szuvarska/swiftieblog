from django.urls import path, include
from . import views
from .views import CustomSignupView

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('articles', views.articles, name='articles'),
    path('articles/<int:article_id>', views.article, name='article'),
    path('forum/', views.forum, name='forum'),
    path('user_account/', views.user_account, name='user_account'),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='auth')),
    # Login, Logout, Password Reset, etc.
    path('accounts/', include(('allauth.urls', 'allauth'), namespace='allauth')),  # django-allauth URLs
    path('accounts/register/', views.register, name='register'),  # Your custom registration view
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
]
