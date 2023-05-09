from django.shortcuts import render
from rest_framework import permissions, viewsets, status, views
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from .serializers import UserSerializer, FriendshipSerializer
from .models import Friendship
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(summary='Получить список всех пользователей'),
    create=extend_schema(summary='Создать пользователя'),
    retrieve=extend_schema(summary='Получить информацию об одном пользователе'),
)
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    #http_method_names = ['get', 'post']
    serializer_class = UserSerializer
    
    def create(self, request):
        serializer = UserSerializer(data=request.data) 

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(summary='Получить список всех заявок в друзья'),
    retrieve=extend_schema(summary='Получить информацию об одной заявке в друзья'),
    create=extend_schema(summary='Создать заявку в друзья'),
    update=extend_schema(summary='Принять или отклонить заявку в друзья'),
)
class FriendshipView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]    
    queryset = Friendship.objects.all().order_by('id')
    serializer_class = FriendshipSerializer
    #http_method_names = ['get', 'post', 'put']

    def perform_create(self, serializer):
        user = self.request.user
        friend = serializer.validated_data['friend']

        outgoing_requests = user.outgoing_requests.all()
        incoming_requests = user.incoming_requests.all()

        if outgoing_requests.filter(friend=friend).exists() or friend == user:
            pass

        elif incoming_requests.filter(friend=user, status=1).exists():
            incoming_request = incoming_requests.get(friend=user, status=1)
            incoming_request.status = 0
            incoming_request.save()
            serializer.save(user=user,status=0)

        else:
            serializer.save(user=user,status=1)