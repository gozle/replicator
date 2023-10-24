from rest_framework import serializers
from api.models import Node, Source


class NodeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    api_url = serializers.SerializerMethodField()

    def get_api_url(self, obj):
        return obj.api_url

    class Meta:
        model = Node
        fields = ('id', 'api_url')
