import base64
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
from emkopo_mixins.signature import load_private_key, sign_data
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
        return loan_notification_employer(request)

def loan_notification_employer(request):
    loan_number = request.data.get("LoanNumber")

    # Retrieve the LoanOfferRequest instance
    loan_offer_request = LoanOfferRequest.objects.get(LoanNumber=loan_number)

    fsp = Fsp.objects.first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    # Generate XML data for the API call
    response = generate_xml_for_notification(loan_offer_request, fsp)

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

        return Response({"message": "Notification successfully sent and saved."},
                        status=status.HTTP_200_OK)
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

    # Convert the XML Element to string (we'll sign this string)
    xml_string = tostring(document, encoding="utf-8").decode("utf-8")

    # Load the private key to sign the data
    private_key = load_private_key(settings.EMKOPO_PRIVATE_KEY)

    # Convert the XML string to bytes
    xml_bytes = xml_string.encode('utf-8')

    # Sign the XML data (xml_bytes) using the private key
    signature = sign_data(private_key, xml_bytes)

    # Encode the signature in base64
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    # Add the Signature element to the document
    SubElement(document, "Signature").text = signature_b64

    # Convert the final XML (with the signature) to string
    final_xml_string = tostring(document, encoding="utf-8").decode("utf-8")

    # Send the API response with the final XML payload
    response = log_and_make_api_call(
        request_type=OUTGOING,
        payload=final_xml_string,
        signature=signature_b64,
        url=settings.ESS_UTUMISHI_API
    )
    return response
