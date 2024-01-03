# serializers.py

from rest_framework import serializers
from .models import GroupMemberRating


class GroupMemberRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMemberRating
        fields = ["id", "rated_by", "rated_member", "group", "rating", "comment"]
