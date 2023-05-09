from rest_framework.test import APITestCase
from VK_app.models import Friendship
from django.contrib.auth.models import User


class ModelsTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username = 'one', password = 'one') 
        self.user2 = User.objects.create_user(
            username = 'two', password = 'two')        
        self.friendship = Friendship.objects.create(user=self.user1, friend = self.user2)

    def test_friendship(self):
        user = self.friendship.user
        friend = self.friendship.friend
        status = self.friendship.status

        self.assertEqual(user, self.user1)
        self.assertEqual(friend, self.user2)

