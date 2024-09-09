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
        operation_description="API to receive product catalog in XML format",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Document': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'Header': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'Sender': openapi.Schema(type=openapi.TYPE_STRING),
                                'Receiver': openapi.Schema(type=openapi.TYPE_STRING),
                                'FSPCode': openapi.Schema(type=openapi.TYPE_STRING),
                                'MsgId': openapi.Schema(type=openapi.TYPE_STRING),
                                'MessageType': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                        'MessageDetails': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'ProductCode': openapi.Schema(type=openapi.TYPE_STRING),
                                    'ProductName': openapi.Schema(type=openapi.TYPE_STRING),
                                    'ProductDescription': openapi.Schema(
                                        type=openapi.TYPE_STRING),
                                    'ForExecutive': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'MinimumTenure': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'MaximumTenure': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'InterestRate': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                   format=openapi.FORMAT_DECIMAL),
                                    'ProcessFee': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                 format=openapi.FORMAT_DECIMAL),
                                    'Insurance': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                format=openapi.FORMAT_DECIMAL),
                                    'MaxAmount': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                format=openapi.FORMAT_DECIMAL),
                                    'MinAmount': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                format=openapi.FORMAT_DECIMAL),
                                    'RepaymentType': openapi.Schema(type=openapi.TYPE_STRING),
                                    'Currency': openapi.Schema(type=openapi.TYPE_STRING),
                                    'TermsCondition': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'TermsConditionNumber': openapi.Schema(
                                                    type=openapi.TYPE_STRING),
                                                'Description': openapi.Schema(
                                                    type=openapi.TYPE_STRING),
                                                'TCEffectiveDate': openapi.Schema(
                                                    type=openapi.TYPE_STRING,
                                                    format=openapi.FORMAT_DATE)
                                            }
                                        )
                                    ),
                                }
                            )
                        ),
                        'Signature': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            }
        ),
        responses={200: DocumentSerializer(many=False)},
    )
    def post(self, request, *args, **kwargs):
        # Parse XML to a dictionary
        try:
            xml_data = request.body.decode('utf-8')
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Use Serializer to validate data
        serializer = DocumentSerializer(data=data_dict)
        if serializer.is_valid():
            # Convert the dictionary back to XML format
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
