import xmltodict
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanDeductionStopNotificationSerializer
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanDeductionStopNotification


class LoanDeductionStopNotificationAPIView(APIView):
    """
    API View to receive XML data for Loan Deduction Stop Notification and insert into LoanDeductionStopNotification model.
    """

    @swagger_auto_schema(
        operation_description="Receive XML for loan deduction stop notification and insert into LoanDeductionStopNotification model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload with loan deduction stop notification"
        ),
        responses={
            200: openapi.Response(description="Data successfully inserted into LoanDeductionStopNotification."),
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

        return deduction_stop_notification(data_dict, xml_data)



def deduction_stop_notification(data_dict, xml_data):
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

    serializer = LoanDeductionStopNotificationSerializer(data=combined_data)

    if serializer.is_valid():

        try:
            LoanDeductionStopNotification.objects.create(
                FSPReferenceNumber=serializer.validated_data.get('FSPReferenceNumber'),
                CheckNumber=serializer.validated_data.get('CheckNumber'),
                LoanNumber=serializer.validated_data.get('LoanNumber'),
                FirstName=serializer.validated_data.get('FirstName'),
                MiddleName=serializer.validated_data.get('MiddleName'),
                LastName=serializer.validated_data.get('LastName'),
                VoteCode=serializer.validated_data.get('VoteCode'),
                VoteName=serializer.validated_data.get('VoteName'),
                DepartmentCode=serializer.validated_data.get('DepartmentCode'),
                DepartmentName=serializer.validated_data.get('DepartmentName'),
                DeductionCode=serializer.validated_data.get('DeductionCode'),
                DeductionDescription=serializer.validated_data.get('DeductionDescription'),
                DeductionAmount=serializer.validated_data.get('DeductionAmount'),
                BalanceAmount=serializer.validated_data.get('BalanceAmount'),
                StopDate=serializer.validated_data.get('StopDate'),
                StopPayReason=serializer.validated_data.get('StopPayReason'),
                MessageType=header_data.get('MessageType'),
                RequestType=INCOMING,
            )
            return Response(
                {'message': 'Loan offer request processed successfully'},
                status=status.HTTP_200_OK,
                content_type='application/xml'
            )
        except Exception as e:
            print(str(e))
            return Response(
                {'error': f'Failed to save FullLoanRepaymentRequest: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/xml'
            )
    else:
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)