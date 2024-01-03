from django.db import models
import uuid
from user.models import User
from goals.models import Goal


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(User, related_name="member_groups")

    # One-to-One relationship with a Goal
    # we assume below that a group has one collective goal
    # If a group can have multiple goals, we gonna switch latr to  Many-to-Many relationship
    group_goal = models.ForeignKey(
        Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name="group"
    )

    def __str__(self):
        return self.name
