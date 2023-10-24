import random
from rest_framework import serializers
from api.models import File, Source, FileGroup
from urllib.parse import urljoin


class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    source = serializers.PrimaryKeyRelatedField(queryset=Source.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=FileGroup.objects.all(), required=False)
    url = serializers.SerializerMethodField('get_valid_url')
    created_at = serializers.DateTimeField(required=False)

    @staticmethod
    def get_valid_url(obj):
        replications = obj.replications.all()
        if not replications:
            return None
        replication = random.choice(replications)
        return urljoin(replication.node.base_url, obj.node.path)

    class Meta:
        model = File
        fields = ('id', 'source', 'group', 'url', 'created_at')
