import xmltodict
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from emkopo_constants.constants import INCOMING
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re

from emkopo_loan.models import AccountValidationRequest
from emkopo_mixins.signature import verify_xml_signature
from ..mixins import log_and_make_api_call
from ..serializers import AccountValidationRequestSerializer


class AccountValidationRequestAPIView(APIView):
    """
    API View to receive XML data from third-party system and insert it into AccountValidationRequest model.
    """

    @swagger_auto_schema(
        operation_description="Receive XML for account validation and insert into AccountValidationRequest model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description='XML payload with account validation details',
        ),
        responses={
            200: openapi.Response(description="Data successfully inserted into AccountValidationRequest."),
            400: openapi.Response(description="Bad request: Invalid XML or missing fields."),
        }
    )
    def post(self, request):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response({"error": "Content-Type must be application/xml"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the XML data from the request body
        try:
            xml_data = request.body_cache.decode('utf-8').strip()
            if not xml_data:
                raise ValueError("Empty request body")

            # Remove whitespace between XML tags
            xml_data = re.sub(r'>\s+<', '><', xml_data)
        except Exception as e:
            return Response(
                {'error': f'Invalid XML data in request body: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        if not settings.EMKOPO_SIT:
            # Verify the XML signature before proceeding
            if not verify_xml_signature(xml_data):
                return Response({"error": "Signature verification failed"},
                                status=status.HTTP_400_BAD_REQUEST)

        # Convert XML data to a dictionary
        try:
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response(
                {'error': f'Failed to parse XML: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        return account_validation_request(data_dict, xml_data)

def account_validation_request(data_dict, xml_data):
    # Extract 'Document' data to pass to the serializer
    document_data = data_dict.get('Document')
    if not document_data:
        return Response(
            {'error': 'Document node is missing in the XML data.'},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/xml'
        )

    # Extract Header and MessageDetails
    header_data = document_data.get('Data', {}).get('Header', {})
    message_details = document_data.get('Data', {}).get('MessageDetails', {})
    try:
        log_and_make_api_call(
            request_type=INCOMING,
            payload=xml_data,
            signature=settings.ESS_SIGNATURE,
            url=settings.ESS_UTUMISHI_API
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to save API request: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/xml'
        )

    # Combine Header and MessageDetails for serialization
    combined_data = {**header_data, **message_details,
                     'Signature': document_data.get('Signature', '')}
    # Extract the relevant fields from the XML and map them to the request data
    try:
        # Pass the dictionary data to the serializer
        serializer = AccountValidationRequestSerializer(data=combined_data)
        # Validate and save the data
        if serializer.is_valid():
            AccountValidationRequest.objects.create(
                AccountNumber=serializer.validated_data.get('AccountNumber'),
                FirstName=serializer.validated_data.get('FirstName'),
                MiddleName=serializer.validated_data.get('MiddleName'),
                LastName=serializer.validated_data.get('LastName'),
                MessageType=header_data.get('MessageType'),
                RequestType=INCOMING,
            )
            return Response(
                {"message": "Data successfully inserted into AccountValidationRequest."},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except AttributeError as e:
        return Response({"error": "Missing required fields", "details": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

