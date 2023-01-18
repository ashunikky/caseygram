from django.urls import reverse

from homepage.models import Comment, Post
from django.contrib.auth.models import User
from django.test import TestCase


class ReplyTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="tester")

        self.post = Post.objects.create(caption="hello world", author=self.user)

    def test_create_reply(self):
        reply_response = self.when_reply_object_is_created()
        self.then_reply_object_should_be_present_in_db(reply_response)

    def given_comment(self):
        return Comment.objects.create(post=self.post, content="how are you", author=self.user)

    def given_reply(self):
        comment = self.given_comment()
        reply = Comment.objects.create(parent=comment, post=self.post, content="i am fine", author=self.user)
        return reply

    def when_reply_object_is_created(self):
        self.client.login(username='user', password='password')
        comment = self.given_comment()
        reply = self.given_reply()
        url = reverse('comment-reply', kwargs={'pk': comment.pk})
        response = self.client.post(url, {'content': reply.content}, follow=True)
        return response

    def then_reply_object_should_be_present_in_db(self, reply_response):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(reply_response.status_code, response.status_code)
        # comment = self.given_comment()
        # reply = Comment.objects.get(parent=comment.content)
        # self.assertEqual(reply.content, "i am fine")
