# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Notification
from .serializers import NotificationSerializer


class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by(
            "-created_at"
        )
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        notification.read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
