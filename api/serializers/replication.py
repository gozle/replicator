from rest_framework import serializers
from api.models import Source, Node


class ReplicationSerializer(serializers.ModelSerializer):
    source = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    nodes = serializers.SerializerMethodField()
    replicate = serializers.BooleanField(default=True)

    def get_nodes(self, obj):
        return Node(obj.nodes, many=True).data

    class Meta:
        model = Source
        fields = ('nodes', 'source', 'replicas')
