from rest_framework import serializers


class GeneratePlanSerializer(serializers.Serializer):
    block_code = serializers.CharField(max_length=32)


class DispatchPlanSerializer(serializers.Serializer):
    plan_code = serializers.CharField(max_length=40)
