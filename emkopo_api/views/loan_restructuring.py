import base64
import re
import uuid
import xmltodict
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg import openapi
from django.utils import timezone

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import INCOMING, OUTGOING
from emkopo_loan.models import LoanRestructuringRequest
from emkopo_mixins.signature import load_private_key, sign_data


class LoanRestructuringRequestAPIView(APIView):
    """
    API View to receive loan restructuring request, insert into model, and send response to a third-party system.
    """

    @swagger_auto_schema(
        operation_description="Receive loan restructuring request, insert into model, and send response.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload containing loan restructuring request",
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
            return loan_restructuring(data_dict, xml_data)
        except Exception as e:
            return Response({'error': f'Invalid XML data: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST)

def loan_restructuring(data_dict, xml_data):
    document = data_dict.get('Document', {})
    data = document.get('Data', {})
    message_details = data.get('MessageDetails', {})

    # Extract specific fields from the XML payload
    application_number = message_details.get('ApplicationNumber')
    comments = message_details.get('Comments')
    loan_number = message_details.get('LoanNumber')
    loan_outstanding_amount = message_details.get('LoanOutstandingAmount')
    new_loan_amount = message_details.get('NewLoanAmount')
    new_installment_amount = message_details.get('NewInstallmentAmount')

    # Validate required fields
    if not application_number or not loan_number or not loan_outstanding_amount or not new_loan_amount or not new_installment_amount:
        return Response(
            {
                'error': 'ApplicationNumber, LoanNumber, LoanOutstandingAmount, NewLoanAmount, and NewInstallmentAmount are required fields.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create a new LoanRestructuringRequest object
    LoanRestructuringRequest.objects.create(
        ApplicationNumber=application_number,
        LoanNumber=loan_number,
        Comments=comments,
        LoanOutstandingAmount=loan_outstanding_amount,
        NewLoanAmount=new_loan_amount,
        NewInstallmentAmount=new_installment_amount,
        Timestamp=timezone.now(),
        MessageType="LOAN_RESTRUCTURING_NOTIFICATION",
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


def loan_restructuring_request(restructuring_request, fsp):
    """
    Generate XML payload to send to the third-party system.
    """
    # Create the root element
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = "FSPSystem"  # Set Sender
    SubElement(header, "Receiver").text = "ESS_UTUMISHI"  # Set Receiver
    SubElement(header, "FSPCode").text = "1001"  # Set FSPCode
    SubElement(header, "MsgId").text = str(uuid.uuid4())  # Generate unique MsgId
    SubElement(header, "MessageType").text = "LOAN_RESTRUCTURING_NOTIFICATION"

    # Add the message details to the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")
    SubElement(message_details,
               "ApplicationNumber").text = restructuring_request.ApplicationNumber
    SubElement(message_details, "Comments").text = restructuring_request.Comments
    SubElement(message_details, "LoanNumber").text = restructuring_request.LoanNumber
    SubElement(message_details, "LoanOutstandingAmount").text = str(
        restructuring_request.LoanOutstandingAmount)
    SubElement(message_details, "NewLoanAmount").text = str(
        restructuring_request.NewLoanAmount)
    SubElement(message_details, "NewInstallmentAmount").text = str(
        restructuring_request.NewInstallmentAmount)

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

    try:
        LoanRestructuringRequest.objects.create(
            ApplicationNumber=restructuring_request.ApplicationNumber,
            LoanNumber=restructuring_request.LoanNumber,
            Comments=restructuring_request.Comments,
            LoanOutstandingAmount=restructuring_request.LoanOutstandingAmount,
            NewLoanAmount=restructuring_request.NewLoanAmount,
            NewInstallmentAmount=restructuring_request.NewInstallmentAmount,
            MessageType="LOAN_RESTRUCTURING_NOTIFICATION",
            RequestType=INCOMING
        )

        # Send the API response with the final XML payload
        response = log_and_make_api_call(
            request_type=OUTGOING,
            payload=final_xml_string,
            signature=signature_b64,
            url=settings.ESS_UTUMISHI_API
        )

    except Exception as e:
        # Handle any exceptions that occur during XML parsing
        return Response({'error': f'Invalid XML data: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST)

    return response
