import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring

from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanNotificationEmployer
from emkopo_product.models import Fsp
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..mixins import log_and_make_api_call
from ..serializers import LoanRepaymentNotificationSerializer


class LoanRepaymentNotificationAPIView(APIView):
    """
    API View to send XML data for loan repayment notification, fetch data from LoanTakeoverDetail,
    and insert it into the LoanRepaymentNotification model.
    """

    @swagger_auto_schema(
        operation_description="Send XML for loan repayment notification and insert into LoanRepaymentNotification model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ApplicationNumber': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='ApplicationNumber'
                )
            },
            required=['ApplicationNumber']
        ),
        responses={
            200: openapi.Response(description="Data successfully sent and inserted."),
            400: openapi.Response(description="Bad request: Invalid input or missing fields."),
            500: openapi.Response(description="Failed to send data to third-party system."),
        }
    )
    def post(self, request):
        # Get the loan_takeover_detail_id from the request body
        loan_takeover_detail_id = request.data.get("ApplicationNumber")

        # Fetch the LoanTakeoverDetail instance
        try:
            loan_takeover_detail = LoanNotificationEmployer.objects.get(ApplicationNumber=loan_takeover_detail_id)
        except LoanNotificationEmployer.DoesNotExist:
            return Response({"error": "LoanNotificationEmployer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the data for the serializer
        request_data = {
            "CheckNumber": loan_takeover_detail.CheckNumber,
            "ApplicationNumber": loan_takeover_detail.ApplicationNumber,
            "LoanNumber": "SBT-0001",
            "PaymentReference": loan_takeover_detail.PaymentReference,
            "DeductionCode": "003",  # Example value
            "PaymentDescription": "Loan repayment notification",  # Example description
            "PaymentDate": "2022-05-26T21:32:52",
            "MaturityDate": "2022-05-26T21:32:52",
            "PaymentAmount": 100000.00,
            "LoanBalance": 120000.00,
            "MessageType": "PARTIAL_LOAN_REPAYMENT_NOTIFICATION",
            "RequestType": OUTGOING,
        }

        fsp = Fsp.objects.first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        msg_id = str(uuid.uuid4())
        message_type = 'FULL_REPAYMENT_0FF_BALANCE_RESPONSE'

        response = generate_xml_for_repayment(request_data, fsp)

        if response.get('status') == 200:
            return Response({"message": "Data successfully sent and inserted."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send data to the third-party system."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_xml_for_repayment(request_data, fsp):
    """
    Generate XML data for loan repayment notification.
    """
    serializer = LoanRepaymentNotificationSerializer(data=request_data)
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
        SubElement(header, "MessageType").text = "PARTIAL_LOAN_REPAYMENT_NOTIFICATION"

        # Create the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "CheckNumber").text = data["CheckNumber"]
        SubElement(message_details, "ApplicationNumber").text = data["ApplicationNumber"]
        SubElement(message_details, "LoanNumber").text = data["LoanNumber"]
        SubElement(message_details, "PaymentReference").text = data["PaymentReference"]
        SubElement(message_details, "DeductionCode").text = data["DeductionCode"]
        SubElement(message_details, "PaymentDescription").text = data["PaymentDescription"]
        SubElement(message_details, "PaymentDate").text = data["PaymentDate"]
        SubElement(message_details, "MaturityDate").text = data["MaturityDate"]
        SubElement(message_details, "PaymentAmount").text = str(data["PaymentAmount"])
        SubElement(message_details, "LoanBalance").text = str(data["LoanBalance"])

        # Add the Signature element
        SubElement(document, "Signature").text = "XYZ"

        # Convert the XML Element to string
        xml_string = tostring(document, encoding="utf-8").decode("utf-8")

        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_string,
            signature="XYZ",  # Replace with actual signature if available
            url="https://third-party-api.example.com/endpoint"
            # Replace with actual endpoint URL
        )
        return response
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

