from django.db.models import Count, Subquery, OuterRef
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ForumPostForm, SubjectForm
from .models import ForumPost, Subject, Category


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
            post_content = request.POST.get('post_content')
            subject = subject_form.save(commit=False)
            post = ForumPost(content=post_content, author=request.user, subject=subject)
            subject.category = category
            subject.author = request.user
            subject.save()
            post.save()

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
