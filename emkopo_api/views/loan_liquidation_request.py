import xmltodict
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import html
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanLiquidationRequestSerializer
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanLiquidationRequest


class LoanLiquidationRequestAPIView(APIView):
    """
    API View to receive and process XML data from a third-party system for Loan Liquidation Request.
    """

    @swagger_auto_schema(
        operation_description="Receive XML for loan liquidation request from third-party system.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description='XML payload with loan liquidation details',
        ),
        responses={
            200: openapi.Response(description="Data successfully inserted into LoanLiquidationRequest."),
            400: openapi.Response(description="Bad request: Invalid XML or missing fields."),
        }
    )
    def post(self, request):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response({"error": "Content-Type must be application/xml"}, status=status.HTTP_400_BAD_REQUEST)

        # Decode and clean the XML data
        try:
            xml_data = html.unescape(request.body_cache.decode('utf-8').strip())
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
                signature=settings.ESS_SIGNATURE,  # Replace with actual signature if available
                url=settings.ESS_UTUMISHI_API
                # Replace with actual endpoint URL
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

        # Validate the data using the serializer
        serializer = LoanLiquidationRequestSerializer(data=combined_data)

        if serializer.is_valid():
            try:
                LoanLiquidationRequest.objects.create(
                    ProductCode=serializer.validated_data.get('ProductCode'),
                    LoanAmount=serializer.validated_data.get('LoanAmount'),
                    DeductionAmount=serializer.validated_data.get('DeductionAmount'),
                    TakeOverBalance=serializer.validated_data.get('TakeOverBalance'),
                    FSP1Code=serializer.validated_data.get('FSP1Code'),
                    FSP1Name=serializer.validated_data.get('FSP1Name'),
                    FSP1LoanNumber=serializer.validated_data.get('FSP1LoanNumber'),
                    FSP1PaymentReferenceNumber=serializer.validated_data.get(
                        'FSP1PaymentReferenceNumber'),
                    NetLoanAmount=serializer.validated_data.get('NetLoanAmount'),
                    TotalAmountToPay=serializer.validated_data.get('TotalAmountToPay'),
                    PaymentRate=serializer.validated_data.get('PaymentRate'),
                    Reserved3=serializer.validated_data.get('Reserved3'),
                    TermsAndConditionsNumber=serializer.validated_data.get('TermsAndConditionsNumber'),
                    ApplicationNumber=serializer.validated_data.get('ApplicationNumber'),
                    FSPReferenceNumber=serializer.validated_data.get('FSPReferenceNumber'),
                    ApproverName=serializer.validated_data.get('ApproverName'),
                    ApproverDesignation=serializer.validated_data.get('ApproverDesignation'),
                    ApproverWorkstation=serializer.validated_data.get('ApproverWorkstation'),
                    ApproverInstitution=serializer.validated_data.get('ApproverInstitution'),
                    ActionDateAndTime=serializer.validated_data.get('ActionDateAndTime'),
                    ContactPerson=serializer.validated_data.get('ContactPerson'),
                    ApprovalReferenceNumber=serializer.validated_data.get('ApprovalReferenceNumber'),
                    Status=serializer.validated_data.get('Status'),
                    Reason=serializer.validated_data.get('Reason'),
                    Comments=serializer.validated_data.get('AdditionalComment'),
                    MessageType=header_data.get('MessageType'),
                    RequestType=INCOMING,
                )

                return Response(
                    {"message": "Data successfully inserted into LoanLiquidationRequest."},
                    status=status.HTTP_200_OK)

            except AttributeError as e:
                return Response({"error": "Missing required fields", "details": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
