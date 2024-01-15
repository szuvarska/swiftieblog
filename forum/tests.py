from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Subject, ForumPost


class ForumViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.subject = Subject.objects.create(title='Test Subject', category=self.category, author=self.user)
        self.post = ForumPost.objects.create(content='Test Content', author=self.user, subject=self.subject)
        self.assertEqual(Subject.objects.count(), 1)
        self.assertEqual(ForumPost.objects.count(), 1)

    def test_forum_view(self):
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum.html')

    def test_category_detail_view(self):
        response = self.client.get(reverse('category_detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/category_detail.html')

    def test_subject_detail_view(self):
        response = self.client.get(reverse('subject_detail', args=[self.subject.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/subject_detail.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/post_detail.html')

    def test_category_detail_post(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('category_detail', args=[self.category.id]),
                                    {'title': 'New Subject', 'post_content': 'New Post'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Subject.objects.count(), 2)

    def test_subject_detail_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('subject_detail', args=[self.subject.id]), {'content': 'New Post'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ForumPost.objects.count(), 2)
