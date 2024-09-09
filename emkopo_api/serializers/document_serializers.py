from rest_framework import serializers

from emkopo_api.serializers import HeaderSerializer, ProductCatalogSerializer


class DocumentSerializer(serializers.Serializer):
    Header = HeaderSerializer()
    MessageDetails = ProductCatalogSerializer(many=True)
    Signature = serializers.CharField(max_length=100)
