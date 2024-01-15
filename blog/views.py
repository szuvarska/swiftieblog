from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .forms import CustomSignupForm
from .models import Article
from allauth.account.views import LoginView, SignupView


def main_page(request):
    latest_articles = Article.objects.order_by('-pub_date')
    context = {'latest_articles': latest_articles}
    return render(request, 'main_page.html', context)


def about(request):
    return render(request, 'about.html')


@login_required
def user_account(request):
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
    }

    context = {'user_info': user_info}
    return render(request, 'user_account.html', context)


def article(request, article_id):
    article = Article.objects.get(id=article_id)

    context = {'article': article}
    return render(request, 'article.html', context=context)


def custom_login(request, **kwargs):
    print('Using custom login template')
    return LoginView.as_view(template_name='account/login.html')(request, **kwargs)


def custom_logout(request):
    logout(request)
    return redirect('/')


class CustomSignupView(SignupView):
    form_class = CustomSignupForm


def confirmation_signup(request):
    return render(request, 'account/confirmation_signup.html')
