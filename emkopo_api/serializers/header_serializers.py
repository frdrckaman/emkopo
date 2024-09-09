from rest_framework import serializers


class HeaderSerializer(serializers.Serializer):
    Sender = serializers.CharField(max_length=100)
    Receiver = serializers.CharField(max_length=100)
    FSPCode = serializers.CharField(max_length=10)
    MsgId = serializers.CharField(max_length=50)
    MessageType = serializers.CharField(max_length=50)