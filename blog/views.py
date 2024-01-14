from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import logout

from .forms import CommentForm, CustomSignupForm
from .models import Article, Comment
from allauth.account.views import LoginView, SignupView


def main_page(request):
    # Retrieve the latest articles
    latest_articles = Article.objects.order_by('-pub_date')[:5]  # Change 5 to the desired number of articles

    context = {'latest_articles': latest_articles}
    return render(request, 'main_page.html', context)


@login_required  # Ensures the user is logged in to access this view
def user_account(request):
    # Retrieve the logged-in user's information
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        # Add more user-related information as needed
    }

    context = {'user_info': user_info}
    return render(request, 'user_account.html', context)


def articles(request):
    articles = Article.objects.order_by('-pub_date')
    context = {'list_of_articles': articles}
    return render(request, 'articles.html', context=context)


def article(request, article_id):
    article = Article.objects.get(id=article_id)
    comments = Comment.objects.filter(article=article).order_by('-pub_date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment(article=article,
                        author=form.cleaned_data["your_name"],
                        content=form.cleaned_data["comment"],
                        pub_date=timezone.now())
            c.save()
    else:
        form = CommentForm()

    context = {'article': article, 'comments': comments, 'form': form}
    return render(request, 'article.html', context=context)


def custom_login(request, **kwargs):
    print('Using custom login template')
    return LoginView.as_view(template_name='account/login.html')(request, **kwargs)


def custom_logout(request):
    logout(request)
    return redirect('/')


class CustomSignupView(SignupView):
    form_class = CustomSignupForm  # Use your custom form


def confirmation_signup(request):
    return render(request, 'account/confirmation_signup.html')
