from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.exceptions import NotFound
from .models import Group
from .serializers import GroupSerializer


@api_view(["GET", "POST"])
def group_list(request):
    if request.method == "GET":
        groups = Group.objects.all().order_by("-created_at")
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 10)
        paginator = Paginator(groups, size)

        try:
            groups_page = paginator.page(page)
        except PageNotAnInteger:
            groups_page = paginator.page(1)
        except EmptyPage:
            groups_page = paginator.page(paginator.num_pages)

        serializer = GroupSerializer(groups_page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def group_detail(request, pk):
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        raise NotFound(detail="Group not found", code=404)

    if request.method == "GET":
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
