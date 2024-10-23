from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import fromstring
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_date
import html
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanDeductionRecordSerializer
from emkopo_constants.constants import INCOMING


class LoanMonthlyDeductionRecordAPIView(APIView):
    """
    API View to receive XML data for Loan Deduction Records and insert it into LoanDeductionRecord model.
    """

    @swagger_auto_schema(
        operation_description="Receive XML for loan deduction records and insert into LoanDeductionRecord model.",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload with deduction records"
        ),
        responses={
            200: openapi.Response(description="Data successfully inserted into LoanDeductionRecord."),
            400: openapi.Response(description="Bad request: Invalid XML or missing fields."),
        }
    )
    def post(self, request):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response({"error": "Content-Type must be application/xml"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the XML data from the request body
        try:
            raw_xml = request.body.decode('utf-8')
            cleaned_xml = self.clean_xml_data(raw_xml)  # Clean up the XML data
            xml_data = fromstring(cleaned_xml)  # Parse the cleaned XML
        except Exception as e:
            return Response({"error": "Invalid XML format", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            log_and_make_api_call(
                request_type=INCOMING,
                payload=cleaned_xml,
                signature="XYZ",  # Replace with actual signature if available
                url="https://third-party-api.example.com/endpoint"
                # Replace with actual endpoint URL
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to save API request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/xml'
            )

        # Extract the relevant fields and map them to the request data
        try:
            deduction_records = xml_data.findall('Data/MessageDetails/DeductionRecord')
            for record in deduction_records:
                request_data = {
                    "LoanNumber": self.get_xml_value(record, 'LoanNumber'),
                    "CheckNumber": self.get_xml_value(record, 'CheckNumber'),
                    "FirstName": self.get_xml_value(record, 'FirstName'),
                    "MiddleName": self.get_xml_value(record, 'MiddleName'),
                    "LastName": self.get_xml_value(record, 'LastName'),
                    "NationalId": self.get_xml_value(record, 'NationalId'),
                    "VoteCode": self.get_xml_value(record, 'VoteCode'),
                    "VoteName": self.get_xml_value(record, 'VoteName'),
                    "DepartmentCode": self.get_xml_value(record, 'DepartmentCode'),
                    "DepartmentName": self.get_xml_value(record, 'DepartmentName'),
                    "DeductionCode": self.get_xml_value(record, 'DeductionCode'),
                    "DeductionDescription": self.get_xml_value(record, 'DeductionDescription'),
                    "BalanceAmount": self.get_xml_value(record, 'BalanceAmount'),
                    "DeductionAmount": self.get_xml_value(record, 'DeductionAmount'),
                    "HasStopPay": self.get_xml_value(record, 'HasStopPay', is_bool=True),
                    "StopPayReason": self.get_xml_value(record, 'StopPayReason', allow_null=True),
                    "CheckDate": parse_date(self.get_xml_value(record, 'CheckDate')),
                    "MessageType": "FSP_MONTHLY_DEDUCTIONS",
                    "RequestType": INCOMING,
                }

                # Pass the dictionary data to the serializer
                serializer = LoanDeductionRecordSerializer(data=request_data)

                # Validate and save the data
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Data successfully inserted into LoanDeductionRecord."}, status=status.HTTP_200_OK)

        except AttributeError as e:
            return Response({"error": "Missing required fields", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def clean_xml_data(self, raw_xml):
        """
        Clean up the XML data by unescaping HTML entities and removing unwanted characters.
        """
        # Unescape HTML entities
        cleaned_xml = html.unescape(raw_xml)

        # Remove any unnecessary whitespace, newlines, or control characters
        cleaned_xml = re.sub(r'\s+', ' ', cleaned_xml).strip()

        return cleaned_xml

    def get_xml_value(self, xml_element, tag, is_bool=False, allow_null=False):
        """
        Utility function to safely extract text from an XML element, handling missing or None values.
        If the tag is missing, return an empty string or None depending on `allow_null`.
        """
        element = xml_element.find(tag)
        if element is not None and element.text is not None:
            return element.text.strip() if not is_bool else element.text.strip().lower() == 'true'
        return None if allow_null else ''