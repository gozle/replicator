from rest_framework import serializers
from api.models import File, Source, FileGroup
from api.serializers.node import NodeSerializer


class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=FileGroup.objects.all(), required=False)
    replicas = serializers.SerializerMethodField()
    url = serializers.URLField()
    created_at = serializers.DateTimeField(required=False)

    @staticmethod
    def get_replicas(obj):
        return NodeSerializer(obj.replicas, many=True).data

    class Meta:
        model = File
        fields = ('id', 'source', 'group', 'replicas', 'url', 'created_at')
