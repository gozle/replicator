from rest_framework import serializers
from api.models import FileGroup
from api.serializers.file import FileSerializer


class FileGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    files = serializers.SerializerMethodField()

    def get_files(self, obj):
        return FileSerializer(obj.files, many=True).data

    class Meta:
        fields = ('id', 'files')
        model = FileGroup
