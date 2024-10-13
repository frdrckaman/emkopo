import xmltodict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanRepaymentRequestSerializer
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanRepaymentRequest


class LoanRepaymentRequestAPIView(APIView):
    """
    API View to receive XML data for loan repayment request and insert it into the LoanRepaymentRequest model.
    """

    @swagger_auto_schema(
        operation_description="Receive XML for loan repayment request and insert into LoanRepaymentRequest model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description='XML payload with loan repayment request details',
        ),
        responses={
            200: openapi.Response(description="Data successfully inserted into LoanRepaymentRequest."),
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

            # Convert XML data to a dictionary
        try:
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response(
                {'error': f'Failed to parse XML: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

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

        # Combine Header and MessageDetails for serialization
        combined_data = {**header_data, **message_details, 'Signature': document_data.get(
            'Signature', '')}

        # Pass the dictionary data to the serializer
        serializer = LoanRepaymentRequestSerializer(data=combined_data)

        if serializer.is_valid():
            try:
                LoanRepaymentRequest.objects.create(
                    DeductionCode=serializer.validated_data.get('DeductionCode'),
                    VoteCode=serializer.validated_data.get('VoteCode'),
                    VoteName=serializer.validated_data.get('VoteName'),
                    CheckNumber=serializer.validated_data.get('CheckNumber'),
                    FirstName=serializer.validated_data.get('FirstName'),
                    MiddleName=serializer.validated_data.get('MiddleName'),
                    LastName=serializer.validated_data.get('LastName'),
                    PayDate=serializer.validated_data.get('PayDate'),
                    MessageType=header_data.get('MessageType'),
                    RequestType=INCOMING,
                    status=0
                    # Static value based on the XML structure
                )
                return Response({
                    "message": "Data successfully inserted into LoanLiquidationNotification."},
                    status=status.HTTP_200_OK)

            except AttributeError as e:
                return Response({"error": "Missing required fields", "details": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
        # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
