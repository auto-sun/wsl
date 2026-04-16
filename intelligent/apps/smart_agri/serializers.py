from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)


class DetectionUploadSerializer(serializers.Serializer):
    image = serializers.FileField()
    plot_code = serializers.CharField(max_length=32, required=False, allow_blank=True)
    remarks = serializers.CharField(required=False, allow_blank=True, max_length=200)
