import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.etree.ElementTree as ET
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from unittest.mock import Mock

from emkopo_api.serializers import ProductCatalogSerializer
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
        # Fetch the Sender and FSPCode from the Fsp model where name = 'Sender' and code = 'FSPCode'
        fsp = Fsp.objects.first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all products from the catalog
        products = ProductCatalog.objects.all()
        serializer = ProductCatalogSerializer(products, many=True)

        # Generate a unique MsgId
        msg_id = str(uuid.uuid4())

        # Convert the serialized data to XML format
        xml_data = self.convert_to_xml(serializer.data, fsp, msg_id)

        # Simulate the API call to the third-party system
        response = self.send_to_third_party(xml_data)

        if response.status_code == 200:
            return Response({"message": "Data sent successfully (simulated)"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send data (simulated)"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def convert_to_xml(self, data, fsp, msg_id):
        # Create the root element
        document = Element("Document")
        data_elem = SubElement(document, "Data")

        # Create the header element
        header = SubElement(data_elem, "Header")
        SubElement(header, "Sender").text = fsp.name  # Get Sender from Fsp model
        SubElement(header, "Receiver").text = "ESS_UTUMISHI"
        SubElement(header, "FSPCode").text = fsp.code  # Get FSPCode from Fsp model
        SubElement(header, "MsgId").text = msg_id  # Use generated unique MsgId
        SubElement(header, "MessageType").text = "PRODUCT_DETAIL"

        # Add each product as a MessageDetails element
        for product in data:
            message_details = SubElement(data_elem, "MessageDetails")
            for key, value in product.items():
                if key == 'terms_conditions':
                    for term in value:
                        term_elem = SubElement(message_details, "TermsCondition")
                        for term_key, term_value in term.items():
                            SubElement(term_elem, term_key).text = str(term_value)
                else:
                    SubElement(message_details, key).text = str(value)

        # Add the Signature element
        SubElement(document, "Signature").text = "XYZ"

        # Convert the Element to a string
        xml_string = tostring(document, encoding="utf-8").decode("utf-8")
        return xml_string

    @staticmethod
    def send_to_third_party(xml_data):
        print(xml_data)
        mock_response = Mock()
        mock_response.status_code = 200  # Simulating a successful response
        mock_response.content = "Data sent successfully (simulated)"
        return mock_response

        # url = 'https://third-party-api.example.com/endpoint'  # Replace with the actual API endpoint
        # headers = {'Content-Type': 'application/xml'}
        #
        # try:
        #     response = requests.post(url, data=xml_data, headers=headers)
        #     return response
        # except requests.exceptions.RequestException as e:
        #     print(f"An error occurred: {e}")
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
