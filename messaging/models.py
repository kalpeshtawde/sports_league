from django.db import models
from uuid import uuid4

from account.models import User


class Messaging(models.Model):
    message_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    message = models.TextField()

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        to_field='user_id',
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+',
        to_field='user_id',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
