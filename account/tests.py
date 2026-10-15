from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class AccountTests(TestCase):
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
