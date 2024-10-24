import re

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import xmltodict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from emkopo_api.mixins import log_and_make_api_call
from emkopo_constants.constants import INCOMING
from emkopo_loan.models import LoanPayOffBalanceRequest


class LoanPayOffBalanceRequestAPIView(APIView):
    """
    API View to receive top-up payoff balance request from a third-party system.
    """

    @swagger_auto_schema(
        operation_description="Receive top-up payoff balance request from the third-party system",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="XML payload containing top-up payoff balance request",
        ),
        responses={
            200: openapi.Response(description="Successful Response"),
            400: openapi.Response(description="Invalid XML data or missing required fields"),
            500: openapi.Response(description="Internal Server Error"),
        },
        consumes=['application/xml'],  # Indicate that the API consumes XML
    )
    def post(self, request, *args, **kwargs):
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

            return payoff_balance_request(data_dict, xml_data)

        except Exception as e:
            return Response({'error': f'Invalid XML data: {str(e)}'},
                            status=status.HTTP_400_BAD_REQUEST)

def payoff_balance_request(data_dict, xml_data):
    log_and_make_api_call(
        request_type=INCOMING,
        payload=xml_data,
        signature=settings.ESS_SIGNATURE,
        url=settings.ESS_UTUMISHI_API
    )

    # Extract data from the parsed dictionary
    document = data_dict.get('Document', {})
    data = document.get('Data', {})
    message_details = data.get('MessageDetails', {})

    # Extract specific fields from the XML payload
    check_number = message_details.get('CheckNumber')
    loan_number = message_details.get('LoanNumber')
    first_name = message_details.get('FirstName')
    middle_name = message_details.get('MiddleName')
    last_name = message_details.get('LastName')
    vote_code = message_details.get('VoteCode')
    vote_name = message_details.get('VoteName')
    deduction_amount = message_details.get('DeductionAmount')
    deduction_code = message_details.get('DeductionCode')
    deduction_name = message_details.get('DeductionName')
    deduction_balance = message_details.get('DeductionBalance')
    payment_option = message_details.get('PaymentOption')

    # Validate required fields
    if not check_number or not loan_number or not first_name or not middle_name or not last_name:
        return Response(
            {
                'error': 'CheckNumber, LoanNumber, FirstName, MiddleName, and LastName are required fields.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create a new LoanPayOffBalanceRequest object
    LoanPayOffBalanceRequest.objects.create(
        CheckNumber=check_number,
        LoanNumber=loan_number,
        FirstName=first_name,
        MiddleName=middle_name,
        LastName=last_name,
        VoteCode=vote_code,
        VoteName=vote_name,
        DeductionAmount=deduction_amount,
        DeductionCode=deduction_code,
        DeductionName=deduction_name,
        DeductionBalance=deduction_balance,
        PaymentOption=payment_option,
        MessageType="TOP_UP_PAY_0FF_BALANCE_REQUEST",
        RequestType=INCOMING,
    )

    return Response({'message': 'Pay off balance request created successfully.'},
                    status=status.HTTP_200_OK)
