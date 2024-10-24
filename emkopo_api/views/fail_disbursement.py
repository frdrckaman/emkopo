import re

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from drf_yasg.utils import swagger_auto_schema
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanOfferRequest
from emkopo_product.models import Fsp


class LoanDisbursementFailureNotificationAPIView(APIView):
    """
    API View to select a LoanOfferRequest and send disbursement notification to the third-party system.
    """

    @swagger_auto_schema(
        operation_description="Send loan disbursement notification to the third-party system",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ApplicationNumber': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description='Application Number')
            },
            required=['ApplicationNumber'],
            example={
                'ApplicationNumber': '1002'
            }
        ),
        responses={
            200: openapi.Response(description="Notification sent successfully"),
            404: openapi.Response(description="LoanOfferRequest not found"),
            400: openapi.Response(description="Invalid data"),
            500: openapi.Response(description="Internal Server Error"),
        },
        consumes=['application/json']
    )
    def post(self, request, *args, **kwargs):
        return fail_disbursement(request)

def fail_disbursement(request):
    application_number = request.data.get('ApplicationNumber')

    # Validate parameters
    if not application_number:
        return Response({'error': 'ApplicationNumber is required.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the LoanOfferRequest instance
        loan_offer_request = LoanOfferRequest.objects.get(
            ApplicationNumber=application_number,
            status=5
        )
    except LoanOfferRequest.DoesNotExist:
        return Response({
            'error': 'LoanOfferRequest not found with the provided ApplicationNumber.'},
            status=status.HTTP_404_NOT_FOUND)

    fsp = Fsp.objects.all().first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    response = loan_disbursement_notification(loan_offer_request, fsp)

    if response.get('status') == 200:
        return Response({"message": "Data sent successfully"},
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": response.get('error', 'Failed to send data')},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def loan_disbursement_notification(disburse_response, fsp):
    """
    Generate XML data for product decommission message.
            """
    # Create the root element
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = fsp.name  # Get Sender from Fsp model
    SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
    SubElement(header, "FSPCode").text = fsp.code  # Get FSPCode from Fsp model
    SubElement(header, "MsgId").text = str(uuid.uuid4())  # Generate unique MsgId
    SubElement(header, "MessageType").text = "LOAN_DISBURSEMENT_FAILURE_NOTIFICATION"

    # Add the product code to the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")
    SubElement(message_details,
               "ApplicationNumber").text = disburse_response.ApplicationNumber
    SubElement(message_details, "Reason").text = disburse_response.FailureReason
    # Add the Signature element
    SubElement(document, "Signature").text = "XYZ"

    # Convert the Element to a string
    xml_string = tostring(document, encoding="utf-8").decode("utf-8").strip()
    xml_data = re.sub(r'>\s+<', '><', xml_string)

    response = log_and_make_api_call(
        request_type=OUTGOING,
        payload=xml_data,
        signature=settings.ESS_SIGNATURE,
        url=settings.ESS_UTUMISHI_API
    )

    return response
