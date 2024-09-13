import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import xmltodict

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanChargeRequestDocumentSerializer


class LoanChargesRequestAPIView(APIView):
    @swagger_auto_schema(
        operation_description="API to receive loan charges request in XML format",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_BINARY,
            description="XML data representing loan charges request"
        ),
        responses={200: "Successfully processed the request", 400: "Invalid data"}
    )
    def post(self, request, *args, **kwargs):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response(
                {'error': 'Content-Type must be application/xml'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Use the cached body instead of accessing request.body directly
        try:
            xml_data = request.body_cache.decode('utf-8').strip()
            xml_data = re.sub(r'>\s+<', '><', xml_data)
            if not xml_data:
                raise ValueError("Empty request body")
        except Exception as e:
            return Response(
                {'error': f'Invalid XML data in request body: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Convert XML data to a dictionary
        try:
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response(
                {'error': f'Failed to parse XML: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Extract data for saving to the ApiRequest model
        document_data = data_dict.get('Document')
        if not document_data:
            return Response(
                {'error': 'Document node is missing in the XML data.'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Save the request data to the ApiRequest model

        try:
            log_and_make_api_call(
                request_type="inward",
                payload=xml_data,
                signature="XYZ",  # Replace with actual signature if available
                url="https://third-party-api.example.com/endpoint"
                # Replace with actual endpoint URL
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to save API request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/xml'
            )

        data_for_serialization = {
            'Header': document_data.get('Data', {}).get('Header', {}),
            'MessageDetails': document_data.get('Data', {}).get('MessageDetails', {}),
            'Signature': document_data.get('Signature', '')
        }

        # Validate the extracted data using the serializer
        serializer = LoanChargeRequestDocumentSerializer(data=data_for_serialization)

        if serializer.is_valid():
            # Simulate successful processing of the request
            simulated_response = {
                'message': 'Simulated: Loan charges request received and processed successfully.',
                'received_data': document_data  # Display the received data
            }
            return Response(simulated_response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
