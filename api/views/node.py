from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.serializers import NodeSerializer
from api.models import Node

__all__ = ['create_node', 'list_node', 'update_node', 'partial_update_node',
           'destroy_node', 'retrieve_node']


class NodePagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST', ])
def create_node(request, *args, **kwargs):
    id = request.POST.get('id')
    local_ip = request.POST.get('local_ip')
    api_port = request.POST.get('api_port')
    if not id or not local_ip or not api_port:
        return Response('required fields: id, local_ip, api_port', status=status.HTTP_400_BAD_REQUEST)
    node = Node(id=id, local_ip=local_ip, api_port=api_port)
    try:
        Node.objects.get(id=id)
        return Response('node already exists', status=status.HTTP_400_BAD_REQUEST)
    except Node.DoesNotExist:
        node.save()
    return Response(NodeSerializer(node).data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def list_node(request):
    queryset = Node.objects.all().order_by(request.GET.get('order_by', 'id'))
    paginator = NodePagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = NodeSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', ])
def update_node(request, pk=None):
    snippet = Node.objects.get(pk=pk)
    serializer = NodeSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
def partial_update_node(request, pk=None):
    snippet = Node.objects.get(pk=pk)
    serializer = NodeSerializer(snippet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def retrieve_node(request, pk):
    snippet = Node.objects.get(pk=pk)
    serializer = NodeSerializer(snippet)
    return Response(serializer.data)


@api_view(['DELETE', ])
def destroy_node(request, pk):
    snippet = Node.objects.get(pk=pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
