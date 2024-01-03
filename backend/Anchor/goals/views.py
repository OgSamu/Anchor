from rest_framework.decorators import api_view
from django.http import Http404
from .models import Goal, User
from .serializers import GoalSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema


@api_view(["GET", "POST"])
def goalsList(request, pk=None):
    if request.method == "POST":
        serializer = GoalSerializer(data=request.data)
        if serializer.is_valid():
            goal = serializer.save()
            return Response(
                {"message": "Goal created successfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print("i got here to get some goals for a speicifc user")
        try:
            if pk:
                goals = Goal.objects.filter(user__user_id=pk)
                print("user pk", request.user.user_id)
                if request.user.is_authenticated and request.user.user_id == pk:
                    goals = goals
                    print("i got here", goals)
                else:
                    goals = goals.filter(visibility="public")

                goals = goals.order_by("-start_date")

                page = request.query_params.get("page", 1)
                size = request.query_params.get("size", 10)
                paginator = Paginator(goals, size)

                try:
                    goalReturn = paginator.page(page)
                except PageNotAnInteger:
                    goalReturn = paginator.page(1)
                except EmptyPage:
                    goalReturn = paginator.page(paginator.num_pages)

                serializer = GoalSerializer(goalReturn, many=True)

                return Response(
                    {"type": "publicgoals", "items": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "No goals found"}, status=status.HTTP_404_NOT_FOUND
            )

        except ObjectDoesNotExist:
            raise NotFound(detail="Author not found", code=404)
