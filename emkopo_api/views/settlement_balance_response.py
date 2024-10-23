import re
import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xmltodict
from drf_yasg.utils import swagger_auto_schema
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg import openapi
from django.utils import timezone

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import OUTGOING, INCOMING
from emkopo_loan.models import LoanSettlementBalanceResponse


class LoanSettlementBalanceResponseAPIView(APIView):
    """
    API View to receive loan settlement balance response from a third-party system,
    insert into LoanSettlementBalanceResponse model, and send the response to a third-party system.
    """

    @swagger_auto_schema(
        operation_description="Receive loan settlement balance response, insert into model, and send response.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload containing loan settlement balance response",
        ),
        responses={
            200: openapi.Response(description="Successful Response"),
            400: openapi.Response(description="Invalid XML data or missing required fields"),
            500: openapi.Response(description="Internal Server Error"),
        },
        consumes=['application/xml'],
    )
    def post(self, request, *args, **kwargs):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response(
                {'error': 'Content-Type must be application/xml'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Decode the XML data from the request body
            xml_data = request.body.decode('utf-8').strip()
            xml_data = re.sub(r'>\s+<', '><', xml_data)

            # Parse the XML data to a Python dictionary
            data_dict = xmltodict.parse(xml_data)

            # Extract data from the parsed dictionary
            document = data_dict.get('Document', {})
            data = document.get('Data', {})
            message_details = data.get('MessageDetails', {})

            # Extract specific fields from the XML payload
            loan_number = message_details.get('LoanNumber')
            fsp_reference_number = message_details.get('FSPReferenceNumber')
            payment_reference_number = message_details.get('PaymentReferenceNumber')
            total_payoff_amount = message_details.get('TotalPayoffAmount')
            outstanding_balance = message_details.get('OutstandingBalance')
            final_payment_date = message_details.get('FinalPaymentDate')
            last_deduction_date = message_details.get('LastDeductionDate')
            last_pay_date = message_details.get('LastPayDate')
            end_date = message_details.get('EndDate')

            # Validate required fields
            if not loan_number or not fsp_reference_number or not payment_reference_number:
                return Response(
                    {
                        'error': 'LoanNumber, FSPReferenceNumber, and PaymentReferenceNumber are required fields.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create a new LoanSettlementBalanceResponse object
            LoanSettlementBalanceResponse.objects.create(
                LoanNumber=loan_number,
                FSPReferenceNumber=fsp_reference_number,
                PaymentReferenceNumber=payment_reference_number,
                TotalPayoffAmount=total_payoff_amount,
                OutstandingBalance=outstanding_balance,
                FinalPaymentDate=final_payment_date,
                LastDeductionDate=last_deduction_date,
                LastPayDate=last_pay_date,
                EndDate=end_date,
                Timestamp=timezone.now(),
                MessageType="LOAN_TOP_UP_BALANCE_RESPONSE",
                RequestType=INCOMING
            )

            response = log_and_make_api_call(
                request_type=INCOMING,
                payload=xml_data,
                signature=settings.ESS_SIGNATURE,  # Replace with actual signature if available
                url=settings.ESS_UTUMISHI_API
                # Replace with actual endpoint URL
            )

            if response.get('status') == 200:
                return Response({
                    'message': 'Settlement balance response processed and sent successfully.'},
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Failed to send response to the third-party system.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Handle any exceptions that occur during XML parsing
            return Response({'error': f'Invalid XML data: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)


def loan_settlement_balance_response(settlement_response, fsp):
    """
    Generate XML payload to send to the third-party system.
    """
    # Create the root element
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = fsp.name
    SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
    SubElement(header, "FSPCode").text = fsp.code
    SubElement(header, "MsgId").text = str(uuid.uuid4())
    SubElement(header, "MessageType").text = "LOAN_TOP_UP_BALANCE_RESPONSE"

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
    SubElement(message_details,
               "FinalPaymentDate").text = settlement_response.FinalPaymentDate.isoformat()
    SubElement(message_details,
               "LastDeductionDate").text = settlement_response.LastDeductionDate.isoformat()
    SubElement(message_details, "LastPayDate").text = (
        settlement_response.LastPayDate.isoformat())
    SubElement(message_details, "EndDate").text = settlement_response.EndDate.isoformat()

    # Add the Signature element
    SubElement(document, "Signature").text = "XYZ"

    # Convert the Element to a string
    xml_string = tostring(document, encoding="utf-8").decode("utf-8").strip()
    xml_data = re.sub(r'>\s+<', '><', xml_string)

    try:
        LoanSettlementBalanceResponse.objects.create(
            LoanNumber=settlement_response.LoanNumber,
            FSPReferenceNumber=settlement_response.FSPReferenceNumber,
            PaymentReferenceNumber=settlement_response.PaymentReferenceNumber,
            TotalPayoffAmount=settlement_response.TotalPayoffAmount,
            OutstandingBalance=settlement_response.OutstandingBalance,
            FinalPaymentDate=settlement_response.FinalPaymentDate,
            LastDeductionDate=settlement_response.LastDeductionDate,
            LastPayDate=settlement_response.LastPayDate,
            EndDate=settlement_response.EndDate,
            MessageType="LOAN_TOP_UP_BALANCE_RESPONSE",
            RequestType=OUTGOING
        )

        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_data,
            signature=settings.ESS_SIGNATURE,  # Replace with actual signature if available
            url=settings.ESS_UTUMISHI_API
            # Replace with actual endpoint URL
        )

    except Exception as e:
        # Handle any exceptions that occur during XML parsing
        return Response({'error': f'Invalid XML data: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST)
    return response
