from django.db import models
from user.models import User
from groups.models import Group


class GroupMemberProgress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_progress"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="member_progress"
    )
    progress = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress in {self.group.name}"
