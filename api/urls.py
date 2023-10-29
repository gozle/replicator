from django.urls import path
from api import views


urlpatterns = [
    path('nodes', views.list_node),
    path('nodes/add', views.create_node),
    path('nodes/<str:pk>/get', views.retrieve_node),
    path('nodes/<str:pk>/update', views.update_node),
    path('nodes/<str:pk>/partial_update', views.partial_update_node),
    path('nodes/<str:pk>/delete', views.destroy_node),

    path('file_groups', views.list_file_group),
    path('file_groups/add', views.create_file_group),
    path('file_groups/<int:pk>/get', views.retrieve_file_group),
    path('file_groups/<int:pk>/update', views.update_file_group),
    path('file_groups/<int:pk>/partial_update', views.partial_update_file_group),
    path('file_groups/<int:pk>/delete', views.destroy_file_group),

    path('sources', views.list_source),
    path('sources/add', views.create_source),
    path('sources/<str:pk>/get', views.retrieve_source),
    path('sources/<str:pk>/update', views.update_source),
    path('sources/<str:pk>/partial_update', views.partial_update_source),
    path('sources/<str:pk>/delete', views.destroy_source),
    path('sources/<str:pk>/nodes', views.list_source_nodes),
    path('sources/<str:pk>/node', views.get_source_node),

    path('files', views.list_file),
    path('files/add', views.create_file),
    path('files/<int:pk>/url', views.retrieve_file_url),
    path('files/<int:pk>/get', views.retrieve_file),
    path('files/<int:pk>/exists', views.file_exists),
    path('files/<int:pk>/update', views.update_file),
    path('files/<int:pk>/partial_update', views.partial_update_file),
    path('files/<int:pk>/delete', views.destroy_file),

    path('protected/<str:hmac_key>/<str:filename>', views.retrieve_protected_file),
]


