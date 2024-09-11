from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from xml.etree.ElementTree import Element, SubElement, tostring
import uuid
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_product.models import ProductCatalog, Fsp


class GenerateXMLForDecommissionView(APIView):
    """
    API View to generate XML for product decommissioning and simulate sending to third-party system.
    """

    @swagger_auto_schema(
        operation_description="Generate XML for product decommissioning",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the product to decommission')
            },
            required=['id']
        ),
        responses={
            200: openapi.Response(description="Data sent successfully (simulated)"),
            404: openapi.Response(description="Product not found"),
            500: openapi.Response(description="Failed to send data to third-party system")
        }
    )
    def post(self, request):
        # Get the product ID from the request data
        product_id = request.data.get("id")

        # Retrieve the product instance
        product = get_object_or_404(ProductCatalog, pk=product_id)

        # Retrieve the Fsp instance dynamically
        fsp = Fsp.objects.all().first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        ProductCatalog.objects.filter(pk=product_id).update(status=False)

        # Generate XML data for API call
        xml_data = self.generate_xml_for_decommission(product, fsp)

        # Simulate the API call to the third-party system
        response = self.send_to_third_party(xml_data)

        if response.status_code == 200:
            return Response({"message": "Data sent successfully (simulated)"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send data to third-party system."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def generate_xml_for_decommission(self, product, fsp):
        """
        Generate XML data for product decommission message.
        """
        # Create the root element
        document = Element("Document")
        data_elem = SubElement(document, "Data")

        # Create the header element
        header = SubElement(data_elem, "Header")
        SubElement(header, "Sender").text = fsp.name  # Get Sender from Fsp model
        SubElement(header, "Receiver").text = "ESS_UTUMISHI"
        SubElement(header, "FSPCode").text = fsp.code  # Get FSPCode from Fsp model
        SubElement(header, "MsgId").text = str(uuid.uuid4())  # Generate unique MsgId
        SubElement(header, "MessageType").text = "PRODUCT_DECOMMISSION"

        # Add the product code to the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "ProductCode").text = product.ProductCode

        # Add the Signature element
        SubElement(document, "Signature").text = "XYZ"

        # Convert the Element to a string
        xml_string = tostring(document, encoding="utf-8").decode("utf-8")
        return xml_string

    def send_to_third_party(self, xml_data):
        """
        Simulate sending data to a third-party system.
        """
        # Simulate the response
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status_code = 200  # Simulating a successful response
        mock_response.content = "Data sent successfully (simulated)"
        return mock_response