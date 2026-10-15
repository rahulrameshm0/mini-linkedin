from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class AccountTests(TestCase):
    def test_delete_account_requires_confirmation_and_password(self):
        user = User.objects.create_user('alice', password='Strong-pass19')
        self.client.force_login(user)
        url = reverse('delete_account')
        self.assertContains(self.client.get(url), 'Permanently delete my account')
        self.client.post(url, {'password': 'wrong', 'confirm': 'on'})
        self.client.post(url, {'password': 'Strong-pass19'})
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_delete_account_removes_owned_activity_and_logs_out(self):
        from posts.models import Post, Comment
        user = User.objects.create_user('alice', password='Strong-pass19')
        other = User.objects.create_user('bob', password='Strong-pass19')
        profile, _ = Profile.objects.get_or_create(user=user)
        other_profile, _ = Profile.objects.get_or_create(user=other)
        other_profile.following.add(profile)
        own_post = Post.objects.create(user=user, content='My post')
        other_post = Post.objects.create(user=other, content='Other post')
        other_post.likes.add(user)
        Comment.objects.create(user=user, post=other_post, content='My comment')
        self.client.force_login(user)
        self.assertRedirects(self.client.post(reverse('delete_account'), {
            'password': 'Strong-pass19', 'confirm': 'on', 'user_id': other.pk,
        }), reverse('signin'))
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
        self.assertTrue(User.objects.filter(pk=other.pk).exists())
        self.assertFalse(Profile.objects.filter(pk=profile.pk).exists())
        self.assertFalse(Post.objects.filter(pk=own_post.pk).exists())
        self.assertTrue(Post.objects.filter(pk=other_post.pk).exists())
        self.assertFalse(Comment.objects.filter(user_id=user.pk).exists())
        self.assertFalse(other_post.likes.exists())
        self.assertFalse(other_profile.following.exists())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_delete_account_requires_login_and_csrf(self):
        from django.test import Client
        url = reverse('delete_account')
        self.assertRedirects(self.client.get(url), reverse('signin') + '?next=' + url)
        user = User.objects.create_user('alice', password='Strong-pass19')
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        self.assertEqual(client.post(url, {'password': 'Strong-pass19', 'confirm': 'on'}).status_code, 403)
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_signup_and_duplicate_email(self):
        data = {'username': 'newperson', 'email': 'person@example.com', 'password1': 'Unique-phrase-738!', 'password2': 'Unique-phrase-738!'}
        self.assertRedirects(self.client.post(reverse('signup'), data), reverse('dashboard'))
        self.assertTrue(Profile.objects.filter(user__username='newperson').exists())
        self.client.post(reverse('logout'))
        data['username'] = 'another'
        data['email'] = 'PERSON@example.com'
        self.assertContains(self.client.post(reverse('signup'), data), 'already uses this email')
        self.assertEqual(User.objects.count(), 1)

    def test_follow_and_profile(self):
        a = User.objects.create_user('alice', password='pass')
        b = User.objects.create_user('bob', password='pass')
        self.client.force_login(a)
        self.client.post(reverse('follow', args=['bob']))
        self.assertTrue(a.profile.following.filter(user=b).exists())
        self.client.post(reverse('follow', args=['bob']))
        self.assertFalse(a.profile.following.exists())
        self.client.post(reverse('follow', args=['alice']))
        self.assertFalse(a.profile.following.exists())
        self.client.post(reverse('edit_profile'), {'headline': 'Engineer', 'location': 'Delhi', 'bio': 'Building things'})
        self.assertContains(self.client.get(reverse('profile', args=['alice'])), 'Engineer')

    def test_login_and_post_only_logout(self):
        User.objects.create_user('member', password='Strong-pass19')
        self.assertEqual(self.client.get(reverse('signin')).status_code, 200)
        self.assertRedirects(self.client.post(reverse('signin'), {'username': 'member', 'password': 'Strong-pass19'}), reverse('dashboard'))
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
