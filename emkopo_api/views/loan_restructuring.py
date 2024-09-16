import re
import uuid
import xmltodict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from xml.etree.ElementTree import Element, SubElement, tostring
from drf_yasg import openapi
from django.utils import timezone

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanRestructuringRequest


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
                signature="XYZ",  # Replace with actual signature if available
                url="https://third-party-api.example.com/endpoint"
                # Replace with actual endpoint URL
            )

            if response.get('status') == 200:
                return Response({
                    'message': 'Settlement balance response processed and sent successfully.'},
                    status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any exceptions that occur during XML parsing
            return Response({'error': f'Invalid XML data: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)


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

    # Add the Signature element
    SubElement(document, "Signature").text = "XYZ"

    # Convert the Element to a string
    xml_string = tostring(document, encoding="utf-8").decode("utf-8").strip()
    xml_data = re.sub(r'>\s+<', '><', xml_string)

    return xml_data
