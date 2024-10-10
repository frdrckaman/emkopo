from xml.etree.ElementTree import Element, SubElement, tostring

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid
from datetime import datetime

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanOfferRequest, LoanNotificationEmployer
from emkopo_product.models import Fsp


class LoanNotificationToEmployerAPIView(APIView):
    """
    API View to generate and send XML notification to employer and save response into LoanNotificationEmployer model.
    """

    @swagger_auto_schema(
        operation_description="Generate XML notification from LoanOfferRequest and send it to a third-party system.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'LoanNumber': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='ID of the LoanOfferRequest object to generate the notification for'
                )
            },
            required=['loan_offer_request_id']
        ),
        responses={
            200: openapi.Response(description="Notification successfully sent and saved to LoanNotificationEmployer."),
            404: openapi.Response(description="LoanOfferRequest not found."),
            500: openapi.Response(description="Failed to send notification to the third-party system."),
        }
    )
    def post(self, request):
        # Get the loan_offer_request_id from the request body
        loan_number = request.data.get("LoanNumber")

        # Retrieve the LoanOfferRequest instance
        loan_offer_request = LoanOfferRequest.objects.get(LoanNumber=loan_number)

        fsp = Fsp.objects.first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        msg_id = str(uuid.uuid4())
        message_type = 'NOTIFICATION_FROM_FSP1_TO_EMPLOYER'

        # Generate XML data for the API call
        xml_data = generate_xml_for_notification(loan_offer_request, fsp)

        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_data,
            signature="XYZ",  # Replace with actual signature if available
            url="https://third-party-api.example.com/endpoint"
            # Replace with actual endpoint URL
        )

        if response.get('status') == 200:
            # After sending the payload, insert data into the LoanNotificationEmployer model
            try:
                LoanNotificationEmployer.objects.create(
                    PaymentReference=loan_offer_request.PaymentReferenceNumber,
                    FSPCode="0003",
                    FSPName="FSP1 Name",
                    ProductCode=int(loan_offer_request.ProductCode),
                    ProductName="Salary Loan",
                    FSP1LoanNumber=loan_offer_request.FSP1LoanNumber,
                    ApplicationNumber=loan_offer_request.ApplicationNumber,
                    LoanPayoffAmount=loan_offer_request.TotalAmountToPay or 0,
                    LoanLiquidationDate=loan_offer_request.DisbursementDate.date() if loan_offer_request.DisbursementDate else datetime.now().date(),
                    CheckNumber=str(loan_offer_request.CheckNumber),
                    FirstName=loan_offer_request.FirstName,
                    MiddleName=loan_offer_request.MiddleName,
                    LastName=loan_offer_request.LastName,
                    VoteCode=loan_offer_request.VoteCode,
                    VoteName=loan_offer_request.VoteName,
                    NIN=loan_offer_request.NIN,
                    DeductionCode="011001",
                    DeductionDescription="Deduction Description",
                    MessageType="NOTIFICATION_FROM_FSP1_TO_EMPLOYER",
                    RequestType="OUTWARD_NOTIFICATION",
                )
            except Exception as e:
                return Response(
                    {'error': f'Failed to save LoanNotificationEmployer: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content_type='application/xml'
                )

            return Response({"message": "Notification successfully sent and saved."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": response.get('error', 'Failed to send notification')},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_xml_for_notification(loan_offer_request, fsp):
    """
    Generate XML data for notification from LoanOfferRequest data.
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
    SubElement(header, "MessageType").text = "NOTIFICATION_FROM_FSP1_TO_EMPLOYER"

    # Create the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")
    SubElement(message_details, "PaymentReference").text = loan_offer_request.PaymentReferenceNumber or "77122876112"
    SubElement(message_details, "FSPCode").text = "0003"
    SubElement(message_details, "FSPName").text = "FSP1 Name"
    SubElement(message_details, "ProductCode").text = loan_offer_request.ProductCode
    SubElement(message_details, "ProductName").text = "Salary Loan"
    SubElement(message_details, "FSP1LoanNumber").text = loan_offer_request.FSP1LoanNumber or "1109000"
    SubElement(message_details, "ApplicationNumber").text = loan_offer_request.ApplicationNumber
    SubElement(message_details, "LoanPayoffAmount").text = str(loan_offer_request.TotalAmountToPay) or 0
    SubElement(message_details, "LoanLiquidationDate").text = loan_offer_request.DisbursementDate.strftime('%Y-%m-%dT%H:%M:%S') if loan_offer_request.DisbursementDate else datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    SubElement(message_details, "CheckNumber").text = str(loan_offer_request.CheckNumber)
    SubElement(message_details, "FirstName").text = loan_offer_request.FirstName
    SubElement(message_details, "MiddleName").text = loan_offer_request.MiddleName
    SubElement(message_details, "LastName").text = loan_offer_request.LastName
    SubElement(message_details, "VoteCode").text = loan_offer_request.VoteCode
    SubElement(message_details, "VoteName").text = loan_offer_request.VoteName
    SubElement(message_details, "NIN").text = loan_offer_request.NIN
    SubElement(message_details, "DeductionCode").text = "011001"  #get from finacle
    SubElement(message_details, "DeductionDescription").text = "Deduction Description"

    # Add the Signature element
    SubElement(document, "Signature").text = "XYZ"

    # Convert the ElementTree to a string
    xml_string = tostring(document, encoding="utf-8").decode("utf-8")
    return xml_string
