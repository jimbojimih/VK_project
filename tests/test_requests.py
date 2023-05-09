from rest_framework.test import APITestCase, APIRequestFactory
from django.test import Client
from VK_app.models import Friendship
from django.contrib.auth.models import User


class URLTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='one', password='one')
        self.user2 = User.objects.create_user(username='two', password='two') 
        self.user3 = User.objects.create_user(username='three', password='three') 
        self.user4 = User.objects.create_user(username='four', password='four')    
        self.auth_guest1, self.auth_guest2 = Client(), Client()

        self.auth_guest1.force_login(self.user1) #autohorized client1
        self.auth_guest2.force_login(self.user2) #autohorized client2
        self.guest = Client() #unautohorized client 

        self.users_urls, self.friendships_url = '/users/', '/users/friendships/'
            
    def test_create_account(self):
        request = self.guest.post(self.users_urls, {'username': 'testcreate', 'password': 'testcreate'})
        self.assertEqual(request.status_code, 201)
        self.assertEqual(User.objects.get(username='testcreate').username, 'testcreate') 
        User.objects.get(username='testcreate').delete() 

    def test_creating_an_outgoing_request(self):
        request = self.auth_guest1.post(self.friendships_url, {'friend': self.user2.id, 'user':1, "status":1})
        self.assertEqual(request.status_code, 201)
        self.assertTrue(Friendship.objects.filter(user=self.user1.id, friend=self.user2.id).exists()) 
        self.assertEqual(Friendship.objects.get(user=self.user1.id, friend=self.user2.id).status, 1)

    def test_a_counter_request(self):
        self.auth_guest1.post(self.friendships_url, {'friend': self.user2.id, 'user':1, "status":1})
        self.auth_guest1.logout()

        request = self.auth_guest2.post(self.friendships_url, {'friend': self.user1.id, 'user':2, "status":1})
        self.assertEqual(request.status_code, 201)
        self.assertTrue(Friendship.objects.filter(user=self.user2.id, friend=self.user1.id).exists())    

        self.assertEqual(Friendship.objects.get(user=self.user1.id, friend=self.user2.id).status, 0)
        self.assertEqual(Friendship.objects.get(user=self.user2.id, friend=self.user1.id).status, 0)
        
        request = self.auth_guest2.get(self.users_urls+'1/')
        self.assertEqual(request.data['status'], 0) #0 means he is a friend       
