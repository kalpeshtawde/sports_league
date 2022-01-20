from django.db import models

from account.models import User


class Messaging(models.Model):
    message = models.TextField()

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_user_one'
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_user_two'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
