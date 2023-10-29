import os
import pathlib
import uuid
from urllib.parse import urljoin
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from api.serializers import FileSerializer
from api.models import File, Node, Source, FileGroup
from lib.mimetypes_v2 import mimetypes
from lib.utils import get_client_ip, generate_hmac

__all__ = ['create_file', 'list_file', 'update_file', 'partial_update_file',
           'destroy_file', 'retrieve_file', 'file_exists', 'retrieve_file_url',
           'retrieve_protected_file']


class FilePagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST', ])
def create_file(request, *args, **kwargs):
    try:
        this_node = Node.objects.get(id=settings.NODE_ID)
    except Node.DoesNotExist:
        return Response(f'I don\'t exist...', status=500)

    try:
        source = Source.objects.get(id=request.POST.get('source'))
    except Source.DoesNotExist:
        return Response('source is required', status=400)

    file = request.FILES.get('file')
    if not file:
        return Response(f'file is required', status=400)

    ext = mimetypes.guess_extension(file.content_type)
    if not ext:
        print('**UNKNOWN TYPE ', file.content_type)
        return Response(f'Cannot determine extension for "{file.content_type}"', status=404)

    model = File(source=source)

    group_id = request.POST.get('group_id')
    if group_id:
        try:
            model.group = FileGroup.objects.get(pk=group_id)
        except FileGroup.DoesNotExist:
            g = FileGroup(id=group_id or uuid.uuid4().hex)
            g.save()
            model.group = g

    filename = request.POST.get('filename') or uuid.uuid4().hex + ext
    directory = os.path.join(source.directory,
                             pathlib.Path(request.POST.get('path')),
                             model.group.id if model.group else '',
                             )
    abspath = os.path.join(directory, filename)
    path = abspath.replace('\\', '/')

    if is_traversal_path(abspath):
        if model.group:
            model.group.delete()
        return Response('Tryin\' to heck huh?', status=403)

    model.file = file
    model.path = path
    model.save()
    model.replicas.add(this_node)

    serializer = FileSerializer(model)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', ])
def list_file(request):
    queryset = File.objects.all().order_by(request.GET.get('order_by', 'id'))
    paginator = FilePagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = FileSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT', ])
def update_file(request, pk=None):
    snippet = File.objects.get(pk=pk)
    serializer = FileSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', ])
def partial_update_file(request, pk=None):
    snippet = File.objects.get(pk=pk)
    serializer = FileSerializer(snippet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def retrieve_protected_file(request, hmac_key, filename):
    response = HttpResponse()
    ip = get_client_ip(request)
    new_hmac_key = File.generate_hmac(ip)
    response["Content-Disposition"] = f'attachment; filename={filename}'
    response['X-Accel-Redirect'] = '/protected/' + filename
    return Response()


@api_view(['GET', ])
def retrieve_file_url(request, pk):
    try:
        file = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return Response('File not found', status=404)

    group_permission = request.GET.get('group_permission')

    if file.protected:
        ip = get_client_ip(request)
        path, filename = os.path.split(file.path)
        if group_permission and file.group:
            hmac_key = generate_hmac(ip, path)
            cache.set(hmac_key, file.path, settings.FILE_CACHE_TIMEOUT)
        replica = file.random_replica()
        url = urljoin(replica.static_url, f'{hmac_key}/{os.path.split(file.path)[1]}')
    else:
        replica = file.random_replica()
        url = urljoin(replica.static_url, file.path)
    return Response(url)


@api_view(['GET', ])
def retrieve_file(request, pk):
    file = File.objects.get(pk=pk)
    serializer = FileSerializer(file)
    return Response(serializer.data)


@api_view(['GET', ])
def file_exists(request, pk):
    file = File.objects.get(pk=pk)
    return Response(os.path.exists(os.path.join(settings.DATA_DIR, file.path)))


@api_view(['DELETE', ])
def destroy_file(request, pk):
    snippet = File.objects.get(pk=pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# def start_replication(file):
#     node = Node.objects.get(id=settings.NODE_ID)
#     channel = rabbitmq.channel()
#     channel.exchange_declare(exchange='file_replication_tasks', exchange_type='direct')
#     for replication in Replication.objects.filter(source=file.source, replicate=True).exclude(node=node):
#         channel.basic_publish(exchange='file_replication_tasks', routing_key=replication.node.id, body=file.id)


def is_traversal_path(filename):
    data_dir = settings.DATA_DIR
    filepath = os.path.join(data_dir, filename)
    requested_path = os.path.relpath(filepath, start=data_dir)
    requested_path = os.path.normpath(os.path.join(data_dir, requested_path))
    common_prefix = os.path.commonpath([requested_path, data_dir])
    return str(common_prefix) != str(data_dir)

