import xmltodict
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import PartialLoanRepaymentRequestSerializer
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import PartialLoanRepaymentRequest


class PartialLoanRepaymentRequestAPIView(APIView):
    """
    API View to receive XML data for partial loan repayment request and insert it into the PartialLoanRepaymentRequest model.
    """

    @swagger_auto_schema(
        operation_description="Receive XML for partial loan repayment request and insert into PartialLoanRepaymentRequest model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description='XML payload with partial loan repayment request details',
        ),
        responses={
            200: openapi.Response(description="Data successfully inserted into PartialLoanRepaymentRequest."),
            400: openapi.Response(description="Bad request: Invalid XML or missing fields."),
        }
    )
    def post(self, request):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response({"error": "Content-Type must be application/xml"}, status=status.HTTP_400_BAD_REQUEST)

        # Decode and clean up the XML data
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
        return partial_loan_repayment_request(data_dict, xml_data)

def partial_loan_repayment_request(data_dict, xml_data):
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

    try:
        # Pass the dictionary data to the serializer
        serializer = PartialLoanRepaymentRequestSerializer(data=combined_data)

        # Validate and save the data
        if serializer.is_valid():
            PartialLoanRepaymentRequest.objects.create(
                CheckNumber=serializer.validated_data.get('CheckNumber'),
                FirstName=serializer.validated_data.get('FirstName'),
                MiddleName=serializer.validated_data.get('MiddleName'),
                LastName=serializer.validated_data.get('LastName'),
                VoteCode=serializer.validated_data.get('VoteCode'),
                VoteName=serializer.validated_data.get('VoteName'),
                DeductionAmount=serializer.validated_data.get('DeductionAmount'),
                DeductionCode=serializer.validated_data.get('DeductionCode'),
                DeductionName=serializer.validated_data.get('DeductionName'),
                DeductionBalance=serializer.validated_data.get('DeductionBalance'),
                FSPCode=serializer.validated_data.get('FSPCode'),
                PaymentOption=serializer.validated_data.get('PaymentOption'),
                Intention=serializer.validated_data.get('Intention'),
                AmountToPay=serializer.validated_data.get('AmountToPay'),
                MessageType=header_data.get('MessageType'),
                RequestType=INCOMING,
            )
            return Response(
                {"message": "Data successfully inserted into PartialLoanRepaymentRequest."},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except AttributeError as e:
        return Response({"error": "Missing required fields", "details": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

