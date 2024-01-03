from django.db import models
from user.models import User


class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.title}"
