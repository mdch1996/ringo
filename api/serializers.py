from rest_framework import serializers


class SwitchSerializer(serializers.Serializer):
    device = serializers.IntegerField()
    key = serializers.BooleanField()
