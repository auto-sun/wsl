from rest_framework import serializers


class DeviceCodeSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=32)


class DeviceCommandSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=32)
    command = serializers.CharField(max_length=64, required=False, allow_blank=True)
