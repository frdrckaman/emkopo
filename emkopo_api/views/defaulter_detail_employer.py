import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanDefaulterDetailEmployerSerializer
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanTakeoverDetail
from emkopo_product.models import Fsp


class LoanDefaulterDetailEmployerAPIView(APIView):
    """
    API View to send XML data for loan defaulter details, fetch data from LoanTakeoverDetail,
    and insert it into the LoanDefaulterDetailEmployer model.
    """

    @swagger_auto_schema(
        operation_description="Send XML for loan defaulter details and insert into LoanDefaulterDetailEmployer model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'LoanNumber': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='LoanNumber'
                )
            },
            required=['LoanNumber']
        ),
        responses={
            200: openapi.Response(description="Data successfully sent and inserted."),
            400: openapi.Response(description="Bad request: Invalid input or missing fields."),
            500: openapi.Response(description="Failed to send data to third-party system."),
        }
    )
    def post(self, request):
        # Get the loan_takeover_detail_id from the request body
        loan_takeover_detail_id = request.data.get("LoanNumber")

        # Fetch the LoanTakeoverDetail instance
        try:
            loan_takeover_detail = LoanTakeoverDetail.objects.get(LoanNumber=loan_takeover_detail_id)
        except LoanTakeoverDetail.DoesNotExist:
            return Response({"error": "LoanTakeoverDetail not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the data for the serializer
        request_data = {
            "CheckNumber": "9723101",
            "LoanNumber": loan_takeover_detail.LoanNumber,
            "VoteName": "Utumishi",  # Static value or fetched from another source if applicable
            "FirstName": "Simba<",
            "MiddleName": "Mapunda<",
            "LastName": "Nguchiro",
            "InstallationAmount": loan_takeover_detail.TotalPayoffAmount,  # Example mapping
            "DeductionAmount": loan_takeover_detail.TotalPayoffAmount,  # Example mapping
            "DeductionCode": "00101",  # Example static code
            "DeductionName": "Salary Loan",  # Example static deduction name
            "OutstandingBalance": loan_takeover_detail.OutstandingBalance,
            "LastPayDate": "2022-05-26T21:32:52",
            "MessageType": "DEFAULTER_DETAILS_TO_EMPLOYER",
            "RequestType": OUTGOING,
        }

        fsp = Fsp.objects.first()

        if not fsp:
            return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

        msg_id = str(uuid.uuid4())
        message_type = 'DEFAULTER_DETAILS_TO_EMPLOYER'

        response = generate_xml_for_defaulter(request_data, fsp)

        if response.get('status') == 200:
            return Response({"message": "Data successfully sent and inserted."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send data to the third-party system."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_xml_for_defaulter(request_data, fsp):
    """
    Generate XML data for loan defaulter details.
    """
    serializer = LoanDefaulterDetailEmployerSerializer(data=request_data)
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
        SubElement(header, "MessageType").text = "DEFAULTER_DETAILS_TO_EMPLOYER"

        # Create the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "VoteCode").text = "20"
        SubElement(message_details, "VoteName").text = data["VoteName"]
        SubElement(message_details, "CheckNumber").text = data["CheckNumber"]
        SubElement(message_details, "LoanNumber").text = data["LoanNumber"]
        SubElement(message_details, "FirstName").text = data["FirstName"]
        SubElement(message_details, "MiddleName").text = data["MiddleName"]
        SubElement(message_details, "LastName").text = data["LastName"]
        SubElement(message_details, "InstallationAmount").text = str(
            data["InstallationAmount"])
        SubElement(message_details, "DeductionName").text = data["DeductionName"]
        SubElement(message_details, "DeductionCode").text = data["DeductionCode"]
        SubElement(message_details, "OutstandingBalance").text = str(
            data["OutstandingBalance"])
        SubElement(message_details, "LastPayDate").text = data["LastPayDate"]

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

