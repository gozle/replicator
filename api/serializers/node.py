from rest_framework import serializers
from api.models import Node, Source


class NodeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    api_url = serializers.URLField()

    class Meta:
        model = Node
        fields = ('id', 'api_url')
