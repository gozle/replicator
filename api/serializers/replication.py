from rest_framework import serializers
from api.models import Source, Node


class ReplicationSerializer(serializers.ModelSerializer):
    node = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    replicate = serializers.BooleanField(default=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all())

    class Meta:
        model = Source
        fields = ('node', 'replicate', 'source')
