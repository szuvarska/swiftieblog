from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import logout

from .forms import CommentForm
from .models import Article, ForumPost, Comment, Subject, Category
from allauth.account.views import SignupView, LoginView


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
    return LoginView.as_view(template_name='registration/login.html')(request, **kwargs)


def custom_logout(request):
    logout(request)
    return redirect('/')


def forum(request):
    categories = Category.objects.annotate(
        subjects_count=Count('subjects'),
        posts_count=Count('subjects__forumpost'),
        last_post_date = Max('subjects__forumpost__pub_date'),
        last_post_author = Max('subjects__forumpost__author__username')
    )

    context = {'categories': categories}
    return render(request, 'forum.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subjects = category.subjects.all()

    context = {'category': category, 'subjects': subjects}
    return render(request, 'category_detail.html', context)


def subject_detail(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    posts = ForumPost.objects.filter(subject=subject)
    return render(request, 'subject_detail.html', {'subject': subject, 'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    return render(request, 'post_detail.html', {'post': post})
