from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article
from .forms import CustomSignupForm


class ForumViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.article = Article.objects.create(title='Test Article', content='Test Content', author_id=self.user.id, picture="article_images/taylor-swift-little-lies-dress-new-york-011024_1122-e334ee7d4a064bd78526_yrcotMk.webp")

    def test_main_page(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_user_account_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_account.html')

    def test_user_account_unauthenticated(self):
        response = self.client.get(reverse('user_account'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_article_page(self):
        response = self.client.get(reverse('article', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article.html')

    def test_custom_signup_view(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        self.assertIsInstance(response.context['form'], CustomSignupForm)

    def test_custom_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)

    def test_confirmation_signup(self):
        response = self.client.get(reverse('account_confirmation_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/confirmation_signup.html')
