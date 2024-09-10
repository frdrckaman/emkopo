from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xmltodict
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.serializers import DocumentSerializer


class ProductCatalogAPIView(APIView):
    @swagger_auto_schema(
        operation_description="API to receive product details in XML format",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_BINARY,
            description="XML data representing product details and terms & conditions"
        ),
        responses={200: DocumentSerializer(many=False)},
    )
    def post(self, request, *args, **kwargs):
        # Try to read and decode the XML data
        try:
            # Decode the request body as UTF-8 and strip any leading/trailing whitespace
            xml_data = request.body.decode('utf-8').strip()
            if not xml_data:
                raise ValueError("Empty request body")
        except Exception as e:
            return Response(
                {'error': 'Invalid XML data in request body: ' + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Try to parse the XML data to a dictionary
        try:
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response(
                {'error': 'Failed to parse XML: ' + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Validate the data using the serializer
        serializer = DocumentSerializer(data=data_dict)
        if serializer.is_valid():
            # Convert the dictionary back to XML format for the third-party request
            xml_payload = xmltodict.unparse(data_dict, pretty=True)

            # URL of the third-party system
            third_party_url = 'https://third-party-system.com/api/receive-data/'

            # Headers for the request
            headers = {'Content-Type': 'application/xml'}

            # Send the request to the third-party system
            try:
                response = requests.post(third_party_url, data=xml_payload, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                return Response({'message': 'Data successfully sent to third-party system',
                                 'response': response.text}, status=status.HTTP_200_OK)
            except requests.exceptions.RequestException as e:
                return Response({'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

