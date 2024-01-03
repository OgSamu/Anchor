from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"

    def create(self, validated_data):
        return Goal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.end_date = validated_data.get("end_date", instance.end_date)
        instance.image = validated_data.get("image", instance.image)
        instance.metrics = validated_data.get("metrics", instance.metrics)
        instance.visibility = validated_data.get("visibility", instance.visibility)
        instance.progress = validated_data.get("progress", instance.progress)
        instance.milestones = validated_data.get("milestones", instance.milestones)
        instance.save()
        return instance
