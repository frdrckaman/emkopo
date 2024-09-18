import re

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid
from xml.etree.ElementTree import Element, SubElement, tostring

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanSettlementBalanceResponse
from emkopo_product.models import Fsp


class LoanTakeOverDetailsAPIView(APIView):
    """
    API View to receive loan number and FSP reference number,
    retrieve necessary data, and send XML response to a third-party system.
    """

    @swagger_auto_schema(
        operation_description="Receive LoanNumber and FSPReferenceNumber, process, and send XML response.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'LoanNumber': openapi.Schema(type=openapi.TYPE_STRING,
                                             description="Loan Number"),
                'FSPReferenceNumber': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description="FSP Reference Number"),
            },
            required=['LoanNumber', 'FSPReferenceNumber']
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
                examples={
                    'application/json': {
                        'message': 'Loan takeover details processed and sent successfully.'
                    }
                }
            ),
            400: openapi.Response(description="Invalid data or missing required fields"),
            500: openapi.Response(description="Internal Server Error"),
        },
        consumes=['application/json'],
    )
    def post(self, request, *args, **kwargs):
        # Extract LoanNumber and FSPReferenceNumber from the request body
        loan_number = request.data.get('LoanNumber')
        fsp_reference_number = request.data.get('FSPReferenceNumber')

        # Validate required fields
        if not loan_number or not fsp_reference_number:
            return Response(
                {'error': 'LoanNumber and FSPReferenceNumber are required fields.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Retrieve data from LoanSettlementBalanceResponse
            settlement_response = LoanSettlementBalanceResponse.objects.get(
                LoanNumber=loan_number,
                FSPReferenceNumber=fsp_reference_number
            )

            if not settlement_response:
                return Response({'error': 'Loan settlement response not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Retrieve FSP data
            fsp = Fsp.objects.all().first()  # Adjust the code based on your needs

            if not fsp:
                return Response({'error': 'FSP not found.'}, status=status.HTTP_404_NOT_FOUND)

            response = generate_response_xml(settlement_response, fsp)

            if response.get('status') == 200:
                return Response(
                    {'message': 'Loan takeover details processed and sent successfully.'},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Failed to send response to the third-party system.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': f'Error processing request: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)


def generate_response_xml(settlement_response, fsp):
    """
    Generate XML payload to send to the third-party system.
    """
    # Create the root element
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = fsp.sysName
    SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
    SubElement(header, "FSPCode").text = fsp.code
    SubElement(header, "MsgId").text = str(uuid.uuid4())
    SubElement(header, "MessageType").text = "LOAN_TAKEOVER_DETAILS_FROM_FSP"

    # Add the message details to the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")
    SubElement(message_details, "LoanNumber").text = settlement_response.LoanNumber
    SubElement(message_details,
               "FSPReferenceNumber").text = settlement_response.FSPReferenceNumber
    SubElement(message_details,
               "PaymentReferenceNumber").text = settlement_response.PaymentReferenceNumber
    SubElement(message_details, "TotalPayoffAmount").text = str(
        settlement_response.TotalPayoffAmount)
    SubElement(message_details, "OutstandingBalance").text = str(
        settlement_response.OutstandingBalance)
    SubElement(message_details, "FSPBankAccount").text = fsp.FSPBankAccount
    SubElement(message_details, "FSPBankAccountName").text = fsp.FSPBankAccountName
    SubElement(message_details, "SWIFTCode").text = fsp.SWIFTCode
    SubElement(message_details, "MNOChannels").text = fsp.MNOChannels
    SubElement(message_details,
               "FinalPaymentDate").text = settlement_response.FinalPaymentDate.isoformat()
    SubElement(message_details,
               "LastDeductionDate").text = settlement_response.LastDeductionDate.isoformat()
    SubElement(message_details,
               "LastPayDate").text = settlement_response.LastPayDate.isoformat()
    SubElement(message_details, "EndDate").text = settlement_response.EndDate.isoformat()

    # Add the Signature element
    SubElement(document, "Signature").text = "XYZ"

    # Convert the Element to a string
    xml_string = tostring(document, encoding="utf-8").decode("utf-8").strip()
    xml_data = re.sub(r'>\s+<', '><', xml_string)

    response = log_and_make_api_call(
        request_type=OUTGOING,
        payload=xml_data,
        signature="XYZ",  # Replace with actual signature if available
        url="https://third-party-api.example.com/endpoint"
        # Replace with actual endpoint URL
    )

    return response
