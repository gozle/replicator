from rest_framework import serializers
from api.models import Source, Node


class ReplicationSerializer(serializers.ModelSerializer):
    node = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    replicate = serializers.BooleanField(default=True)
    sources = serializers.SerializerMethodField()

    def get_sources(self, obj):
        return Source(obj.sources, many=True).data

    class Meta:
        model = Source
        fields = ('id', 'node', 'max_replicas')
