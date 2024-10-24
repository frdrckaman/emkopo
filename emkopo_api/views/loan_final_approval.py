import re

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xmltodict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanOfferRequest
from emkopo_mixins.signature import verify_xml_signature


class LoanFinalApprovalNotificationAPIView(APIView):
    """
    API View to receive loan final approval notification from the third-party system.
    """

    @swagger_auto_schema(
        operation_description="Receive loan final approval notification from the third-party system",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Sender': openapi.Schema(type=openapi.TYPE_STRING,
                                         description='Sender of the notification'),
                'Receiver': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='Receiver of the notification'),
                'MsgId': openapi.Schema(type=openapi.TYPE_STRING, description='Message ID'),
                'FSPCode': openapi.Schema(type=openapi.TYPE_STRING, description='FSP Code'),
                'MessageType': openapi.Schema(type=openapi.TYPE_STRING,
                                              description='Message Type'),
                'ApplicationNumber': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description='Application Number'),
                'Reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason'),
                'FSPReferenceNumber': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description='FSP Reference Number'),
                'LoanNumber': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Loan Number'),
                'Approval': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='Approval Status')
            },
        ),
        responses={
            200: openapi.Response(description="Data sent successfully (simulated)"),
            400: openapi.Response(description="Invalid data"),
            500: openapi.Response(description="Failed to send data to third-party system")
        },
        consumes=['application/json', 'application/xml'],
    )
    def post(self, request, *args, **kwargs):
        # Determine the content type
        global application_number
        content_type = request.content_type

        if content_type == 'application/xml':
            # Handle XML payload
            try:
                # Decode and parse the XML data
                xml_data = request.body.decode('utf-8').strip()
                xml_data = re.sub(r'>\s+<', '><', xml_data)
                payload = xmltodict.parse(xml_data)
            except Exception as e:
                return Response({'error': f'Invalid XML data: {str(e)}'},
                                status=status.HTTP_400_BAD_REQUEST)
            if not settings.EMKOPO_SIT:
                # Verify the XML signature before proceeding
                if not verify_xml_signature(xml_data):
                    return Response({"error": "Signature verification failed"},
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    'error': 'Unsupported content type. Use application/json or application/xml.'},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )

        return log_and_make_api_call(payload, xml_data)

def loan_final_approval(payload, xml_data):
    content_type = 'application/xml'
    response = log_and_make_api_call(
        request_type=INCOMING,
        payload=xml_data,
        signature=settings.ESS_SIGNATURE,  # Replace with actual signature if available
        url=settings.ESS_UTUMISHI_API
        # Replace with actual endpoint URL
    )

    if response.get('status') == 200:
        try:
            if content_type == 'application/xml':
                # Adjust the path for XML structure
                data = payload.get('Document', {}).get('Data', {})
                message_details = data.get('MessageDetails', {})
            else:
                # Directly use JSON structure
                message_details = payload

            application_number = message_details.get('ApplicationNumber')
            approval = message_details.get('Approval')

            if approval == 'APPROVED':
                ln_status = 3
            elif approval == 'REJECTED':
                ln_status = 9
            else:
                ln_status = 8

            loan_offer_request = LoanOfferRequest.objects.get(
                ApplicationNumber=application_number)
            loan_offer_request.status = ln_status
            loan_offer_request.save()
        except LoanOfferRequest.DoesNotExist:
            return Response({
                'error': f'LoanOfferRequest with ApplicationNumber '
                         f'{application_number} not found.'},
                status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Data sent successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": response.get('error', 'Failed to send data')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

