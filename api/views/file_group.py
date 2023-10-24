from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.serializers import FileGroupSerializer
from api.models import FileGroup


__all__ = ['create_file_group', 'list_file_group', 'update_file_group', 'partial_update_file_group',
           'destroy_file_group', 'retrieve_file_group']


class FileGroupPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST', ])
def create_file_group(request, *args, **kwargs):
    serializer = FileGroupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def list_file_group(request):
    queryset = FileGroup.objects.all().order_by(request.GET.get('order_by', 'id'))
    paginator = FileGroupPagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = FileGroupSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', ])
def update_file_group(request, pk=None):
    snippet = FileGroup.objects.get(pk=pk)
    serializer = FileGroupSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
def partial_update_file_group(request, pk=None):
    snippet = FileGroup.objects.get(pk=pk)
    serializer = FileGroupSerializer(snippet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def retrieve_file_group(request, pk):
    snippet = FileGroup.objects.get(pk=pk)
    serializer = FileGroupSerializer(snippet)
    return Response(serializer.data)


@api_view(['DELETE', ])
def destroy_file_group(request, pk):
    snippet = FileGroup.objects.get(pk=pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
