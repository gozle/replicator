from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.serializers import SourceSerializer, NodeSerializer
from api.models import Source, Node
from services.node_rpc import NodeRpcClient

__all__ = ['create_source', 'list_source', 'update_source', 'partial_update_source',
           'destroy_source', 'retrieve_source', 'get_source_node', 'list_source_nodes']


class SourcePagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST', ])
def create_source(request):
    serializer = SourceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def list_source_nodes(request, pk):
    source = Source.objects.get(pk)
    node = Node.objects.filter(sources__in=[source])
    serializer = NodeSerializer(node, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
def get_source_node(request, pk):
    source = Source.objects.get(pk)
    node_rpc_client = NodeRpcClient()
    node_id = node_rpc_client.call(source.id)
    if not node_id:
        Response(f'No nodes to replicate files from "{source.id}". Add replication for this source', status=404)
    node = Node.objects.get(node_id)
    serializer = NodeSerializer(node)
    return Response(serializer.data)


@api_view(['GET', ])
def list_source(request):
    queryset = Source.objects.all().order_by(request.GET.get('order_by', 'id'))
    paginator = SourcePagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = SourceSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', ])
def update_source(request, pk=None):
    snippet = Source.objects.get(pk=pk)
    serializer = SourceSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
def partial_update_source(request, pk=None):
    snippet = Source.objects.get(pk=pk)
    serializer = SourceSerializer(snippet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def retrieve_source(request, pk):
    snippet = Source.objects.get(pk=pk)
    serializer = SourceSerializer(snippet)
    return Response(serializer.data)


@api_view(['DELETE', ])
def destroy_source(request, pk):
    snippet = Source.objects.get(pk=pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
