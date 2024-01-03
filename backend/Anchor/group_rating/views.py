# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import GroupMemberRating, Group
from .serializers import GroupMemberRatingSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def group_member_rating(request, group_id):
    if request.method == "GET":
        ratings = GroupMemberRating.objects.filter(group_id=group_id)
        serializer = GroupMemberRatingSerializer(ratings, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        data["rated_by"] = request.user.id
        data["group"] = group_id

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response(
                {"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the rated_member is part of the group
        rated_member_id = data.get("rated_member")
        if not group.members.filter(user_id=rated_member_id).exists():
            return Response(
                {"error": "Rated member is not part of the group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = GroupMemberRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
