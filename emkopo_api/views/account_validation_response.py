import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import AccountValidationResponseSerializer
from emkopo_constants.constants import OUTGOING
from emkopo_loan.models import LoanOfferRequest
from emkopo_product.models import Fsp


class AccountValidationResponseAPIView(APIView):
    """
    API View to send XML data for account validation response and insert it into AccountValidationResponse model.
    """

    @swagger_auto_schema(
        operation_description="Send XML for account validation response and check if the AccountNumber exists in LoanOfferRequest model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'AccountNumber': openapi.Schema(type=openapi.TYPE_STRING, description='Account number to validate'),
            },
            required=['AccountNumber']
        ),
        responses={
            200: openapi.Response(description="Data successfully sent and inserted."),
            400: openapi.Response(description="Bad request: Invalid input or missing fields."),
            404: openapi.Response(description="Account number not found."),
            500: openapi.Response(description="Failed to send data to third-party system."),
        }
    )
    def post(self, request):
        return account_validation_response(request)


def account_validation_response(request):
    account_number = request.data.get("AccountNumber")
    if not account_number:
        return Response({"error": "AccountNumber parameter is required."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Check if the AccountNumber exists in the LoanOfferRequest model
    try:
        client_account = LoanOfferRequest.objects.get(BankAccountNumber=account_number)
    except LoanOfferRequest.DoesNotExist:
        return Response(
            {"error": f"AccountNumber '{account_number}' not found in LoanOfferRequest."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Parse the request data
    request_data = {
        "AccountNumber": client_account.BankAccountNumber,
        "Valid": "true",
        "Reason": "Account number blocked",
        "MessageType": "ACCOUNT_VALIDATION_RESPONSE",
        "RequestType": OUTGOING,
    }

    fsp = Fsp.objects.first()

    if not fsp:
        return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

    response = generate_xml_for_validation_response(request_data, fsp)

    if response.get('status') == 200:
        return Response({"message": "Data successfully sent and inserted."},
                        status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to send data to the third-party system."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_xml_for_validation_response(request_data, fsp):
    """
    Generate XML data for account validation response.
    """
    serializer = AccountValidationResponseSerializer(data=request_data)
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
        SubElement(header, "MessageType").text = "ACCOUNT_VALIDATION_RESPONSE"

        # Create the MessageDetails element
        message_details = SubElement(data_elem, "MessageDetails")
        SubElement(message_details, "Valid").text = "true" if data["Valid"] else "false"
        SubElement(message_details, "Reason").text = data["Reason"]

        # Add the Signature element
        SubElement(document, "Signature").text = settings.EMKOPO_SIGNATURE

        # Convert the XML Element to string
        xml_string = tostring(document, encoding="utf-8").decode("utf-8")

        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=xml_string,
            signature=settings.ESS_SIGNATURE,
            url=settings.ESS_UTUMISHI_API
        )
        return response
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

