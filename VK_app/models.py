from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):

    class Status(models.IntegerChoices):
        APPROVE = 0
        REQUEST = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_requests')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_requests')
    status = models.IntegerField(choices=Status.choices, null=True)
