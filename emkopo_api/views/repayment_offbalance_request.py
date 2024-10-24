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
from emkopo_api.serializers import LoanRepaymentOffBalanceRequestSerializer
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanTakeoverDetail
from emkopo_mixins.signature import load_private_key, sign_data
from emkopo_product.models import Fsp


class LoanRepaymentOffBalanceRequestAPIView(APIView):
    """
    API View to send XML data for loan repayment off-balance request, fetch data from LoanTakeoverDetail,
    and insert it into the LoanRepaymentOffBalanceRequest model.
    """

    @swagger_auto_schema(
        operation_description="Send XML for loan repayment off-balance request and insert into LoanRepaymentOffBalanceRequest model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'LoanNumber': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='LoanNumber ID'
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
        return repayment_offbalance_request(request)

def repayment_offbalance_request(request):
    loan_takeover_detail_id = request.data.get("LoanNumber")

    try:
        loan_takeover_detail = LoanTakeoverDetail.objects.get(
            LoanNumber=loan_takeover_detail_id)
    except LoanTakeoverDetail.DoesNotExist:
        return Response({"error": "LoanTakeoverDetail not found."},
                        status=status.HTTP_404_NOT_FOUND)

    # Prepare the data for the serializer
    request_data = {
        "TotalPayoffAmount": loan_takeover_detail.TotalPayoffAmount,
        "LoanNumber": loan_takeover_detail.LoanNumber,
        "LastDeductionDate": loan_takeover_detail.LastDeductionDate,
        "FSPBankAccount": loan_takeover_detail.FSPBankAccount,
        "FSPBankAccountName": loan_takeover_detail.FSPBankAccountName,
        "SWIFTCode": loan_takeover_detail.SWIFTCode,
        "MNOChannels": loan_takeover_detail.MNOChannels,
        "FinalPaymentDate": loan_takeover_detail.FinalPaymentDate,
        "EndDate": loan_takeover_detail.EndDate,
        "MessageType": "REPAYMENT_0FF_BALANCE_REQUEST_TO_FSP",
        "RequestType": "OUTWARD_REPAYMENT",
    }

    fsp = Fsp.objects.first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    # Generate the XML payload
    response = generate_xml_for_request(request_data, fsp)

    if response.get('status') == 200:
        return Response({"message": "Data successfully sent and inserted."},
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send data to the third-party system."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_xml_for_request(data, fsp):
    """
    Generate XML data for loan repayment off-balance request.
    """
    serializer = LoanRepaymentOffBalanceRequestSerializer(data=data)
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
        SubElement(header, "MessageType").text = "REPAYMENT_0FF_BALANCE_REQUEST_TO_FSP"

        # Create the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "TotalPayOffAmount").text = str(data["TotalPayoffAmount"])
        SubElement(message_details, "LoanNumber").text = data["LoanNumber"]
        SubElement(message_details, "LastDeductionDate").text = data["LastDeductionDate"]
        SubElement(message_details, "FSPBankAccount").text = data["FSPBankAccount"]
        SubElement(message_details, "FSPBankAccountName").text = data["FSPBankAccountName"]
        SubElement(message_details, "SWIFTCode").text = data["SWIFTCode"]
        SubElement(message_details, "MNOChannels").text = data["MNOChannels"]
        SubElement(message_details,
                   "PaymentReferenceNumber").text = "22211"  # Static or dynamically assigned
        SubElement(message_details, "EndDate").text = data["EndDate"]

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
