import base64
import re

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring
import uuid
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import OUTGOING
from emkopo_mixins.signature import load_private_key, sign_data
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
        return self.product_decommission(request)

    def product_decommission(self, request):
        product_id = request.data.get("id")

        fsp = Fsp.objects.all().first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        product = ProductCatalog.objects.get(pk=product_id)

        # Generate XML data for API call
        xml_data = self.generate_xml_for_decommission(product, fsp)

        product.status = False
        product.save()

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
        SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
        SubElement(header, "FSPCode").text = fsp.code  # Get FSPCode from Fsp model
        SubElement(header, "MsgId").text = str(uuid.uuid4())  # Generate unique MsgId
        SubElement(header, "MessageType").text = "PRODUCT_DECOMMISSION"

        # Add the product code to the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "ProductCode").text = product.ProductCode

        # Add the Signature element
        # SubElement(document, "Signature").text = "XYZ"
        #
        # # Convert the Element to a string
        # xml_string = tostring(document, encoding="utf-8").decode("utf-8").strip()
        # xml_data = re.sub(r'>\s+<', '><', xml_string)

        # Convert the XML Element to string (we'll sign this string)
        xml_string = tostring(document, encoding="utf-8").decode("utf-8")

        # Load the private key to sign the data
        private_key = load_private_key(settings.EMKOPO_PRIVATE_KEY)

        # Convert the XML string to bytes
        xml_bytes = xml_string.encode('utf-8')

        # Sign the XML data (xml_bytes) using the private key
        signature = sign_data(private_key, xml_bytes)

        # Encode the signature in base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')

        # Add the Signature element to the document
        SubElement(document, "Signature").text = signature_b64

        # Convert the final XML (with the signature) to string
        final_xml_string = tostring(document, encoding="utf-8").decode("utf-8")

        return final_xml_string
