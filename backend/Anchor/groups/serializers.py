from rest_framework import serializers
from .models import Group
from user.models import User


class GroupSerializer(serializers.ModelSerializer):
    # If you want to display member details instead of just their IDs
    members = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field="username",  # or 'id', depending on what you want to display
    )

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "members",
            "group_goal",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        members_data = validated_data.pop("members")
        group = Group.objects.create(**validated_data)
        for member_data in members_data:
            group.members.add(member_data)
        return group

    def update(self, instance, validated_data):
        members_data = validated_data.pop("members", None)
        instance = super(GroupSerializer, self).update(instance, validated_data)

        if members_data is not None:
            instance.members.clear()
            for member_data in members_data:
                instance.members.add(member_data)

        return instance
