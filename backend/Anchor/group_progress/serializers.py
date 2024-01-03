from rest_framework import serializers
from .models import GroupMemberProgress


class GroupMemberProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMemberProgress
        fields = ["id", "user", "group", "progress", "updated_at"]
