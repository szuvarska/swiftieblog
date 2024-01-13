from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Subquery, OuterRef
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import logout

from .forms import CommentForm, ForumPostForm, SubjectForm
from .models import Article, ForumPost, Comment, Subject, Category
from allauth.account.views import LoginView


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
        last_post_date=Subquery(
            ForumPost.objects.filter(subject__category=OuterRef('pk')).order_by('-pub_date').values('pub_date')[:1]
        ),
        last_post_author=Subquery(
            ForumPost.objects.filter(subject__category=OuterRef('pk')).order_by('-pub_date').values('author__username')[
            :1]
        )
    )

    context = {'categories': categories}
    return render(request, 'forum/forum.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subjects = category.subjects.all()

    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        if subject_form.is_valid():
            # Create the first post for the new subject
            post_content = request.POST.get('post_content')  # Adjust accordingly based on your form field name
            subject = subject_form.save(commit=False)
            post = ForumPost(content=post_content, author=request.user, subject=subject)
            subject.category = category
            subject.author = request.user
            subject.save()
            post.save()

            # Clear the form after successful submission
            subject_form = SubjectForm()

            return redirect('category_detail', category_id=category.id)
    else:
        subject_form = SubjectForm()

    context = {'category': category, 'subjects': subjects, 'subject_form': subject_form}
    return render(request, 'forum/category_detail.html', context)


def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    posts = ForumPost.objects.filter(subject=subject).order_by('pub_date')

    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.subject = subject
            post.author = request.user
            post.save()

            # Clear the form after successful submission
            form = ForumPostForm()
    else:
        form = ForumPostForm()

    context = {'subject': subject, 'posts': posts, 'form': form}
    return render(request, 'forum/subject_detail.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    return render(request, 'forum/post_detail.html', {'post': post})
