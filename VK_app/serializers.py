from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Friendship
        fields = ("id", "status", "user", "friend") 
   
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    incoming_requests = serializers.SerializerMethodField()
    outgoing_requests = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "password", "friends", 
                  'incoming_requests', 'outgoing_requests', "status")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        
        return user

    def get_incoming_requests(self, instance):
        incoming_requests = instance.incoming_requests.filter(status=1)
        return FriendshipSerializer(incoming_requests, many=True).data

    def get_outgoing_requests(self, instance):
        outgoing_requests = instance.outgoing_requests.filter(status=1)
        return FriendshipSerializer(outgoing_requests, many=True).data

    def get_friends(self, instance):
        '''
        Сrutch. Тк одобренная заявка может быть одна (в одну сторону)
        или же может существовать так же встречная, пока так,
        необходимо найти более чистый способ.
        '''
        friends_in = instance.incoming_requests.filter(status=0) 
        friends_out = instance.outgoing_requests.filter(status=0)
        in_ = [{"id":u.id, "id_user":u.user.id, "user":u.user.username} 
                for u in friends_in if u.user != instance]
        out = [{"id":u.id, "id_user":u.friend.id, "user":u.friend.username} 
                for u in friends_out if u.friend != instance]
        prev, ans = None, []
        for i in (in_ + out):
            if i['user'] == prev:
                continue
            prev = i['user']
            ans.append(i)
        return ans

    def get_status(self, instance):
        if self.context['request'].user.is_authenticated:
            user = self.context['request'].user
            status_in = instance.outgoing_requests.filter(friend=user).exists()
            status_out = user.outgoing_requests.filter(friend=instance).exists()
            
            if not status_in and not status_out or user == instance:
                return None

            elif status_in and status_out:
                return instance.outgoing_requests.get(friend=user).status

            elif status_in:
                return instance.outgoing_requests.get(friend=user).status

            elif status_out:
                return -user.outgoing_requests.get(friend=instance).status


        
