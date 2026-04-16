from rest_framework import serializers


class DiagnosisUploadSerializer(serializers.Serializer):
    image = serializers.FileField()
