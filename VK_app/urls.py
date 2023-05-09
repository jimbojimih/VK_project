from django.contrib import admin
from django.urls import path, include
from .views import UserView, FriendshipView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'friendships', FriendshipView)
router.register(r'', UserView)

urlpatterns = [
    path('drf_auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
