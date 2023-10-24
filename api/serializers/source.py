from rest_framework import serializers
from api.models import Source


class SourceSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    directory = serializers.CharField()
    max_replicas = serializers.IntegerField()

    class Meta:
        model = Source
        fields = ('id', 'directory', 'max_replicas')
