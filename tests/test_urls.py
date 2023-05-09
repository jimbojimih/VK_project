from rest_framework.test import APITestCase
from django.test import Client
from VK_app.models import Friendship
from django.contrib.auth.models import User


class URLTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username = 'one', password = 'one')   
        self.autohorized_guest = Client()

        self.autohorized_guest.force_login(self.user) #autohorized client
        self.guest = Client() #unautohorized client     
            
    def test_unautohorized_200(self):
        urls = ['/users/', '/users/friendships/', ]
        response = self.guest.get(urls[0])
        self.assertEqual(response.status_code, 200) 
        response = self.guest.get(urls[1])
        self.assertEqual(response.status_code, 403)    
    
    def test_autohorized_200(self):
        urls = ['/users/', '/users/friendships/', ]
        for u in urls:
            with self.subTest(u=u):
                response  = self.autohorized_guest.get(u)
                self.assertEqual(response.status_code, 200)
