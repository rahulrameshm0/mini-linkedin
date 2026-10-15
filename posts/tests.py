from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment

class CommunityTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner', 'owner@example.com', 'A-strong-pass27')
        self.other = User.objects.create_user('other', 'other@example.com', 'A-strong-pass27')
        self.post = Post.objects.create(user=self.owner, content='A professional update')
        self.client.force_login(self.other)

    def test_private_feed(self):
        self.client.logout()
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 302)

    def test_ownership(self):
        self.assertEqual(self.client.post(reverse('edit', args=[self.post.pk]), {'content': 'hacked'}).status_code, 404)
        self.assertEqual(self.client.post(reverse('delete', args=[self.post.pk])).status_code, 404)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'A professional update')

    def test_delete_requires_post(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse('delete', args=[self.post.pk])).status_code, 405)
        self.client.post(reverse('delete', args=[self.post.pk]))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_like_toggle_and_comment_validation(self):
        url = reverse('like', args=[self.post.pk])
        self.client.post(url)
        self.assertEqual(self.post.likes.count(), 1)
        self.client.post(url)
        self.assertEqual(self.post.likes.count(), 0)
        self.client.post(reverse('comment', args=[self.post.pk]), {'content': '   '})
        self.assertEqual(Comment.objects.count(), 0)
        self.client.post(reverse('comment', args=[self.post.pk]), {'content': 'Great idea!'})
        self.assertEqual(Comment.objects.get().user, self.other)

    def test_post_validation_and_edit(self):
        self.assertEqual(self.client.post(reverse('upload_files'), {'content': '  '}).status_code, 400)
        self.client.post(reverse('upload_files'), {'content': 'My first update'})
        post = Post.objects.get(user=self.other)
        self.client.post(reverse('edit', args=[post.pk]), {'content': 'Updated'})
        post.refresh_from_db()
        self.assertEqual(post.content, 'Updated')

    def test_search_and_pages(self):
        response = self.client.get(reverse('dashboard'), {'q': 'professional'})
        self.assertContains(response, 'A professional update')
        self.assertNotContains(self.client.get(reverse('dashboard'), {'q': 'unmatched'}), 'A professional update')
        for name, args in [('network', []), ('profile', ['owner']), ('edit_profile', [])]:
            self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200)

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(reverse('delete', args=[self.post.pk])).status_code, 403)
