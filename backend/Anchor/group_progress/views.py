from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import GroupMemberProgress, Group
from .serializers import GroupMemberProgressSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAuthenticated])
def group_member_progress(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is a member of the group
    if not group.members.filter(id=request.user.id).exists():
        return Response(
            {"error": "User not a member of the group"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        # Possibly restrict this to only be accessible by group admins or the individual user
        progress = GroupMemberProgress.objects.filter(group=group)
        serializer = GroupMemberProgressSerializer(progress, many=True)
        return Response(serializer.data)

    elif request.method in ["POST", "PUT"]:
        data = request.data
        data["user"] = request.user.id
        data["group"] = group_id

        progress_value = data.get("progress")
        if progress_value is None or not 0 <= progress_value <= 100:
            return Response(
                {"error": "Invalid progress value"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GroupMemberProgressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                if request.method == "POST"
                else status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
