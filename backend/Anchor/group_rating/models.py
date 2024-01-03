# models.py

from django.db import models
from user.models import User
from groups.models import Group


class GroupMemberRating(models.Model):
    rated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_ratings"
    )
    rated_member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_ratings"
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    rating = models.IntegerField()  #  rating scale of 1-5
    comment = models.TextField(
        blank=True, null=True
    )  # feedback when one user rates the other

    def __str__(self):
        return f"{self.rated_by.username} rates {self.rated_member.username} in {self.group.name}"
