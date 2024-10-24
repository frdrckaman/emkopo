import base64
import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import FullLoanRepaymentNotificationSerializer
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanNotificationEmployer
from emkopo_mixins.signature import load_private_key, sign_data
from emkopo_product.models import Fsp


class FullLoanRepaymentNotificationAPIView(APIView):
    """
    API View to send XML data for full loan repayment notification, fetch data from LoanNotificationEmployer,
    and insert it into the FullLoanRepaymentNotification model.
    """

    @swagger_auto_schema(
        operation_description="Send XML for full loan repayment notification and insert into FullLoanRepaymentNotification model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'ApplicationNumber': openapi.Schema(type=openapi.TYPE_STRING,escription='Application Number')},
            required=['loan_notification_employer_id']
        ),
        responses={
            200: openapi.Response(description="Data successfully sent and inserted."),
            400: openapi.Response(description="Bad request: Invalid input or missing fields."),
            500: openapi.Response(description="Failed to send data to third-party system."),
        }
    )
    def post(self, request):
        return full_loan_repayment(request)

def full_loan_repayment(request):
    loan_notification_employer_id = request.data.get("ApplicationNumber")

    # Fetch the LoanNotificationEmployer instance
    try:
        loan_notification_employer = LoanNotificationEmployer.objects.get(
            ApplicationNumber=loan_notification_employer_id)
    except LoanNotificationEmployer.DoesNotExist:
        return Response({"error": "LoanNotificationEmployer not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Prepare the data for the serializer
    request_data = {
        "CheckNumber": loan_notification_employer.CheckNumber,
        "ApplicationNumber": loan_notification_employer.ApplicationNumber,
        "LoanNumber": "SBT-001",
        "PaymentReference": loan_notification_employer.PaymentReference,
        "DeductionCode": loan_notification_employer.DeductionCode,
        "PaymentDescription": "Full Loan Repayment",  # Example description
        "PaymentDate": "2022-05-26T21:32:52",
        "PaymentAmount": 100000.00,
        "LoanBalance": 0.00,  # Assuming full loan repayment
        "MessageType": "FULL_LOAN_REPAYMENT_NOTIFICATION",
        "RequestType": OUTGOING,
    }

    fsp = Fsp.objects.first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    response = generate_xml_for_repayment(request_data, fsp)

    if response.get('status') == 200:
        return Response({"message": "Data successfully sent and inserted."},
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send data to the third-party system."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_xml_for_repayment(request_data, fsp):
    """
    Generate XML data for full loan repayment notification.
    """
    serializer = FullLoanRepaymentNotificationSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        document = Element("Document")
        data_elem = SubElement(document, "Data")

        # Create the header
        header = SubElement(data_elem, "Header")
        SubElement(header, "Sender").text = fsp.name
        SubElement(header, "Receiver").text = settings.EMKOPO_UTUMISHI_SYSNAME
        SubElement(header, "FSPCode").text = fsp.code
        SubElement(header, "MsgId").text = str(uuid.uuid4())
        SubElement(header, "MessageType").text = "FULL_LOAN_REPAYMENT_NOTIFICATION"

        # Create the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "CheckNumber").text = data["CheckNumber"]
        SubElement(message_details, "ApplicationNumber").text = data["ApplicationNumber"]
        SubElement(message_details, "LoanNumber").text = data["LoanNumber"]
        SubElement(message_details, "PaymentReference").text = data["PaymentReference"]
        SubElement(message_details, "DeductionCode").text = data["DeductionCode"]
        SubElement(message_details, "PaymentDescription").text = data["PaymentDescription"]
        SubElement(message_details, "PaymentDate").text = data["PaymentDate"]
        SubElement(message_details, "PaymentAmount").text = str(data["PaymentAmount"])
        SubElement(message_details, "LoanBalance").text = str(data["LoanBalance"])

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
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
