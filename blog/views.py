from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone

from .forms import CommentForm
from .models import Article, ForumPost, Comment
from allauth.account.views import SignupView


def main_page(request):
    # Retrieve the latest articles
    latest_articles = Article.objects.order_by('-pub_date')[:5]  # Change 5 to the desired number of articles

    context = {'latest_articles': latest_articles}
    return render(request, 'main_page.html', context)


def forum(request):
    latest_forum_posts = ForumPost.objects.order_by('-pub_date')[:5]  # Change 5 to the desired number of forum posts

    context = {'latest_forum_posts': latest_forum_posts}
    return render(request, 'forum.html', context)


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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            messages.success(request, 'Registration successful!')
            return redirect('main_page')  # Redirect to the main page or another view
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


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
    return render(request, 'blog/post.html', context=context)


class CustomSignupView(SignupView):
    template_name = 'registration/signup.html'  # Customize this to your template path

    def form_valid(self, form):
        # Your custom logic after the form is successfully validated
        response = super().form_valid(form)
        # Add any additional logic here
        return response

    def form_invalid(self, form):
        # Your custom logic if the form is invalid
        response = super().form_invalid(form)
        # Add any additional logic here
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data if needed
        return context
