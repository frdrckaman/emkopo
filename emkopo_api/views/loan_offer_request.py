from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import xmltodict
import re

from emkopo_api.mixins import log_and_make_api_call
from emkopo_api.serializers import LoanOfferRequestSerializer
from emkopo_constants.constants import INCOMING, NEW_LOAN, TOP_UP_LOAN, TAKE_OVER_LOAN
from emkopo_loan.models import LoanOfferRequest


class LoanOfferRequestAPIView(APIView):
    @swagger_auto_schema(
        operation_description="API to receive loan offer request in XML format",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_BINARY,
            description="XML data representing loan offer request"
        ),
        responses={200: "Successfully processed the request", 400: "Invalid data"}
    )
    def post(self, request, *args, **kwargs):
        # Ensure the content type is XML
        if request.content_type != 'application/xml':
            return Response(
                {'error': 'Content-Type must be application/xml'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Decode and clean up the XML data
        try:
            xml_data = request.body_cache.decode('utf-8').strip()
            if not xml_data:
                raise ValueError("Empty request body")

            # Remove whitespace between XML tags
            xml_data = re.sub(r'>\s+<', '><', xml_data)
        except Exception as e:
            return Response(
                {'error': f'Invalid XML data in request body: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Convert XML data to a dictionary
        try:
            data_dict = xmltodict.parse(xml_data)
        except Exception as e:
            return Response(
                {'error': f'Failed to parse XML: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Extract 'Document' data to pass to the serializer
        document_data = data_dict.get('Document')
        if not document_data:
            return Response(
                {'error': 'Document node is missing in the XML data.'},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/xml'
            )

        # Extract Header and MessageDetails
        header_data = document_data.get('Data', {}).get('Header', {})
        message_details = document_data.get('Data', {}).get('MessageDetails', {})
        # print('frdrck 1')
        try:
            log_and_make_api_call(
                request_type=INCOMING,
                payload=xml_data,
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

        # Combine Header and MessageDetails for serialization
        combined_data = {**header_data, **message_details,
                         'Signature': document_data.get('Signature', '')}

        # Validate the data using the serializer
        serializer = LoanOfferRequestSerializer(data=combined_data)

        if serializer.is_valid():
            if header_data.get('MessageType') == settings.EMKOPO_NEW_LOAN_MSG:
                loan_offer_type = NEW_LOAN
            elif header_data.get('MessageType') == settings.EMKOPO_NEW_TOP_UP_MSG:
                loan_offer_type = TOP_UP_LOAN
            elif header_data.get('MessageType') == settings.EMKOPO_NEW_TAKEOVER_MSG:
                loan_offer_type = TAKE_OVER_LOAN
            else:
                loan_offer_type = 'Unknown'

            # Log the request data
            try:
                LoanOfferRequest.objects.create(
                    CheckNumber=serializer.validated_data.get('CheckNumber'),
                    FirstName=serializer.validated_data.get('FirstName'),
                    MiddleName=serializer.validated_data.get('MiddleName'),
                    LastName=serializer.validated_data.get('LastName'),
                    Sex=serializer.validated_data.get('Sex'),
                    BankAccountNumber=serializer.validated_data.get('BankAccountNumber'),
                    EmploymentDate=serializer.validated_data.get('EmploymentDate'),
                    MaritalStatus=serializer.validated_data.get('MaritalStatus'),
                    ConfirmationDate=serializer.validated_data.get('ConfirmationDate'),
                    TotalEmployeeDeduction=serializer.validated_data.get(
                        'TotalEmployeeDeduction'),
                    NearestBranchName=serializer.validated_data.get('NearestBranchName'),
                    VoteCode=serializer.validated_data.get('VoteCode'),
                    VoteName=serializer.validated_data.get('VoteName'),
                    NIN=serializer.validated_data.get('NIN'),
                    DesignationCode=serializer.validated_data.get('DesignationCode'),
                    DesignationName=serializer.validated_data.get('DesignationName'),
                    BasicSalary=serializer.validated_data.get('BasicSalary'),
                    NetSalary=serializer.validated_data.get('NetSalary'),
                    OneThirdAmount=serializer.validated_data.get('OneThirdAmount'),
                    RequestedAmount=serializer.validated_data.get('RequestedAmount'),
                    DesiredDeductibleAmount=serializer.validated_data.get(
                        'DesiredDeductibleAmount'),
                    RetirementDate=serializer.validated_data.get('RetirementDate'),
                    TermsOfEmployment=serializer.validated_data.get('TermsOfEmployment'),
                    Tenure=serializer.validated_data.get('Tenure'),
                    ProductCode=serializer.validated_data.get('ProductCode'),
                    InterestRate=serializer.validated_data.get('InterestRate'),
                    ProcessingFee=serializer.validated_data.get('ProcessingFee'),
                    Insurance=serializer.validated_data.get('Insurance'),
                    PhysicalAddress=serializer.validated_data.get('PhysicalAddress'),
                    EmailAddress=serializer.validated_data.get('EmailAddress'),
                    MobileNumber=serializer.validated_data.get('MobileNumber'),
                    ApplicationNumber=serializer.validated_data.get('ApplicationNumber'),
                    LoanPurpose=serializer.validated_data.get('LoanPurpose'),
                    ContractStartDate=serializer.validated_data.get('ContractStartDate'),
                    ContractEndDate=serializer.validated_data.get('ContractEndDate'),
                    FSP1Code=serializer.validated_data.get('FSP1Code'),
                    FSP1LoanNumber=serializer.validated_data.get('FSP1LoanNumber'),
                    TakeOverBalance=serializer.validated_data.get('TakeOverBalance'),
                    FSP1EndDate=serializer.validated_data.get('FSP1EndDate'),
                    FSP1LastDeductionDate=serializer.validated_data.get('FSP1LastDeductionDate'),
                    FSP1BankAccount=serializer.validated_data.get('FSP1BankAccount'),
                    FSP1BankAccountName=serializer.validated_data.get('FSP1BankAccountName'),
                    FSP1SWIFTCode=serializer.validated_data.get('FSP1SWIFTCode'),
                    FSP1MNOChannels=serializer.validated_data.get('FSP1MNOChannels'),
                    FSP1PaymentReferenceNumber=serializer.validated_data.get('FSP1PaymentReferenceNumber'),
                    FSP1FinalPaymentDate=serializer.validated_data.get('FSP1FinalPaymentDate'),
                    LoanOfferType=loan_offer_type,
                    MessageType=header_data.get('MessageType'),
                    RequestType=INCOMING,
                    status=0
                )
            except Exception as e:
                return Response(
                    {'error': f'Failed to save LoanOfferRequest: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content_type='application/xml'
                )

            return Response(
                {'message': 'Loan offer request processed successfully'},
                status=status.HTTP_200_OK,
                content_type='application/xml'
            )
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
