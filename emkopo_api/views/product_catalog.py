import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call, convert_to_xml
from emkopo_api.serializers import ProductCatalogSerializer
from emkopo_constants.constants import OUTGOING
from emkopo_product.models import ProductCatalog, Fsp


class ProductCatalogXMLView(APIView):

    @swagger_auto_schema(
        operation_description="Send product catalog data to a third-party system in XML format.",
        responses={
            200: openapi.Response(description="Data sent successfully"),
            500: openapi.Response(description="Failed to send data"),
        },
    )
    def get(self, request):
        return self.product_catalog(request)

    def product_catalog(self, request):
        fsp = Fsp.objects.first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all products from the catalog
        products = ProductCatalog.objects.all()
        serializer = ProductCatalogSerializer(products, many=True)

        # Generate a unique MsgId
        msg_id = str(uuid.uuid4())
        message_type = 'PRODUCT_DETAIL'

        # Convert the serialized data to XML format
        xml_data = convert_to_xml(OUTGOING, message_type, serializer.data, fsp, msg_id)

        # Simulate the API call to the third-party system
        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_data,
            signature=settings.ESS_SIGNATURE,
            url=settings.ESS_UTUMISHI_API
        )

        if response.get('status') == 200:
            return Response({"message": "Data sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('error', 'Failed to send data')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def send_to_third_party(xml_data):
        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_data,
            signature=settings.ESS_SIGNATURE,
            url=settings.ESS_UTUMISHI_API
        )

        if response.get('status') == 200:
            return Response({"message": "Data sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('error', 'Failed to send data')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

